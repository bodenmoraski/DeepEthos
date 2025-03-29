#!/bin/bash
#
# PhilAlignment - A Framework for Analyzing Philosophical Alignment in AI Models
# This script provides a convenient way to run the PhilAlignment framework
#

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ensure we're in the project root directory
cd "$SCRIPT_DIR"

# Ensure Python can find our modules
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# First copy existing scripts to the new structure if they don't exist
if [ ! -d "code/providers" ] || [ ! -f "code/providers/multi_provider_integration.py" ]; then
    echo "Setting up the framework structure..."
    mkdir -p code/providers code/generation code/analysis

    # Copy scripts if they exist
    [ -f "code/multi_provider_integration.py" ] && cp code/multi_provider_integration.py code/providers/
    [ -f "code/openai_integration.py" ] && cp code/openai_integration.py code/providers/
    [ -f "code/tester.py" ] && cp code/tester.py code/generation/
    [ -f "code/question_generator.py" ] && cp code/question_generator.py code/generation/
    [ -f "code/validate_scenarios.py" ] && cp code/validate_scenarios.py code/analysis/
    [ -f "code/compare_reasoning_approaches.py" ] && cp code/compare_reasoning_approaches.py code/analysis/
fi

# Run the main interface
python -m code.core.philalignment "$@" 