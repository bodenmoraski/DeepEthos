#!/usr/bin/env python3
"""
PhilAlignment - Console Interface

A user-friendly console interface for PhilAlignment that makes it easy to use all the functionality
from a single program.
"""

import os
import sys
import cmd
import textwrap
from typing import List, Optional

# Import functionality from other modules
import scripts.api as api
import storage
import scenarios
from final_prompt import construct_prompt
from scripts.api import format_openai_output, format_anthropic_output, format_gemini_output
import clear_database

# Try to import cloud storage module
try:
    import cloud_storage
    CLOUD_STORAGE_AVAILABLE = True
except ImportError:
    CLOUD_STORAGE_AVAILABLE = False

class PhilAlignmentConsole(cmd.Cmd):
    """
    Interactive console for PhilAlignment.
    Provides a user-friendly interface for running scenarios, viewing responses, and managing the database.
    """
    
    intro = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                           PhilAlignment Console                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    Welcome to PhilAlignment, a system for comparing responses from different AI models
    to ethical scenarios.
    
    Type 'help' or '?' to list available commands.
    Type 'quit' or 'exit' to exit the program.
    """
    
    prompt = "philalignment> "
    
    def __init__(self):
        super().__init__()
        self.scenario_names = scenarios.get_scenario_names()
        
        # Check if cloud storage is configured
        self.cloud_storage_configured = False
        if CLOUD_STORAGE_AVAILABLE:
            self.cloud_storage_configured = cloud_storage.is_cloud_storage_configured()
            if self.cloud_storage_configured:
                print("Google Cloud Storage is configured and available.")
            else:
                print("Google Cloud Storage is not configured. Set GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH in .env file.")
    
    def do_help(self, arg):
        """
        Show help information about available commands.
        Usage: help [command]
        """
        if not arg:
            print("\nAvailable commands:")
            print("  scenarios - List all available scenarios")
            print("  run       - Run a scenario with all AI models")
            print("  list      - List all stored responses")
            print("  view      - View a specific response")
            print("  clear     - Clear responses from the database")
            print("  backup    - Create a backup of the database")
            print("  test      - Test API connections")
            
            # Cloud storage commands
            if CLOUD_STORAGE_AVAILABLE:
                print("\nCloud Storage Commands:")
                print("  cloud sync    - Sync responses to Google Cloud Storage")
                print("  cloud backup  - Create a backup in Google Cloud Storage")
                print("  cloud list    - List backups in Google Cloud Storage")
                print("  cloud restore - Restore responses from Google Cloud Storage")
                print("  cloud status  - Check Google Cloud Storage configuration")
            
            print("\nOther Commands:")
            print("  help      - Show this help message")
            print("  quit      - Exit the program")
            print("\nType 'help <command>' for more information about a specific command.")
        else:
            # Call the default help method for specific commands
            super().do_help(arg)
    
    def do_scenarios(self, arg):
        """
        List all available scenarios.
        Usage: scenarios
        """
        print("\nAvailable scenarios:")
        for i, name in enumerate(self.scenario_names, 1):
            print(f"  {i}. {name}")
    
    def do_run(self, arg):
        """
        Run a scenario with all AI models.
        Usage: run <scenario_id>
        Example: run 1
        """
        if not arg:
            print("Error: Please specify a scenario ID.")
            print("Usage: run <scenario_id>")
            print("Example: run 1")
            print("\nAvailable scenarios:")
            for i, name in enumerate(self.scenario_names, 1):
                print(f"  {i}. {name}")
            return
        
        try:
            scenario_id = int(arg)
            if scenario_id < 1 or scenario_id > len(self.scenario_names):
                print(f"Error: Invalid scenario ID. Please choose a number between 1 and {len(self.scenario_names)}.")
                return
            
            # Get the scenario
            scenario = scenarios.get_scenario(scenario_id)
            print(f"\nRunning scenario {scenario_id}: {self.scenario_names[scenario_id-1]}")
            print(f"Description: {scenario}")
            
            # Construct the prompt
            prompt = construct_prompt(scenario)
            print(f"Prompt constructed successfully. Length: {len(prompt)} characters")
            
            # Get responses from different models
            print("\nGetting responses from models...")
            
            try:
                openai_response = format_openai_output(prompt)
                print(f"OpenAI response received. Word count: {openai_response['word_count']}")
            except Exception as e:
                print(f"Error getting OpenAI response: {e}")
                openai_response = {"error": str(e), "output_text": "Error generating response"}
            
            try:
                anthropic_response = format_anthropic_output(prompt)
                print(f"Anthropic response received. Word count: {anthropic_response['word_count']}")
            except Exception as e:
                print(f"Error getting Anthropic response: {e}")
                anthropic_response = {"error": str(e), "output_text": "Error generating response"}
            
            try:
                gemini_response = format_gemini_output(prompt)
                print(f"Gemini response received. Word count: {gemini_response['word_count']}")
            except Exception as e:
                print(f"Error getting Gemini response: {e}")
                gemini_response = {"error": str(e), "output_text": "Error generating response"}
            
            # Save the responses to storage
            storage.save_response(
                scenario_id=scenario_id,
                scenario_text=scenario,
                openai_response=openai_response,
                anthropic_response=anthropic_response,
                gemini_response=gemini_response
            )
            
            # Print a summary
            print("\nResponse Summary:")
            print(f"OpenAI: {openai_response.get('word_count', 'Error')} words")
            print(f"Anthropic: {anthropic_response.get('word_count', 'Error')} words")
            print(f"Gemini: {gemini_response.get('word_count', 'Error')} words")
            
            # Ask if the user wants to view the responses
            view_responses = input("\nDo you want to view the responses? (y/n): ")
            if view_responses.lower() in ['y', 'yes']:
                self._print_responses(openai_response, anthropic_response, gemini_response)
            
        except ValueError:
            print("Error: Scenario ID must be a number.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def do_list(self, arg):
        """
        List all stored responses.
        Usage: list
        """
        responses = storage.load_responses()
        
        if not responses:
            print("No responses found in storage.")
            return
        
        print(f"\nFound {len(responses)} stored responses:\n")
        
        for i, response in enumerate(responses):
            # Format timestamp
            timestamp = response.get("timestamp", "Unknown")
            if "T" in timestamp:
                timestamp = timestamp.replace("T", " ").split(".")[0]
            
            scenario_id = response.get("scenario_id", "Unknown")
            scenario_name = self.scenario_names[scenario_id-1] if 1 <= scenario_id <= len(self.scenario_names) else "Unknown"
            
            # Get word counts
            openai_words = response.get("responses", {}).get("openai", {}).get("word_count", "N/A")
            anthropic_words = response.get("responses", {}).get("anthropic", {}).get("word_count", "N/A")
            gemini_words = response.get("responses", {}).get("gemini", {}).get("word_count", "N/A")
            
            print(f"Response #{i+1} - Scenario {scenario_id}: {scenario_name}")
            print(f"  Time: {timestamp}")
            print(f"  Word counts: OpenAI: {openai_words}, Anthropic: {anthropic_words}, Gemini: {gemini_words}")
            print()
    
    def do_view(self, arg):
        """
        View a specific response.
        Usage: view <response_id>
        Example: view 1
        """
        if not arg:
            print("Error: Please specify a response ID.")
            print("Usage: view <response_id>")
            print("Example: view 1")
            print("\nUse 'list' to see all available responses.")
            return
        
        try:
            response_id = int(arg) - 1  # Convert to 0-based index
            response = storage.get_response_by_id(response_id)
            
            if not response:
                print(f"Error: Response #{arg} not found.")
                return
            
            # Format timestamp
            timestamp = response.get("timestamp", "Unknown")
            if "T" in timestamp:
                timestamp = timestamp.replace("T", " ").split(".")[0]
            
            scenario_id = response.get("scenario_id", "Unknown")
            scenario_name = self.scenario_names[scenario_id-1] if 1 <= scenario_id <= len(self.scenario_names) else "Unknown"
            scenario_text = response.get("scenario_text", "Unknown")
            
            print(f"\nResponse #{int(arg)} - Scenario {scenario_id}: {scenario_name}")
            print(f"Time: {timestamp}\n")
            
            print("SCENARIO:")
            print("="*80)
            print(textwrap.fill(scenario_text, width=80))
            print("\n")
            
            # Get the responses
            openai_response = response.get("responses", {}).get("openai", {})
            anthropic_response = response.get("responses", {}).get("anthropic", {})
            gemini_response = response.get("responses", {}).get("gemini", {})
            
            self._print_responses(openai_response, anthropic_response, gemini_response)
            
        except ValueError:
            print("Error: Response ID must be a number.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def do_clear(self, arg):
        """
        Clear responses from the database.
        Usage: 
          clear all            - Clear all responses
          clear scenario <id>  - Clear responses for a specific scenario
          clear response <id>  - Clear a specific response
        Examples:
          clear all
          clear scenario 1
          clear response 1
        """
        if not arg:
            print("Error: Please specify what to clear.")
            print("Usage:")
            print("  clear all            - Clear all responses")
            print("  clear scenario <id>  - Clear responses for a specific scenario")
            print("  clear response <id>  - Clear a specific response")
            return
        
        args = arg.split()
        
        if args[0] == "all":
            # Ask for confirmation
            confirm = input("Are you sure you want to clear all responses? This cannot be undone. (y/n): ")
            if confirm.lower() in ['y', 'yes']:
                clear_database.clear_all_responses()
            else:
                print("Operation cancelled.")
        
        elif args[0] == "scenario" and len(args) > 1:
            try:
                scenario_id = int(args[1])
                # Ask for confirmation
                confirm = input(f"Are you sure you want to clear all responses for scenario {scenario_id}? This cannot be undone. (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    clear_database.clear_responses_by_scenario(scenario_id)
                else:
                    print("Operation cancelled.")
            except ValueError:
                print("Error: Scenario ID must be a number.")
        
        elif args[0] == "response" and len(args) > 1:
            try:
                response_id = int(args[1]) - 1  # Convert to 0-based index
                # Ask for confirmation
                confirm = input(f"Are you sure you want to clear response #{args[1]}? This cannot be undone. (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    clear_database.clear_response_by_id(response_id)
                else:
                    print("Operation cancelled.")
            except ValueError:
                print("Error: Response ID must be a number.")
        
        else:
            print("Error: Invalid command.")
            print("Usage:")
            print("  clear all            - Clear all responses")
            print("  clear scenario <id>  - Clear responses for a specific scenario")
            print("  clear response <id>  - Clear a specific response")
    
    def do_backup(self, arg):
        """
        Create a backup of the database.
        Usage: backup
        """
        clear_database.backup_database()
    
    def do_test(self, arg):
        """
        Test API connections.
        Usage: test
        """
        print("\nTesting API connections...")
        
        # Simple test prompt
        test_prompt = "Explain the concept of artificial intelligence in one paragraph."
        
        # Test OpenAI
        print("\nTesting OpenAI API...")
        try:
            openai_response = api.generate_openai_response(test_prompt)
            word_count = len(openai_response.split())
            if "Error" in openai_response:
                print(f"❌ OpenAI API Error: {openai_response}")
            else:
                print(f"✅ OpenAI API is working. Response: {word_count} words")
        except Exception as e:
            print(f"❌ OpenAI API Error: {str(e)}")
        
        # Test Anthropic
        print("\nTesting Anthropic API...")
        try:
            anthropic_response = api.generate_anthropic_response(test_prompt)
            word_count = len(anthropic_response.split())
            if "Error" in anthropic_response:
                print(f"❌ Anthropic API Error: {anthropic_response}")
            else:
                print(f"✅ Anthropic API is working. Response: {word_count} words")
        except Exception as e:
            print(f"❌ Anthropic API Error: {str(e)}")
        
        # Test Gemini
        print("\nTesting Google Gemini API...")
        try:
            gemini_response = api.generate_gemini_response(test_prompt)
            word_count = len(gemini_response.split())
            if "Error" in gemini_response or "No suitable" in gemini_response:
                print(f"❌ Gemini API Error: {gemini_response}")
            else:
                print(f"✅ Gemini API is working. Response: {word_count} words")
        except Exception as e:
            print(f"❌ Gemini API Error: {str(e)}")
        
        # Test Cloud Storage if available
        if CLOUD_STORAGE_AVAILABLE:
            print("\nTesting Google Cloud Storage...")
            if cloud_storage.is_cloud_storage_configured():
                print(f"✅ Google Cloud Storage is configured.")
                print(f"   Bucket: {cloud_storage.GCS_BUCKET_NAME}")
                print(f"   Credentials: {cloud_storage.GCS_CREDENTIALS_PATH}")
            else:
                print("❌ Google Cloud Storage is not configured.")
                print("   Set GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH in .env file.")
    
    def do_cloud(self, arg):
        """
        Cloud storage commands.
        Usage:
          cloud sync    - Sync responses to Google Cloud Storage
          cloud backup  - Create a backup in Google Cloud Storage
          cloud list    - List backups in Google Cloud Storage
          cloud restore - Restore responses from Google Cloud Storage
          cloud status  - Check Google Cloud Storage configuration
        """
        if not CLOUD_STORAGE_AVAILABLE:
            print("Error: Google Cloud Storage is not available.")
            print("Install the required package with 'pip install google-cloud-storage'")
            return
        
        if not arg:
            print("Error: Please specify a cloud storage command.")
            print("Usage:")
            print("  cloud sync    - Sync responses to Google Cloud Storage")
            print("  cloud backup  - Create a backup in Google Cloud Storage")
            print("  cloud list    - List backups in Google Cloud Storage")
            print("  cloud restore - Restore responses from Google Cloud Storage")
            print("  cloud status  - Check Google Cloud Storage configuration")
            return
        
        args = arg.split()
        command = args[0].lower()
        
        if command == "sync":
            storage.sync_to_cloud()
        
        elif command == "backup":
            if cloud_storage.is_cloud_storage_configured():
                cloud_storage.backup_responses_to_gcs()
            else:
                print("Google Cloud Storage is not configured. Set GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH in .env file.")
        
        elif command == "list":
            storage.list_cloud_backups()
        
        elif command == "restore":
            if len(args) > 1:
                backup_name = args[1]
                storage.restore_from_cloud(backup_name)
            else:
                # Ask for confirmation before restoring the latest backup
                confirm = input("Are you sure you want to restore the latest backup from Google Cloud Storage? This will overwrite your current responses. (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    storage.restore_from_cloud()
                else:
                    print("Operation cancelled.")
        
        elif command == "status":
            if cloud_storage.is_cloud_storage_configured():
                print("Google Cloud Storage is configured.")
                print(f"Bucket: {cloud_storage.GCS_BUCKET_NAME}")
                print(f"Credentials: {cloud_storage.GCS_CREDENTIALS_PATH}")
                
                # Check if AUTO_CLOUD_SYNC is enabled
                if storage.AUTO_CLOUD_SYNC:
                    print("Automatic cloud sync is ENABLED.")
                else:
                    print("Automatic cloud sync is DISABLED.")
                    print("To enable, set AUTO_CLOUD_SYNC=true in your .env file.")
            else:
                print("Google Cloud Storage is not configured.")
                print("To configure, set the following in your .env file:")
                print("  GCS_BUCKET_NAME=your-bucket-name")
                print("  GCS_CREDENTIALS_PATH=/path/to/credentials.json")
        
        else:
            print(f"Error: Unknown cloud command '{command}'")
            print("Usage:")
            print("  cloud sync    - Sync responses to Google Cloud Storage")
            print("  cloud backup  - Create a backup in Google Cloud Storage")
            print("  cloud list    - List backups in Google Cloud Storage")
            print("  cloud restore - Restore responses from Google Cloud Storage")
            print("  cloud status  - Check Google Cloud Storage configuration")
    
    def do_quit(self, arg):
        """
        Exit the program.
        Usage: quit
        """
        print("Goodbye!")
        return True
    
    def do_exit(self, arg):
        """
        Exit the program.
        Usage: exit
        """
        return self.do_quit(arg)
    
    def emptyline(self):
        """Do nothing on empty line."""
        pass
    
    def _print_responses(self, openai_response, anthropic_response, gemini_response):
        """Helper method to print responses from all models."""
        # Print each model's response
        for model_name, response in [
            ("OPENAI", openai_response),
            ("ANTHROPIC", anthropic_response),
            ("GEMINI", gemini_response)
        ]:
            model_text = response.get("output_text", "No response available")
            model_words = response.get("word_count", "N/A")
            
            print(f"\n{model_name} RESPONSE: ({model_words} words)")
            print("="*80)
            print(textwrap.fill(model_text, width=80))
            print()

def main():
    """Main function to run the console."""
    console = PhilAlignmentConsole()
    try:
        console.cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 