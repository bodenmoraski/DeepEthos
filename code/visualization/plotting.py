"""
Visualization functions for the PhilAlignment framework.
Provides tools for creating comparative plots and visualizing analysis results.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import sys

# Ensure code directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from code.utils.common import ensure_dir
except ImportError:
    # Fallback import
    def ensure_dir(directory):
        """Ensure a directory exists, creating it if necessary."""
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

# Set the style for all plots
try:
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("muted")
except:
    print("Warning: Could not set preferred style, using default style.")

def create_model_comparison_plot(data, metric, title=None, filename=None, figsize=(12, 8)):
    """
    Create a comparison bar plot for various models and providers.
    
    Args:
        data (dict): Nested dictionary with format: {provider: {model: {metric: value}}}
        metric (str): The metric to plot (e.g., 'word_count', 'reasoning_steps')
        title (str, optional): Plot title
        filename (str, optional): Output filename
        figsize (tuple, optional): Figure size
    
    Returns:
        str: Path to the saved plot if filename is provided, else None
    """
    # Prepare data for plotting
    providers = []
    models = []
    values = []
    
    for provider, provider_data in data.items():
        for model, model_data in provider_data.items():
            if metric in model_data:
                providers.append(provider)
                models.append(model)
                values.append(model_data[metric])
    
    # Create DataFrame for plotting
    df = pd.DataFrame({
        'Provider': providers,
        'Model': models,
        metric: values
    })
    
    # Plot
    plt.figure(figsize=figsize)
    ax = sns.barplot(x='Model', y=metric, hue='Provider', data=df)
    
    # Customize
    if title:
        plt.title(title, fontsize=16)
    else:
        plt.title(f'Comparison of {metric} across models and providers', fontsize=16)
    
    plt.xlabel('Model', fontsize=14)
    plt.ylabel(metric.replace('_', ' ').title(), fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Provider')
    plt.tight_layout()
    
    # Save if filename provided
    if filename:
        plots_dir = ensure_dir("plots")
        output_path = os.path.join(plots_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return output_path
    
    return None

def create_heatmap(data, x_labels, y_labels, title, filename=None, figsize=(12, 10), cmap="YlOrRd"):
    """
    Create a heatmap visualization.
    
    Args:
        data (numpy.ndarray): 2D array of values for the heatmap
        x_labels (list): Labels for the x-axis
        y_labels (list): Labels for the y-axis
        title (str): Plot title
        filename (str, optional): Output filename
        figsize (tuple, optional): Figure size
        cmap (str, optional): Colormap for the heatmap
    
    Returns:
        str: Path to the saved plot if filename is provided, else None
    """
    plt.figure(figsize=figsize)
    ax = sns.heatmap(data, annot=True, fmt=".2f", cmap=cmap, 
                    xticklabels=x_labels, yticklabels=y_labels)
    
    plt.title(title, fontsize=16)
    plt.tight_layout()
    
    # Save if filename provided
    if filename:
        plots_dir = ensure_dir("plots")
        output_path = os.path.join(plots_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return output_path
    
    return None

def create_reasoning_comparison_plot(data, title=None, filename=None, figsize=(12, 8)):
    """
    Create a grouped bar plot comparing reasoning approaches across models.
    
    Args:
        data (dict): Nested dictionary with format: 
                    {model: {reasoning_approach: value}}
        title (str, optional): Plot title
        filename (str, optional): Output filename
        figsize (tuple, optional): Figure size
    
    Returns:
        str: Path to the saved plot if filename is provided, else None
    """
    # Prepare data for plotting
    df = pd.DataFrame(data).T.reset_index()
    df = df.rename(columns={'index': 'Model'})
    
    # Melt the DataFrame for easier plotting
    df_melted = pd.melt(df, id_vars=['Model'], var_name='Reasoning Approach', value_name='Value')
    
    # Plot
    plt.figure(figsize=figsize)
    ax = sns.barplot(x='Model', y='Value', hue='Reasoning Approach', data=df_melted)
    
    # Customize
    if title:
        plt.title(title, fontsize=16)
    else:
        plt.title('Comparison of Reasoning Approaches Across Models', fontsize=16)
    
    plt.xlabel('Model', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Reasoning Approach')
    plt.tight_layout()
    
    # Save if filename provided
    if filename:
        plots_dir = ensure_dir("plots")
        output_path = os.path.join(plots_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return output_path
    
    return None

def create_category_comparison_plot(data, categories, providers=None, title=None, filename=None, figsize=(14, 8)):
    """
    Create a grouped bar plot comparing performance across ethical categories.
    
    Args:
        data (dict): Nested dictionary with format: 
                    {provider: {category: value}}
        categories (list): List of ethical categories to include
        providers (list, optional): Specific providers to include
        title (str, optional): Plot title
        filename (str, optional): Output filename
        figsize (tuple, optional): Figure size
    
    Returns:
        str: Path to the saved plot if filename is provided, else None
    """
    # Filter data if providers specified
    if providers:
        data = {p: data[p] for p in providers if p in data}
    
    # Prepare data for plotting
    plot_data = []
    
    for provider, provider_data in data.items():
        for category in categories:
            if category in provider_data:
                plot_data.append({
                    'Provider': provider,
                    'Category': category,
                    'Value': provider_data[category]
                })
    
    df = pd.DataFrame(plot_data)
    
    # Plot
    plt.figure(figsize=figsize)
    ax = sns.barplot(x='Category', y='Value', hue='Provider', data=df)
    
    # Customize
    if title:
        plt.title(title, fontsize=16)
    else:
        plt.title('Comparison Across Ethical Categories', fontsize=16)
    
    plt.xlabel('Ethical Category', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.xticks(rotation=30, ha='right')
    plt.legend(title='Provider')
    plt.tight_layout()
    
    # Save if filename provided
    if filename:
        plots_dir = ensure_dir("plots")
        output_path = os.path.join(plots_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return output_path
    
    return None 