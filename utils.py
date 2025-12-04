import os
import google.generativeai as genai
from PIL import Image
import pandas as pd
import json
import re
import shutil



def configure_gemini(api_key):
    """Configures the Gemini API with the provided key."""
    genai.configure(api_key=api_key)

def extract_receipt_info(image_path):
    """
    Sends an image to Gemini and extracts receipt information.
    Returns a dictionary with the extracted fields.
    """
    model = genai.GenerativeModel('gemini-flash-latest')
    
    try:
        img = Image.open(image_path)
    except Exception as e:
        return {"Error": f"Failed to open image: {e}"}

    prompt = """
    Analyze this receipt/invoice image and extract the following information in JSON format:
    - Date (YYYY-MM-DD format)
    - Item Category (e.g., Food, Transport, Office Supplies, Inventory, Utilities, etc. Choose the most appropriate one.)
    - Vendor Name
    - Item Name (A concise summary of the main item or service. If multiple, summarize e.g., "Groceries" or "Office Stationery")
    - Receipt_Invoice_No (The receipt or invoice number)
    - Price Amount (The total amount, just the number, e.g., 150.00)

    Ensure the keys in the JSON are exactly: "Date", "Item Category", "Vendor Name", "Item Name", "Receipt_Invoice_No", "Price Amount".
    If a field is missing or illegible, use "Unknown".
    """

    try:
        response = model.generate_content([prompt, img])
        text_response = response.text
        # Clean up potential markdown code blocks
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0]
        
        data = json.loads(text_response)
        data['File Name'] = os.path.basename(image_path)
        return data
    except Exception as e:
        print(f"DEBUG: Extraction Error for {image_path}: {e}")
        return {
            "Date": "Error",
            "Item Category": "Error",
            "Vendor Name": "Error",
            "Item Name": "Error",
            "Receipt_Invoice_No": "Error",
            "Price Amount": "Error",
            "File Name": os.path.basename(image_path),
            "Error Details": str(e)
        }

def sanitize_filename(text):
    """Removes illegal characters from a string to make it safe for a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", str(text))

def rename_file(original_path, data):
    """
    Renames the file based on the extracted data.
    Format: <Date> - <Item Category> - <Vendor Name> - <Item Name> - <Receipt/Invoice No.> - <Price Amount>
    """
    try:
        directory = os.path.dirname(original_path)
        extension = os.path.splitext(original_path)[1]
        
        # Construct new filename
        new_name_parts = [
            data.get("Date", "Unknown"),
            data.get("Item Category", "Unknown"),
            data.get("Vendor Name", "Unknown"),
            data.get("Item Name", "Unknown"),
            data.get("Receipt_Invoice_No", "Unknown"),
            str(data.get("Price Amount", "Unknown"))
        ]
        
        # Sanitize each part
        safe_parts = [sanitize_filename(part).strip() for part in new_name_parts]
        new_filename = " - ".join(safe_parts) + extension
        
        new_path = os.path.join(directory, new_filename)
        
        # Handle duplicates
        counter = 1
        while os.path.exists(new_path):
            new_filename = " - ".join(safe_parts) + f" ({counter})" + extension
            new_path = os.path.join(directory, new_filename)
            counter += 1
            
        os.rename(original_path, new_path)
        return new_path
    except Exception as e:
        print(f"Error renaming file {original_path}: {e}")
        return original_path

def extract_receipt_info(image_path):
    """
    Sends an image to Gemini and extracts receipt information.
    Returns a dictionary with the extracted fields.
    """
    model = genai.GenerativeModel('gemini-flash-latest')
    
    try:
        img = Image.open(image_path)
    except Exception as e:
        return {"Error": f"Failed to open image: {e}"}

    prompt = """
    Analyze this receipt/invoice image and extract the following information in JSON format:
    - Date (YYYY-MM-DD format)
    - Item Category (e.g., Food, Transport, Office Supplies, Inventory, Utilities, etc. Choose the most appropriate one.)
    - Vendor Name
    - Item Name (A concise summary of the main item or service. If multiple, summarize e.g., "Groceries" or "Office Stationery")
    - Receipt_Invoice_No (The receipt or invoice number)
    - Price Amount (The total amount in format "RM 0.00", e.g., "RM 150.00". If currency is missing, assume RM.)

    Ensure the keys in the JSON are exactly: "Date", "Item Category", "Vendor Name", "Item Name", "Receipt_Invoice_No", "Price Amount".
    If a field is missing or illegible, use "Unknown".
    """

    try:
        response = model.generate_content([prompt, img])
        text_response = response.text
        # Clean up potential markdown code blocks
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0]
        
        data = json.loads(text_response)
        data['File Name'] = os.path.basename(image_path)
        return data
    except Exception as e:
        print(f"DEBUG: Extraction Error for {image_path}: {e}")
        return {
            "Date": "Error",
            "Item Category": "Error",
            "Vendor Name": "Error",
            "Item Name": "Error",
            "Receipt_Invoice_No": "Error",
            "Price Amount": "Error",
            "File Name": os.path.basename(image_path),
            "Error Details": str(e)
        }

def sanitize_filename(text):
    """Removes illegal characters from a string to make it safe for a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", str(text))

