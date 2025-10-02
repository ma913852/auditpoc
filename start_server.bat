@echo off
echo ================================================
echo   Audit POC - LLM Backend Server
echo ================================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with your Databricks credentials.
    echo.
    echo Example:
    echo DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
    echo DATABRICKS_TOKEN=your-token-here
    echo.
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not found. Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo Starting Audit POC Server...
echo Server will run on http://localhost:5000
echo Frontend: http://localhost:5000
echo API: http://localhost:5000/api/
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

