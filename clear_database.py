#!/usr/bin/env python3
"""
Script to clear the database of responses.
This script provides functionality to clear all responses or selectively clear responses.
"""

import os
import json
import argparse
import storage
from typing import List, Dict, Any

def clear_all_responses():
    """
    Clear all responses from the database.
    Creates an empty database file.
    """
    # Ensure the storage directory exists
    storage.ensure_storage_exists()
    
    # Write an empty list to the file
    with open(storage.STORAGE_FILE, 'w') as f:
        json.dump([], f)
    
    print(f"All responses have been cleared from {storage.STORAGE_FILE}")
    print("The database is now empty.")

def clear_responses_by_scenario(scenario_id: int):
    """
    Clear all responses for a specific scenario.
    
    Args:
        scenario_id: The ID of the scenario to clear responses for
    """
    # Load existing responses
    responses = storage.load_responses()
    
    # Count responses for the scenario
    scenario_responses = [r for r in responses if r["scenario_id"] == scenario_id]
    count_before = len(scenario_responses)
    
    if count_before == 0:
        print(f"No responses found for scenario {scenario_id}.")
        return
    
    # Filter out responses for the specified scenario
    filtered_responses = [r for r in responses if r["scenario_id"] != scenario_id]
    
    # Save the filtered responses back to the file
    with open(storage.STORAGE_FILE, 'w') as f:
        json.dump(filtered_responses, f, indent=2)
    
    print(f"Cleared {count_before} responses for scenario {scenario_id}.")
    print(f"Remaining responses: {len(filtered_responses)}")

def clear_response_by_id(response_id: int):
    """
    Clear a specific response by its ID.
    
    Args:
        response_id: The ID (index) of the response to clear
    """
    # Load existing responses
    responses = storage.load_responses()
    
    if 0 <= response_id < len(responses):
        # Remove the response at the specified index
        removed_response = responses.pop(response_id)
        
        # Save the updated responses back to the file
        with open(storage.STORAGE_FILE, 'w') as f:
            json.dump(responses, f, indent=2)
        
        scenario_id = removed_response.get("scenario_id", "Unknown")
        timestamp = removed_response.get("timestamp", "Unknown")
        
        print(f"Cleared response #{response_id+1} (Scenario {scenario_id}, {timestamp}).")
        print(f"Remaining responses: {len(responses)}")
    else:
        print(f"Response #{response_id+1} not found.")

def backup_database():
    """
    Create a backup of the current database before clearing it.
    """
    import datetime
    import shutil
    
    # Ensure the storage directory exists
    storage.ensure_storage_exists()
    
    # Create a backup filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(storage.STORAGE_DIR, f"ai_responses_backup_{timestamp}.json")
    
    # Copy the current database to the backup file
    if os.path.exists(storage.STORAGE_FILE):
        shutil.copy2(storage.STORAGE_FILE, backup_file)
        print(f"Database backup created: {backup_file}")
    else:
        print("No database file to backup.")

def main():
    parser = argparse.ArgumentParser(description="Clear the database of responses")
    parser.add_argument("--all", action="store_true", help="Clear all responses")
    parser.add_argument("--scenario", type=int, help="Clear responses for a specific scenario")
    parser.add_argument("--id", type=int, help="Clear a specific response by ID")
    parser.add_argument("--backup", action="store_true", help="Create a backup before clearing")
    
    args = parser.parse_args()
    
    # Create a backup if requested
    if args.backup:
        backup_database()
    
    # Clear responses based on the provided arguments
    if args.all:
        clear_all_responses()
    elif args.scenario is not None:
        clear_responses_by_scenario(args.scenario)
    elif args.id is not None:
        clear_response_by_id(args.id)
    else:
        # If no arguments provided, show the help message
        parser.print_help()
        
        # Also show the current response count
        response_count = storage.get_response_count()
        print(f"\nCurrent database has {response_count} responses.")
        print("Use one of the options above to clear responses.")

if __name__ == "__main__":
    main() 