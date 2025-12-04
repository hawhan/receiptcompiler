import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from utils import configure_gemini, extract_receipt_info, rename_file, copy_and_rename_file, generate_filename
import subprocess
import signal
import sys

import shutil
import zipfile
import io

load_dotenv()

st.set_page_config(page_title="Receipts Compiler", layout="wide")

# PWA Integration - Inject meta tags and service worker
pwa_html = """
<head>
    <!-- PWA Meta Tags -->
    <meta name="theme-color" content="#ff4b4b">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Receipts Compiler">
    <meta name="description" content="Extract information from receipts/invoices using AI, compile them into CSV or Excel, and organize files automatically.">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    
    <!-- Apple Touch Icons -->
    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">
    
    <!-- Web App Manifest -->
    <link rel="manifest" href="/static/manifest.json">
</head>

<script>
    // Register Service Worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/service-worker.js')
                .then((registration) => {
                    console.log('Service Worker registered successfully:', registration.scope);
                })
                .catch((error) => {
                    console.log('Service Worker registration failed:', error);
                });
        });
    }
    
    // PWA Install Prompt Handler
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        console.log('PWA install prompt available');
    });
</script>
"""

st.components.v1.html(pwa_html, height=0)

st.title("🧾 Receipts Compiler & Organizer")
st.markdown("""
This tool extracts information from receipts/invoices using AI, compiles them into a CSV or Excel file, 
and renames the files for easy organization.
""")

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    
    if st.button("Stop App", type="primary"):
        os.kill(os.getpid(), signal.SIGTERM)
        
    # Get API key from Streamlit secrets (cloud) or environment variable (local)
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = os.getenv("GEMINI_API_KEY", "")
    
    if not api_key:
        st.error("⚠️ Gemini API key not found. Please configure it in Streamlit secrets or .env file.")
        st.stop()
    


    # File Handling Options
    file_handling = st.radio("File Handling", 
                             ["Rename Original File", "Copy to 'Processed' Folder", "Keep Original (No Action)"],
                             index=1,
                             help="Choose how to handle the source files after processing")
    
    move_to_original = st.checkbox("Move source files to 'Original' folder", value=True, help="Move the original source files to an 'Original' folder after processing")
    
    # Output Format
    output_format = st.selectbox("Output Format", ["CSV", "Excel (.xlsx)", "None"])

    st.info("Note: File moving and renaming on disk is only available in 'Folder Path' mode. For uploaded files, you can download a ZIP of renamed files.")

    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state['processed_data'] = None
    if 'data_saved' not in st.session_state:
        st.session_state['data_saved'] = False

# Main Area UI
selection_container = st.empty()
start_processing = False

with selection_container.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("1. Select Files")
        # File Selection Mode
        selection_mode = st.radio("Selection Mode", ["Upload Files", "Folder Path (Local Only)"], index=0, horizontal=True)
        
        selected_files = []
        folder_path = ""
        uploaded_files = []
        
        if selection_mode == "Upload Files":
            uploaded_files = st.file_uploader(
                "Upload receipt/invoice images",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                help="Select one or more receipt/invoice images to process"
            )
            st.info("Supported formats: .jpg, .jpeg, .png, .webp")
            if uploaded_files:
                st.success(f"Uploaded {len(uploaded_files)} file(s)")
        else:
            default_path = os.getcwd()
            folder_path = st.text_input("Folder Path", value=default_path, help="Path to the folder containing images (local development only)")

    with col2:
        if file_handling != "Keep Original (No Action)":
            st.subheader("2. Renaming Options")
            st.markdown("Customize how your files are renamed.")
            
            default_format = "{Date} - {Item Category} - {Vendor Name} - {Item Name} - {Receipt_Invoice_No} - RM{Price Amount}"
            format_string = st.text_area("Filename Format", value=default_format, height=100, help="Use placeholders like {Date}, {Vendor Name}, etc.")
            
            st.markdown("**Available Tags:**")
            tags = ["{Date}", "{Vendor Name}", "{Price Amount}", "{Item Category}", "{Item Name}", "{Receipt_Invoice_No}"]
            st.code(" ".join(tags), language="text")
            
            # Preview
            st.markdown("**Preview:**")
            example_data = {
                "Date": "2023-10-27",
                "Item Category": "Food",
                "Vendor Name": "Starbucks",
                "Item Name": "Coffee",
                "Receipt_Invoice_No": "12345",
                "Price Amount": "15.50"
            }
            preview_name = generate_filename(example_data, ".jpg", format_string)
            st.info(preview_name)
        else:
            format_string = "" # Not used

    st.divider()
    start_processing = st.button("Start Processing", type="primary", use_container_width=True)

