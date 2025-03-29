#!/bin/bash
# Installation script for DeepEthos framework

echo "Starting DeepEthos framework installation..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$python_version < 3.7" | bc -l) )); then
    echo "Python 3.7 or higher is required. Found version $python_version"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not found. Please install pip for Python 3."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
pip3 install -e .

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file for API keys..."
    cat > .env << EOF
# API Keys for LLM providers
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
EOF
    echo "Please edit the .env file with your actual API keys."
fi

echo "Installation complete!"
echo "To start using DeepEthos:"
echo "1. Edit the .env file with your API keys"
echo "2. Generate test scenarios: python code/tester.py"
echo "3. Run analysis: python code/multi_provider_integration.py" 