def generate_filename(data, extension, format_string="{Date} - {Item Category} - {Vendor Name} - {Item Name} - {Receipt_Invoice_No} - RM{Price Amount}"):
    """Generates a filename based on the format string and data."""
    try:
        # Create a safe dictionary for formatting
        safe_data = {k: sanitize_filename(str(v)).strip() for k, v in data.items()}
        
        # Fill in missing keys with "Unknown" to prevent errors
        keys = ["Date", "Item Category", "Vendor Name", "Item Name", "Receipt_Invoice_No", "Price Amount"]
        for key in keys:
            if key not in safe_data or not safe_data[key]:
                safe_data[key] = "Unknown"
                
        # Format the string
        new_filename = format_string.format(**safe_data)
        
        # Ensure extension is present
        if not new_filename.lower().endswith(extension.lower()):
            new_filename += extension
            
        return new_filename
    except Exception as e:
        print(f"Error generating filename: {e}")
        return f"Error_Renaming{extension}"

def rename_file(original_path, data, format_string="{Date} - {Item Category} - {Vendor Name} - {Item Name} - {Receipt_Invoice_No} - RM{Price Amount}"):
    """
    Renames the file based on the extracted data and format string.
    """
    try:
        directory = os.path.dirname(original_path)
        extension = os.path.splitext(original_path)[1]
        
        new_filename = generate_filename(data, extension, format_string)
        new_path = os.path.join(directory, new_filename)
        
        # Handle duplicates
        counter = 1
        while os.path.exists(new_path):
            name_part = os.path.splitext(new_filename)[0]
            new_path = os.path.join(directory, f"{name_part} ({counter}){extension}")
            counter += 1
            
        os.rename(original_path, new_path)
        return new_path
    except Exception as e:
        print(f"Error renaming file {original_path}: {e}")
        return original_path

def copy_and_rename_file(original_path, data, destination_folder, format_string="{Date} - {Item Category} - {Vendor Name} - {Item Name} - {Receipt_Invoice_No} - RM{Price Amount}"):
    """
    Copies the file to the destination folder and renames it based on the extracted data and format string.
    """
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            
        extension = os.path.splitext(original_path)[1]
        
        new_filename = generate_filename(data, extension, format_string)
        new_path = os.path.join(destination_folder, new_filename)
        
        # Handle duplicates
        counter = 1
        while os.path.exists(new_path):
            name_part = os.path.splitext(new_filename)[0]
            new_path = os.path.join(destination_folder, f"{name_part} ({counter}){extension}")
            counter += 1
            
        shutil.copy2(original_path, new_path)
        return new_path
    except Exception as e:
        print(f"Error copying file {original_path}: {e}")
        return original_path
