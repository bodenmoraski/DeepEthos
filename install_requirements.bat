@echo off
REM Installation script for DeepEthos framework

echo Starting DeepEthos framework installation...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is required but not found. Please install Python 3.7 or higher.
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PYVER=%%V
echo Found Python version %PYVER%

REM Install required packages
echo Installing required packages...
pip install -e .

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file for API keys...
    (
    echo # API Keys for LLM providers
    echo OPENAI_API_KEY=your_openai_api_key
    echo ANTHROPIC_API_KEY=your_anthropic_api_key
    echo GEMINI_API_KEY=your_gemini_api_key
    ) > .env
    echo Please edit the .env file with your actual API keys.
)

echo Installation complete!
echo To start using DeepEthos:
echo 1. Edit the .env file with your API keys
echo 2. Generate test scenarios: python code\tester.py
echo 3. Run analysis: python code\multi_provider_integration.py

pause 