@echo off
echo Starting Raffle Application...

REM Try to install the most basic required packages
echo Checking for required packages...
pip install fastapi jinja2 python-multipart --user

REM Try to start with uvicorn
python -c "import uvicorn" 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo Starting with uvicorn...
    python -m uvicorn app:app --host 0.0.0.0 --port 8000
) else (
    echo uvicorn not found, starting application directly...
    python app.py
)

echo.
echo If the application didn't start, try running one of these commands:
echo python -m http.server 8000
echo.
echo Then open your browser to http://localhost:8000
pause 