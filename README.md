# PhilAlignment

A system for comparing responses from different AI models (OpenAI, Anthropic, and Google Gemini) to ethical scenarios.

## Overview

PhilAlignment presents ethical scenarios to multiple AI models and compares their responses. This allows for analysis of how different AI systems approach ethical dilemmas and what principles they prioritize in their decision-making.

## Features

- Run ethical scenarios through multiple AI models (OpenAI, Anthropic, and Google Gemini)
- Store and view responses for comparison
- Multiple pre-defined ethical scenarios
- User-friendly console interface for easy interaction
- Command-line interface for running scenarios and viewing responses
- Database management tools for clearing and backing up responses
- Google Cloud Storage integration for automatic backups and syncing

## Requirements

- Python 3.6+
- API keys for OpenAI, Anthropic, and Google Gemini
- (Optional) Google Cloud Storage bucket for cloud backups

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:

```
# API Keys for LLM providers
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key

# Google Cloud Storage Configuration (optional)
GCS_BUCKET_NAME=your-bucket-name
GCS_CREDENTIALS_PATH=/path/to/credentials.json
AUTO_CLOUD_SYNC=false  # Set to 'true' to enable automatic cloud syncing
```

## Google Cloud Storage Setup (Optional)

To use the Google Cloud Storage integration:

1. Create a Google Cloud account if you don't have one
2. Create a new project in Google Cloud Console
3. Enable the Google Cloud Storage API
4. Create a service account with Storage Admin permissions
5. Download the service account key JSON file
6. Update your `.env` file with the bucket name and path to the credentials file
7. Set `AUTO_CLOUD_SYNC=true` in your `.env` file to enable automatic syncing

## Usage

### Interactive Console (Recommended)

The easiest way to use PhilAlignment is through the interactive console:

```bash
python philalignment.py
```

This will start an interactive console where you can:
- List available scenarios
- Run scenarios with all AI models
- View and manage responses
- Test API connections
- Create database backups
- Sync and backup to Google Cloud Storage

Type `help` in the console to see all available commands.

### Cloud Storage Commands

If you've configured Google Cloud Storage, you can use these commands in the console:

```
cloud sync    - Sync responses to Google Cloud Storage
cloud backup  - Create a backup in Google Cloud Storage
cloud list    - List backups in Google Cloud Storage
cloud restore - Restore responses from Google Cloud Storage
cloud status  - Check Google Cloud Storage configuration
```

### Command-line Scripts

Alternatively, you can use the individual command-line scripts:

#### Running a Scenario

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

#### Viewing Responses

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

#### Managing the Database

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

- `philalignment.py`: Interactive console interface for the system
- `api.py`: Functions for interacting with AI model APIs
- `main.py`: Main script for running the default scenario
- `run_scenario.py`: Script for running specific scenarios
- `view_responses.py`: Script for viewing stored responses
- `clear_database.py`: Script for clearing and backing up the database
- `cloud_storage.py`: Functions for Google Cloud Storage integration
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

## Acknowledgements

This project incorporates data from:

- [MultiTP](https://github.com/causalNLP/MultiTP) by causalNLP - MIT License
- [Ethics](https://github.com/hendrycks/ethics) by Dan Hendrycks et al. - MIT License

We are grateful to the authors for making these resources available.

## License

See the LICENSE file for details. 