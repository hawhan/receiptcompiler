# 🧾 Receipts Compiler & Organizer

A Progressive Web App (PWA) that extracts information from receipts and invoices using AI, compiles them into CSV or Excel files, and organizes files automatically.

![PWA Enabled](https://img.shields.io/badge/PWA-Enabled-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## ✨ Features

- 📸 **AI-Powered Extraction**: Uses Google Gemini AI to extract key information from receipt/invoice images
- 📊 **Data Compilation**: Exports extracted data to CSV or Excel format
- 📱 **Progressive Web App**: Install on desktop or mobile for app-like experience
- 🔄 **Batch Processing**: Process multiple receipts at once
- 💾 **File Organization**: Automatically rename and organize processed files
- 🌐 **Cloud-Ready**: Deploy to Streamlit Community Cloud for access anywhere

## 📋 Extracted Information

- Date
- Item Category
- Vendor Name
- Item Name
- Receipt/Invoice Number
- Price Amount
- Original File Name

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd receipts-compiler
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   
   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   
   Open your browser to `http://localhost:8501`

### Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Streamlit Community Cloud.

## 📱 Installing as PWA

### Desktop (Chrome/Edge)
1. Open the app in your browser
2. Look for the install icon (⊕) in the address bar
3. Click "Install Receipts Compiler"

### Mobile (Android)
1. Open the app in Chrome
2. Tap menu (⋮) → "Add to Home screen"

### Mobile (iOS)
1. Open the app in Safari
2. Tap Share → "Add to Home Screen"

## 🎯 Usage

1. **Upload Files**: Select "Upload Files" mode and upload your receipt/invoice images
2. **Configure Options**: Choose file handling and output format preferences
3. **Process**: Click "Start Processing" to extract information
4. **Download**: Download the compiled CSV/Excel file with all extracted data

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Data Processing**: Pandas
- **Image Handling**: Pillow
- **PWA**: Service Workers, Web App Manifest

## 📁 Project Structure

```
receipts-compiler/
├── app.py                  # Main Streamlit application
├── utils.py                # Utility functions for AI extraction
├── requirements.txt        # Python dependencies
├── static/                 # PWA assets
│   ├── manifest.json       # Web app manifest
│   ├── service-worker.js   # Service worker for offline support
│   ├── favicon.ico         # Browser favicon
│   └── icons/              # App icons
├── .streamlit/             # Streamlit configuration
│   └── config.toml
└── PWA_GUIDE.md           # PWA installation guide

```

## 🔒 Security

- API keys are stored securely using Streamlit Secrets (cloud) or environment variables (local)
- Never commit `.env` files or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👤 Author

Your Name

## 🙏 Acknowledgments

- Google Gemini AI for receipt/invoice information extraction
- Streamlit for the amazing web framework
- PWA technology for enhanced user experience
