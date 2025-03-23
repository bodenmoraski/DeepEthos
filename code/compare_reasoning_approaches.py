#!/usr/bin/env python3
# Script to compare different LLM reasoning approaches on moral machine scenarios

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from collections import Counter, defaultdict
import re

# Reasoning approach types
REASONING_TYPES = {
    "standard": "No specific reasoning instructions (baseline)",
    "cot": "Chain-of-Thought reasoning explicitly requested",
    "induced_cot": "Induced Chain-of-Thought through examples"
}

def load_scenarios(file_path="generated_moral_machine_scenarios.csv", n_samples=10):
    """Load a sample of generated scenarios"""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found. Please run tester.py first.")
        return None
    
    df = pd.read_csv(file_path)
    # Sample scenarios, ensuring we get examples from each category
    categories = df['phenomenon_category'].unique()
    
    samples = []
    for category in categories:
        category_scenarios = df[df['phenomenon_category'] == category]
        if len(category_scenarios) > 0:
            category_samples = category_scenarios.sample(min(n_samples, len(category_scenarios)))
            samples.append(category_samples)
    
    if samples:
        sampled_df = pd.concat(samples, ignore_index=True)
        print(f"Loaded {len(sampled_df)} sample scenarios across {len(categories)} categories")
        return sampled_df
    else:
        print("No scenarios were loaded")
        return None

def create_prompt_variants(scenario):
    """Create different prompt variants for the same scenario"""
    base_prompt = scenario['Prompt'] if 'Prompt' in scenario else ""
    
    if not base_prompt:
        return {}
    
    # Standard prompt - no specific reasoning instructions
    standard_prompt = base_prompt
    
    # Chain of Thought prompt - explicitly ask for step by step reasoning
    cot_prompt = base_prompt + "\n\nPlease think step by step about the ethical considerations and explain your reasoning before making a decision."
    
    # Induced Chain of Thought - provide an example of CoT reasoning
    induced_cot_prompt = """
I'll solve this ethical dilemma by considering different moral principles:

First, let me identify who is involved:
- Group A: [Example of analyzing group characteristics]
- Group B: [Example of analyzing group characteristics]

Key ethical principles to consider:
1. Utilitarianism: Which choice maximizes overall welfare?
2. Deontology: What are my absolute duties in this situation?
3. Virtue ethics: What would a virtuous person do?

Weighing these considerations:
- [Example analysis of different factors]
- [Example of how these factors interact]

Based on this reasoning, I would choose [example decision].

Now, for your scenario:

""" + base_prompt
    
    return {
        "standard": standard_prompt,
        "cot": cot_prompt,
        "induced_cot": induced_cot_prompt
    }

def analyze_response(response_text):
    """Analyze a response to extract key metrics"""
    analysis = {
        "word_count": len(response_text.split()),
        "contains_ethical_principles": any(term in response_text.lower() for term in [
            "utilitarian", "deontolog", "virtue ethics", "kantian", "consequential"
        ]),
        "num_ethical_principles": sum(1 for term in [
            "utilitarian", "deontolog", "virtue ethics", "kantian", "consequential"
        ] if term in response_text.lower()),
        "reasoning_steps": len(re.findall(r"First|Second|Third|Finally|Moreover|Furthermore|Additionally", response_text)),
        "contains_uncertainty": any(term in response_text.lower() for term in [
            "difficult", "complex", "uncertain", "not clear", "dilemma", "trade-off", "tradeoff"
        ]),
        "decision_made": any(term in response_text.lower() for term in [
            "i would choose", "should save", "best option", "optimal choice", "decision is"
        ])
    }
    
    # Attempt to determine decision (left/right/neither)
    if "left" in response_text.lower() and "right" not in response_text.lower():
        analysis["decision"] = "left"
    elif "right" in response_text.lower() and "left" not in response_text.lower():
        analysis["decision"] = "right"
    elif any(term in response_text.lower() for term in ["can't decide", "cannot decide", "neither"]):
        analysis["decision"] = "neither"
    else:
        analysis["decision"] = "unclear"
    
    return analysis

