#!/bin/bash
# Script to install all requirements for the Philosophical Alignment Research Framework

echo "Installing dependencies for the Philosophical Alignment Research Framework..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3.7+ before proceeding."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
min_version="3.7"

if [ "$(printf '%s\n' "$min_version" "$python_version" | sort -V | head -n1)" != "$min_version" ]; then
    echo "Python version $python_version detected. Please upgrade to Python 3.7 or higher."
    exit 1
else
    echo "Python version $python_version detected. Proceeding with installation..."
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found. Please install pip3 before proceeding."
    exit 1
fi

# Install using pip
echo "Installing required packages..."
pip3 install -e .

# Check if .env file exists, create if not
if [ ! -f .env ]; then
    echo "Creating .env file for API keys..."
    cat > .env << EOF
# API keys for different providers
# Uncomment and add your keys as needed

# OpenAI API Key
# OPENAI_API_KEY=your_openai_key_here

# Anthropic API Key
# ANTHROPIC_API_KEY=your_anthropic_key_here

# Google Gemini API Key
# GEMINI_API_KEY=your_gemini_key_here
EOF
    echo ".env file created. Please edit it to add your API keys."
else
    echo ".env file already exists. Please make sure it contains your API keys."
fi

echo ""
echo "Installation completed!"
echo ""
echo "To use the framework:"
echo "1. Edit the .env file to add your API keys"
echo "2. Generate scenarios with: python code/tester.py"
echo "3. Run analysis with: python code/multi_provider_integration.py --providers openai anthropic google"
echo ""
echo "For more options, see README.md" 