if start_processing:
    selection_container.empty() # Hide the selection UI
    st.session_state['data_saved'] = False # Reset saved state on new run
    
    # if not api_key:
    #     st.error("Please enter a Gemini API Key.")
    if selection_mode == "Folder Path (Local Only)" and not os.path.exists(folder_path):
        st.error("The specified folder path does not exist.")
    elif selection_mode == "Upload Files" and not uploaded_files:
        st.error("Please upload files to process.")
    else:
        configure_gemini(api_key)
        
        # Get list of images
        files_to_process = []
        temp_dir = None
        
        if selection_mode == "Folder Path (Local Only)":
            image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
            files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]
            files_to_process = [os.path.join(folder_path, f) for f in files]
        else:  # Upload Files mode
            # Create temporary directory for uploaded files
            import tempfile
            temp_dir = tempfile.mkdtemp()
            
            for uploaded_file in uploaded_files:
                # Save uploaded file to temp directory
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                files_to_process.append(temp_path)
        
        if not files_to_process:
            st.warning("No image files found.")
        else:
            st.write(f"Found {len(files_to_process)} images. Processing...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            processed_files_map = {} # Map original filename to new path (if renamed) or old path
            
            # Initialize ZIP buffer for Upload Mode
            zip_buffer = None
            zip_file = None
            if selection_mode == "Upload Files":
                zip_buffer = io.BytesIO()
                zip_file = zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED)
            
            for i, file_path in enumerate(files_to_process):
                filename = os.path.basename(file_path)
                status_text.text(f"Processing: {filename}")
                
                # Validate file path
                if not os.path.exists(file_path):
                    st.warning(f"Skipping file not found: {file_path}")
                    continue

                # Archive to 'Original' if requested (only for local folder mode)
                if move_to_original and selection_mode == "Folder Path (Local Only)":
                    try:
                        source_dir = os.path.dirname(file_path)
                        original_dir = os.path.join(source_dir, "Original")
                        if not os.path.exists(original_dir):
                            os.makedirs(original_dir)
                        shutil.copy2(file_path, os.path.join(original_dir, filename))
                    except Exception as e:
                        st.error(f"Error archiving file {filename}: {e}")

                # Extract Info
                data = extract_receipt_info(file_path)
                results.append(data)
                
                # Handle Files based on selection
                if "Error Details" not in data:
                    if selection_mode == "Folder Path (Local Only)":
                        if file_handling == "Rename Original File":
                            new_path = rename_file(file_path, data, format_string)
                            processed_files_map[filename] = new_path
                        elif file_handling == "Copy to 'Processed' Folder":
                            # Determine destination folder
                            source_dir = os.path.dirname(file_path)
                            processed_dir = os.path.join(source_dir, "Processed")
                            new_path = copy_and_rename_file(file_path, data, processed_dir, format_string)
                            processed_files_map[filename] = new_path
                            
                            # Remove original if archived
                            if move_to_original:
                                try:
                                    os.remove(file_path)
                                except Exception as e:
                                    print(f"Error removing original file {file_path}: {e}")

                        else: # Keep Original
                            processed_files_map[filename] = file_path
                            
                            # Remove original if archived (effectively moving it)
                            if move_to_original:
                                try:
                                    os.remove(file_path)
                                except Exception as e:
                                    print(f"Error removing original file {file_path}: {e}")
                    else: # Upload Files Mode
                        # Generate new name for report and ZIP
                        extension = os.path.splitext(filename)[1]
                        new_filename = generate_filename(data, extension, format_string)
                        processed_files_map[filename] = new_filename # Store new name for report
                        
                        # Add to ZIP
                        if zip_file:
                            try:
                                with open(file_path, 'rb') as f:
                                    zip_file.writestr(new_filename, f.read())
                            except Exception as e:
                                print(f"Error adding to zip: {e}")
                else:
                    processed_files_map[filename] = file_path
                
                progress_bar.progress((i + 1) / len(files_to_process))
            
            # Close ZIP
            if zip_file:
                zip_file.close()

            status_text.text("Processing Complete!")
            
            # Create DataFrame
            df = pd.DataFrame(results)
            
            # Reorder columns to match requirements + File Name at end
            desired_columns = ["Date", "Item Category", "Vendor Name", "Item Name", "Receipt_Invoice_No", "Price Amount", "File Name"]
            
            # Check if we have errors to show
            if "Error Details" in df.columns:
                desired_columns.append("Error Details")

            # Ensure all columns exist
            for col in desired_columns:
                if col not in df.columns:
                    df[col] = ""
            
            # Update File Name column if renamed or copied
            if file_handling != "Keep Original (No Action)":
                def get_new_name(row):
                    old_name = row['File Name']
                    if old_name in processed_files_map:
                        return os.path.basename(processed_files_map[old_name])
                    return old_name

                df['File Name'] = df.apply(get_new_name, axis=1)

            final_df = df[desired_columns]
            
            # Store in session state
            st.session_state['processed_data'] = {
                'df': final_df,
                'save_dir': folder_path if selection_mode == "Folder Path (Local Only)" else os.path.dirname(files_to_process[0]),
                'file_handling': file_handling,
                'move_to_original': move_to_original,
                'zip_buffer': zip_buffer
            }