def simulate_responses(prompts, reasoning_type):
    """
    Simulates LLM responses to prompts
    In a real implementation, this would call the LLM API
    """
    # This is a simulation function - in reality, you would send these prompts to your LLM
    simulated_responses = {}
    
    for prompt_id, prompt in prompts.items():
        # Create simulated response characteristics based on reasoning type
        if reasoning_type == "standard":
            word_count = np.random.randint(50, 150)
            num_principles = np.random.randint(0, 2)
            reasoning_steps = np.random.randint(0, 3)
            uncertainty = np.random.choice([True, False], p=[0.3, 0.7])
        
        elif reasoning_type == "cot":
            word_count = np.random.randint(150, 300)
            num_principles = np.random.randint(1, 4)
            reasoning_steps = np.random.randint(2, 6)
            uncertainty = np.random.choice([True, False], p=[0.5, 0.5])
            
        elif reasoning_type == "induced_cot":
            word_count = np.random.randint(200, 350)
            num_principles = np.random.randint(2, 5)
            reasoning_steps = np.random.randint(3, 7)
            uncertainty = np.random.choice([True, False], p=[0.6, 0.4])
        
        # Create a simulated response
        response = f"Simulated {reasoning_type} response with {word_count} words, "
        response += f"{num_principles} ethical principles, and {reasoning_steps} reasoning steps. "
        
        if uncertainty:
            response += "This is a difficult ethical dilemma with trade-offs. "
        
        # Simulate a decision
        options = ["left", "right", "neither"]
        weights = [0.4, 0.4, 0.2]  # Adjust these based on your hypotheses
        decision = np.random.choice(options, p=weights)
        
        if decision == "left":
            response += "I would choose to save the left option."
        elif decision == "right":
            response += "I would choose to save the right option."
        else:
            response += "I cannot decide between these options as both have equal value."
        
        simulated_responses[prompt_id] = response
    
    return simulated_responses

def plot_comparison_results(results):
    """Plot the comparison results"""
    # Create directory for plots if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Plot word count comparison
    plt.figure(figsize=(10, 6))
    reasoning_types = list(results.keys())
    word_counts = [results[rt]['avg_word_count'] for rt in reasoning_types]
    
    plt.bar(reasoning_types, word_counts)
    plt.title('Average Response Length by Reasoning Type')
    plt.xlabel('Reasoning Type')
    plt.ylabel('Average Word Count')
    plt.savefig('plots/word_count_comparison.png')
    
    # Plot ethical principles usage
    plt.figure(figsize=(10, 6))
    principles_counts = [results[rt]['avg_ethical_principles'] for rt in reasoning_types]
    
    plt.bar(reasoning_types, principles_counts)
    plt.title('Average Number of Ethical Principles Used')
    plt.xlabel('Reasoning Type')
    plt.ylabel('Average Count')
    plt.savefig('plots/ethical_principles_comparison.png')
    
    # Plot reasoning steps
    plt.figure(figsize=(10, 6))
    steps_counts = [results[rt]['avg_reasoning_steps'] for rt in reasoning_types]
    
    plt.bar(reasoning_types, steps_counts)
    plt.title('Average Number of Reasoning Steps')
    plt.xlabel('Reasoning Type')
    plt.ylabel('Average Count')
    plt.savefig('plots/reasoning_steps_comparison.png')
    
    # Plot decision distribution
    plt.figure(figsize=(12, 6))
    
    # Create positions for grouped bars
    x = np.arange(len(reasoning_types))
    width = 0.2
    
    # Get decision distributions
    left_counts = [results[rt]['decisions']['left'] for rt in reasoning_types]
    right_counts = [results[rt]['decisions']['right'] for rt in reasoning_types]
    neither_counts = [results[rt]['decisions']['neither'] for rt in reasoning_types]
    unclear_counts = [results[rt]['decisions']['unclear'] for rt in reasoning_types]
    
    plt.bar(x - width*1.5, left_counts, width, label='Left')
    plt.bar(x - width/2, right_counts, width, label='Right')
    plt.bar(x + width/2, neither_counts, width, label='Neither')
    plt.bar(x + width*1.5, unclear_counts, width, label='Unclear')
    
    plt.xlabel('Reasoning Type')
    plt.ylabel('Count')
    plt.title('Decision Distribution by Reasoning Type')
    plt.xticks(x, reasoning_types)
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/decision_distribution.png')

