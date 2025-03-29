@echo off
rem PhilAlignment - A Framework for Analyzing Philosophical Alignment in AI Models
rem This script provides a convenient way to run the PhilAlignment framework

rem Get the directory of this script
set SCRIPT_DIR=%~dp0

rem Ensure we're in the project root directory
cd /d "%SCRIPT_DIR%"

rem Ensure Python can find our modules
set PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%

rem First copy existing scripts to the new structure if they don't exist
if not exist "code\providers\multi_provider_integration.py" (
    echo Setting up the framework structure...
    mkdir code\providers code\generation code\analysis 2>nul
    
    rem Copy scripts if they exist
    if exist "code\multi_provider_integration.py" copy code\multi_provider_integration.py code\providers\
    if exist "code\openai_integration.py" copy code\openai_integration.py code\providers\
    if exist "code\tester.py" copy code\tester.py code\generation\
    if exist "code\question_generator.py" copy code\question_generator.py code\generation\
    if exist "code\validate_scenarios.py" copy code\validate_scenarios.py code\analysis\
    if exist "code\compare_reasoning_approaches.py" copy code\compare_reasoning_approaches.py code\analysis\
)

rem Run the main interface
python -m code.core.philalignment %* 