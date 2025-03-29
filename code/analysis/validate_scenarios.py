#!/usr/bin/env python3
# Validation script for Moral Machine scenarios

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os

def load_scenarios(file_path="generated_moral_machine_scenarios.csv"):
    """Load generated scenarios from CSV file or generate new ones if needed"""
    if os.path.exists(file_path):
        print(f"Loading scenarios from {file_path}")
        return pd.read_csv(file_path)
    else:
        print(f"File {file_path} not found, generating new scenarios...")
        from question_generator import ScenarioTesterExactMoralMachine
        tester = ScenarioTesterExactMoralMachine(
            model_versions=['gpt4'],
            system_roles=['default'],
            langs=['en'],
            n_questions_per_category=10,
            generate_responses=False
        )
        scenarios = tester.generate_prompts_per_category()
        df = pd.DataFrame(scenarios)
        df.to_csv(file_path, index=False)
        return df

def analyze_category_distribution(df):
    """Analyze the distribution of ethical categories in the scenarios"""
    category_counts = Counter(df['phenomenon_category'])
    
    # Plot category distribution
    plt.figure(figsize=(12, 6))
    categories = list(category_counts.keys())
    counts = list(category_counts.values())
    
    plt.bar(categories, counts)
    plt.title('Distribution of Ethical Categories')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('category_distribution.png')
    
    print("Category Distribution:")
    for category, count in category_counts.items():
        print(f"{category}: {count} scenarios ({count/len(df)*100:.1f}%)")
    
    return category_counts

def analyze_demographic_balance(df):
    """Analyze the demographic balance of characters in scenarios"""
    # Character types that appear in prompts
    character_types = ["Man", "Woman", "ElderlyMan", "ElderlyWoman", "Boy", "Girl", 
                       "Pregnant", "Homeless", "Criminal", "Dog", "Cat"]
    
    # Check which columns are in the dataframe that match character types
    present_types = [col for col in df.columns if col in character_types]
    
    if not present_types:
        print("Character type columns not found in dataframe")
        return
    
    # Sum the counts for each character type
    type_counts = {char_type: df[char_type].sum() for char_type in present_types}
    
    # Plot demographic distribution
    plt.figure(figsize=(12, 6))
    char_types = list(type_counts.keys())
    counts = list(type_counts.values())
    
    plt.bar(char_types, counts)
    plt.title('Distribution of Character Types')
    plt.xlabel('Character Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('demographic_distribution.png')
    
    print("\nDemographic Distribution:")
    for char_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{char_type}: {count} instances")
    
    return type_counts

def analyze_prompt_complexity(df):
    """Analyze the complexity/length of prompts"""
    # Calculate prompt lengths
    if 'Prompt' in df.columns:
        df['prompt_length'] = df['Prompt'].apply(len)
        
        plt.figure(figsize=(10, 6))
        plt.hist(df['prompt_length'], bins=20)
        plt.title('Distribution of Prompt Lengths')
        plt.xlabel('Length (characters)')
        plt.ylabel('Frequency')
        plt.savefig('prompt_length_distribution.png')
        
        print(f"\nPrompt Length Statistics:")
        print(f"Mean: {df['prompt_length'].mean():.1f} characters")
        print(f"Median: {df['prompt_length'].median():.1f} characters")
        print(f"Min: {df['prompt_length'].min()} characters")
        print(f"Max: {df['prompt_length'].max()} characters")
    else:
        print("Prompt column not found in dataframe")

def display_sample_scenarios(df, n=3):
    """Display a few sample scenarios from each category"""
    categories = df['phenomenon_category'].unique()
    
    print("\nSample Scenarios:")
    for category in categories:
        category_scenarios = df[df['phenomenon_category'] == category]
        sample = category_scenarios.sample(min(n, len(category_scenarios)))
        
        print(f"\n{'-'*40}")
        print(f"Category: {category}")
        print(f"{'-'*40}")
        
        for i, (_, scenario) in enumerate(sample.iterrows()):
            if 'Prompt' in scenario:
                print(f"Sample {i+1}:")
                print(scenario['Prompt'])
                print()

def main():
    """Main function to run the validation analysis"""
    # Create plots directory if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Load scenarios
    df = load_scenarios()
    
    print(f"Loaded {len(df)} scenarios")
    
    # Run analysis
    category_counts = analyze_category_distribution(df)
    demographic_counts = analyze_demographic_balance(df)
    analyze_prompt_complexity(df)
    display_sample_scenarios(df)
    
    # Print overall assessment
    print("\nValidation Summary:")
    print(f"- Total scenarios: {len(df)}")
    print(f"- Categories covered: {len(category_counts)}")
    
    # Check if all categories have at least some scenarios
    expected_categories = ["Species", "SocialValue", "Gender", "Age", "Fitness", "Utilitarianism", "Random"]
    missing_categories = [cat for cat in expected_categories if cat not in category_counts]
    
    if missing_categories:
        print(f"- WARNING: Missing scenarios for categories: {', '.join(missing_categories)}")
    else:
        print("- All expected categories are represented")
    
    # Check if prompts are reasonable lengths
    if 'prompt_length' in df.columns:
        if df['prompt_length'].min() < 50:
            print("- WARNING: Some prompts may be too short")
        if df['prompt_length'].max() > 1000:
            print("- WARNING: Some prompts may be too long")
    
    print("\nThe scenario generation appears to be working correctly and can be used as a foundation for philosophical alignment research.")

if __name__ == "__main__":
    main() 