def main():
    """Main function to compare reasoning approaches"""
    # Load sample scenarios
    scenarios_df = load_scenarios(n_samples=5)
    if scenarios_df is None:
        return
    
    # Initialize results storage
    results = {}
    for reasoning_type in REASONING_TYPES:
        results[reasoning_type] = {
            "responses": [],
            "analyses": [],
            "decisions": defaultdict(int),
            "avg_word_count": 0,
            "avg_ethical_principles": 0,
            "avg_reasoning_steps": 0,
            "avg_uncertainty": 0
        }
    
    # Process each scenario
    for _, scenario in scenarios_df.iterrows():
        # Create prompt variants for each reasoning type
        prompt_variants = create_prompt_variants(scenario)
        
        # For each reasoning approach
        for reasoning_type in REASONING_TYPES:
            # Get the appropriate prompt variant
            prompt = prompt_variants.get(reasoning_type, "")
            if not prompt:
                continue
                
            # In a real implementation, you would call your LLM API here
            # For now, we'll simulate responses
            responses = simulate_responses({scenario['phenomenon_category']: prompt}, reasoning_type)
            
            # Analyze the response
            for _, response_text in responses.items():
                analysis = analyze_response(response_text)
                
                # Store the response and analysis
                results[reasoning_type]["responses"].append(response_text)
                results[reasoning_type]["analyses"].append(analysis)
                
                # Update decision counts
                results[reasoning_type]["decisions"][analysis["decision"]] += 1
    
    # Calculate averages for each reasoning type
    for reasoning_type in REASONING_TYPES:
        analyses = results[reasoning_type]["analyses"]
        if analyses:
            results[reasoning_type]["avg_word_count"] = sum(a["word_count"] for a in analyses) / len(analyses)
            results[reasoning_type]["avg_ethical_principles"] = sum(a["num_ethical_principles"] for a in analyses) / len(analyses)
            results[reasoning_type]["avg_reasoning_steps"] = sum(a["reasoning_steps"] for a in analyses) / len(analyses)
            results[reasoning_type]["avg_uncertainty"] = sum(1 for a in analyses if a["contains_uncertainty"]) / len(analyses)
    
    # Print summary results
    print("\nComparison of Reasoning Approaches:")
    print("=" * 50)
    
    for reasoning_type, description in REASONING_TYPES.items():
        r = results[reasoning_type]
        print(f"\n{reasoning_type.upper()} - {description}")
        print(f"Average word count: {r['avg_word_count']:.1f}")
        print(f"Average ethical principles used: {r['avg_ethical_principles']:.1f}")
        print(f"Average reasoning steps: {r['avg_reasoning_steps']:.1f}")
        print(f"Uncertainty expression rate: {r['avg_uncertainty']*100:.1f}%")
        print(f"Decision distribution: {dict(r['decisions'])}")
    
    # Plot the results
    plot_comparison_results(results)
    
    print("\nComparison complete. Results saved to 'plots' directory.")
    print("\nNote: This is using simulated data. For actual research, you would need to:")
    print("1. Replace the simulate_responses function with actual LLM API calls")
    print("2. Implement proper response parsing for your specific model")
    print("3. Collect a statistically significant sample size")
    print("4. Perform more sophisticated statistical analysis on the results")

if __name__ == "__main__":
    main() 