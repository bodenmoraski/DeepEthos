# PhilAlignment

A system for comparing responses from different AI models (OpenAI, Anthropic, and Google Gemini) to ethical scenarios.

## Overview

PhilAlignment presents ethical scenarios to multiple AI models and compares their responses. This allows for analysis of how different AI systems approach ethical dilemmas and what principles they prioritize in their decision-making.

## Features

- Run ethical scenarios through multiple AI models (OpenAI, Anthropic, and Google Gemini)
- Store and view responses for comparison
- Multiple pre-defined ethical scenarios
- Command-line interface for running scenarios and viewing responses
- Database management tools for clearing and backing up responses

## Requirements

- Python 3.6+
- API keys for OpenAI, Anthropic, and Google Gemini

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Usage

### Running a Scenario

To run the default scenario (scenario 1):

```bash
python main.py
```

To run a specific scenario:

```bash
python run_scenario.py --run <scenario_id>
```

To list all available scenarios:

```bash
python run_scenario.py --list
```

To run all scenarios:

```bash
python run_scenario.py --all
```

### Viewing Responses

To list all stored responses:

```bash
python view_responses.py --list
```

To view a specific response:

```bash
python view_responses.py --view <response_id>
```

To list responses for a specific scenario:

```bash
python view_responses.py --scenario <scenario_id>
```

### Managing the Database

To clear all responses from the database:

```bash
python clear_database.py --all
```

To clear responses for a specific scenario:

```bash
python clear_database.py --scenario <scenario_id>
```

To clear a specific response by ID:

```bash
python clear_database.py --id <response_id>
```

To create a backup before clearing:

```bash
python clear_database.py --backup --all
```

## File Structure

- `api.py`: Functions for interacting with AI model APIs
- `main.py`: Main script for running the default scenario
- `run_scenario.py`: Script for running specific scenarios
- `view_responses.py`: Script for viewing stored responses
- `clear_database.py`: Script for clearing and backing up the database
- `storage.py`: Functions for storing and retrieving responses
- `scenarios.py`: Definitions of ethical scenarios
- `final_prompt.py`: Functions for constructing prompts
- `test_api.py`: Script for testing API connections

## Scenarios

1. The Medical Breakthrough
2. The False Confession
3. The Autonomous Car Decision
4. The Resource Allocation Dilemma
5. The Corporate Whistleblower Dilemma
6. The AI Surveillance Dilemma

## License

See the LICENSE file for details. 