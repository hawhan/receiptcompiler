@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Building executable...
pyinstaller --noconfirm --onefile --windowed ^
    --name "ReceiptsCompiler" ^
    --hidden-import=streamlit ^
    --hidden-import=pandas ^
    --hidden-import=google.generativeai ^
    --hidden-import=PIL ^
    --hidden-import=dotenv ^
    --hidden-import=openpyxl ^
    --collect-all streamlit ^
    --add-data "app.py;." ^
    --add-data "utils.py;." ^
    --add-data "file_dialog.py;." ^
    --add-data ".env.example;." ^
    run_executable.py

echo Build complete! Executable is in the 'dist' folder.
pause
