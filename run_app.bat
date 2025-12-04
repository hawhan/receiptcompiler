@echo off
echo Starting Receipts Compiler...
cd /d "%~dp0"
streamlit run app.py
pause
