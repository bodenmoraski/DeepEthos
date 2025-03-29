@echo off
REM Script to install all requirements for the Philosophical Alignment Research Framework

echo Installing dependencies for the Philosophical Alignment Research Framework...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python could not be found. Please install Python 3.7+ before proceeding.
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo Python version %PYVER% detected. Proceeding with installation...

REM Install using pip
echo Installing required packages...
pip install -e .

REM Check if .env file exists, create if not
if not exist .env (
    echo Creating .env file for API keys...
    (
        echo # API keys for different providers
        echo # Uncomment and add your keys as needed
        echo.
        echo # OpenAI API Key
        echo # OPENAI_API_KEY=your_openai_key_here
        echo.
        echo # Anthropic API Key
        echo # ANTHROPIC_API_KEY=your_anthropic_key_here
        echo.
        echo # Google Gemini API Key
        echo # GEMINI_API_KEY=your_gemini_key_here
    ) > .env
    echo .env file created. Please edit it to add your API keys.
) else (
    echo .env file already exists. Please make sure it contains your API keys.
)

echo.
echo Installation completed!
echo.
echo To use the framework:
echo 1. Edit the .env file to add your API keys
echo 2. Generate scenarios with: python code\tester.py
echo 3. Run analysis with: python code\multi_provider_integration.py --providers openai anthropic google
echo.
echo For more options, see README.md

pause 