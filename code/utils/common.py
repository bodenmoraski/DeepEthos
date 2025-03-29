"""
Common utility functions used across the PhilAlignment framework.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def ensure_dir(directory):
    """
    Ensure a directory exists, creating it if necessary.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def load_scenarios(file_path, num_samples=None, categories=None):
    """
    Load scenarios from a CSV file, optionally filtering by category and limiting to a sample.
    
    Args:
        file_path (str): Path to the CSV file containing scenarios
        num_samples (int, optional): Number of scenarios to sample
        categories (list, optional): List of ethical categories to filter by
        
    Returns:
        pandas.DataFrame: Loaded and filtered scenarios
    """
    try:
        df = pd.read_csv(file_path)
        # Filter by categories if specified
        if categories:
            df = df[df['ethical_category'].isin(categories)]
        
        # Sample if specified
        if num_samples and num_samples < len(df):
            df = df.sample(num_samples, random_state=42)
            
        return df
    except Exception as e:
        print(f"Error loading scenarios: {e}")
        return pd.DataFrame()

def save_results(results, filename_prefix, provider_name=None, model_name=None):
    """
    Save results to a JSON file with a timestamp.
    
    Args:
        results (dict): Results to save
        filename_prefix (str): Prefix for the filename
        provider_name (str, optional): Provider name to include in the filename
        model_name (str, optional): Model name to include in the filename
        
    Returns:
        str: Path to the saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create results directory if it doesn't exist
    results_dir = ensure_dir("results")
    
    # Build filename
    components = [filename_prefix]
    if provider_name:
        components.append(provider_name)
    if model_name:
        components.append(model_name)
    components.append(timestamp)
    
    filename = f"{results_dir}/{'-'.join(components)}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {filename}")
    return filename

def plot_comparison(data, title, x_label, y_label, filename, figsize=(10, 6)):
    """
    Create a bar plot for comparison data.
    
    Args:
        data (dict): Data to plot (keys are x-axis labels, values are y-axis values)
        title (str): Plot title
        x_label (str): X-axis label
        y_label (str): Y-axis label
        filename (str): Output filename
        figsize (tuple, optional): Figure size
    """
    # Create plots directory if it doesn't exist
    plots_dir = ensure_dir("plots")
    
    plt.figure(figsize=figsize)
    plt.bar(data.keys(), data.values())
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = f"{plots_dir}/{filename}"
    plt.savefig(output_path)
    plt.close()
    
    print(f"Plot saved to {output_path}")
    return output_path 