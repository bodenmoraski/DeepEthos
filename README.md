# PhilAlignment

A research framework for analyzing philosophical alignment and reasoning approaches across different AI models from multiple providers (OpenAI, Anthropic, and Google Gemini).

## Overview

PhilAlignment generates ethical scenarios and presents them to multiple AI models using various reasoning prompting strategies. It records and analyzes the responses to evaluate how different AI systems approach ethical dilemmas, what principles they prioritize, and how their reasoning processes differ depending on the prompting technique.

## Features

- **Multi-Provider Integration**: Test models from OpenAI (GPT series), Anthropic (Claude models), and Google (Gemini models)
- **Comparative Reasoning Analysis**: Compare three distinct reasoning approaches:
  - Standard prompting (no specific reasoning instructions)
  - Chain-of-Thought (CoT) prompting (explicitly requesting step-by-step reasoning)
  - Induced Chain-of-Thought prompting (providing examples of how to reason)
- **Ethical Scenario Generation**: Create diverse ethical dilemmas across multiple categories (Species, Social Value, Gender, Age, Fitness, Utilitarianism)
- **Automated Analysis & Visualization**: Quantitative comparison of:
  - Response length and complexity
  - Reasoning steps and ethical principles mentioned
  - Decision patterns and distribution
- **Simulation Mode**: Test framework functionality without making actual API calls
- **Flexible Configuration**: Command-line parameters for customizing test runs

## Requirements

- Python 3.7+
- API keys for providers you wish to test:
  - OpenAI API key for GPT models
  - Anthropic API key for Claude models
  - Google API key for Gemini models

## Installation

### Automatic Installation (Recommended)

#### On Unix/Linux/MacOS:
```bash
# Make the installer executable
chmod +x install_requirements.sh
# Run the installer
./install_requirements.sh
```

#### On Windows:
```bash
install_requirements.bat
```

### Manual Installation

1. Clone this repository
2. Install the required packages:

```bash
# Option 1: Using pip with requirements.txt
pip install -r requirements.txt

# Option 2: Using setuptools (recommended for development)
pip install -e .
```

3. Create a `.env` file in the root directory with your API keys:

```
# API Keys for LLM providers
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Usage

### Generating Test Scenarios

First, generate the ethical scenarios that will be used for testing:

```bash
python code/tester.py
```

This will create a file named `generated_moral_machine_scenarios.csv` with sample ethical dilemmas.

### Multi-Provider Integration

The core functionality is in the `multi_provider_integration.py` script, which supports various arguments:

```bash
python code/multi_provider_integration.py [arguments]
```

#### Arguments:

- `--providers`: Specify which providers to use (openai, anthropic, google)
- `--models`: Specific models to test (if not specified, defaults are used)
- `--reasoning`: Reasoning approaches to test (standard, cot, induced_cot)
- `--samples`: Number of samples per category (higher = more comprehensive)
- `--max-tokens`: Maximum tokens for response generation (500-1000 recommended)
- `--categories`: Specific ethical categories to test
- `--simulate`: Run in simulation mode without making actual API calls

#### Examples:

1. Compare OpenAI and Claude models:
   ```bash
   python code/multi_provider_integration.py --providers openai anthropic
   ```

2. Test specific models across providers:
   ```bash
   python code/multi_provider_integration.py --models gpt-4o claude-3-5-sonnet-latest gemini-2.0-flash
   ```

3. Test all providers with Chain-of-Thought reasoning:
   ```bash
   python code/multi_provider_integration.py --providers openai anthropic google --reasoning cot
   ```

4. Run a focused study on specific ethical categories:
   ```bash
   python code/multi_provider_integration.py --providers openai anthropic --categories Species SocialValue
   ```

5. Test in simulation mode (no API calls):
   ```bash
   python code/multi_provider_integration.py --providers openai anthropic google --simulate
   ```

### Comparing Reasoning Approaches

For comparing different reasoning approaches on a set of scenarios:

```bash
python code/compare_reasoning_approaches.py
```

This will run scenarios through the three reasoning approaches and create visualizations.

## Output and Results

After running the scripts, you'll find:

- **Results directory (`results/`)**: JSON files containing the full responses, analyses, and metrics for each model, reasoning type, and scenario.
- **Plots directory (`plots/`)**: Visualization of the results, including:
  - Word count comparison across models and reasoning types
  - Reasoning steps comparison
  - Decision distribution for each reasoning approach
  - Provider-specific comparison charts

## Supported Models

### OpenAI
- gpt-3.5-turbo (latest version)
- gpt-4o (latest omni model)
- o1-mini (reasoning-optimized model)

### Anthropic
- claude-3-5-sonnet-latest
- claude-3-5-haiku-latest
- claude-3-7-sonnet-latest

### Google
- gemini-2.0-flash
- gemini-2.0-flash-lite
- gemini-2.0-pro

## Ethical Categories Tested

- Species (different species saved or sacrificed)
- Social Value (social status differences)
- Gender (gender-based differences)
- Age (age-based differences)
- Fitness (health/fitness differences)
- Utilitarianism (numerical tradeoffs)
- Random (randomly generated scenarios)

## Research Workflow Example

1. **Generate Scenarios**:
   ```bash
   python code/tester.py
   ```

2. **Validate Scenarios** (optional):
   Manually review the generated_moral_machine_scenarios.csv file

3. **Run Multi-Provider Tests**:
   ```bash
   python code/multi_provider_integration.py --providers openai anthropic --samples 5
   ```

4. **Analyze Results**:
   - Review JSON data in the results directory
   - Examine plots in the plots directory

5. **Run More Focused Tests**:
   ```bash
   python code/multi_provider_integration.py --providers openai anthropic --categories Utilitarianism Species --reasoning standard cot --samples 10
   ```

## Extending the Framework

- Add new providers by extending the `setup_clients()` function
- Add new models by updating the `MODELS` dictionary
- Create new reasoning approaches by modifying `create_prompt_variants()`
- Develop new analysis metrics in the `analyze_response()` function

## Acknowledgements

This project incorporates data and methodology from:

- [MultiTP](https://github.com/causalNLP/MultiTP) by causalNLP - MIT License
- [Ethics](https://github.com/hendrycks/ethics) by Dan Hendrycks et al. - MIT License

We are grateful to the authors for making these resources available.

## License

See the LICENSE file for details. 