# Display and Save Logic (Outside the button)
if st.session_state['processed_data'] is not None:
    final_df = st.session_state['processed_data']['df']
    save_dir = st.session_state['processed_data']['save_dir']
    file_handling_used = st.session_state['processed_data']['file_handling']
    
    st.subheader("Extracted Data")
    st.dataframe(final_df)
    
    if not st.session_state['data_saved']:
        save_path = ""
        if output_format == "CSV":
            save_path = os.path.join(save_dir, "compiled_receipts.csv")
        elif output_format == "Excel (.xlsx)":
            save_path = os.path.join(save_dir, "compiled_receipts.xlsx")
        
        try:
            if output_format == "CSV":
                if os.path.exists(save_path):
                    existing_df = pd.read_csv(save_path)
                    combined_df = pd.concat([existing_df, final_df], ignore_index=True)
                    combined_df.to_csv(save_path, index=False)
                    st.success(f"Appended data to `{save_path}`")
                else:
                    final_df.to_csv(save_path, index=False)
                    st.success(f"Saved compiled data to `{save_path}`")
            elif output_format == "Excel (.xlsx)":
                if os.path.exists(save_path):
                    existing_df = pd.read_excel(save_path)
                    combined_df = pd.concat([existing_df, final_df], ignore_index=True)
                    combined_df.to_excel(save_path, index=False)
                    st.success(f"Appended data to `{save_path}`")
                else:
                    final_df.to_excel(save_path, index=False)
                    st.success(f"Saved compiled data to `{save_path}`")
            
            # Add Download Button
            with open(save_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(save_path)
                mime_type = "text/csv" if output_format == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                st.download_button(
                    label=f"Download {output_format} File",
                    data=file_data,
                    file_name=file_name,
                    mime=mime_type,
                    type="primary"
                )
                
            # Add ZIP Download Button if available
            zip_buffer = st.session_state['processed_data'].get('zip_buffer')
            if zip_buffer:
                st.download_button(
                    label="Download Renamed Images (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="renamed_receipts.zip",
                    mime="application/zip",
                    type="primary"
                )
            
            if file_handling_used == "Rename Original File":
                st.success("Files have been renamed.")
            elif file_handling_used == "Copy to 'Processed' Folder":
                st.success("Files have been copied to 'Processed' folder.")
            
            if st.session_state['processed_data']['move_to_original']:
                st.success("Original source files moved to 'Original' folder.")
            
            st.session_state['data_saved'] = True
            
        except PermissionError:
            st.error(f"Permission denied: The file `{save_path}` is open in another program. Please close it and try again.")
            if st.button("Retry Save"):
                # The button click triggers a rerun, which will re-execute this block
                pass
    else:
        st.info("Data has been saved.")

