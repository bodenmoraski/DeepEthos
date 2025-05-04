#!/usr/bin/env python3
"""
Analysis script for DeepEthos research results.
This script processes the JSON results file and generates:
1. Comparative analysis of reasoning approaches
2. Provider-specific performance metrics
3. Ethical decision patterns
4. Response complexity analysis
"""

import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from datetime import datetime
import argparse

def load_results(file_path):
    """Load the results JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def create_comparison_dataframe(results):
    """Create a pandas DataFrame for analysis"""
    data = []
    
    for provider, provider_data in results.items():
        for model, model_data in provider_data.items():
            for reasoning_type, rt_data in model_data.items():
                for scenario in rt_data['scenarios']:
                    if scenario['response'].startswith('[ERROR]'):
                        continue
                        
                    data.append({
                        'provider': provider,
                        'model': model,
                        'reasoning_type': reasoning_type,
                        'scenario_id': scenario['id'],
                        'word_count': scenario['analysis']['word_count'],
                        'reasoning_steps': scenario['analysis']['reasoning_steps'],
                        'decision': scenario['analysis']['decision'],
                        'contains_ethical_principles': scenario['analysis']['contains_ethical_principles'],
                        'ethical_principles_count': len(scenario['analysis']['ethical_principles']),
                        'contains_uncertainty': scenario['analysis']['contains_uncertainty']
                    })
    
    return pd.DataFrame(data)

def plot_reasoning_comparison(df, output_dir):
    """Create comparison plots for reasoning approaches"""
    plt.figure(figsize=(15, 10))
    
    # 1. Word Count Comparison
    plt.subplot(2, 2, 1)
    sns.boxplot(x='reasoning_type', y='word_count', hue='provider', data=df)
    plt.title('Response Length by Reasoning Approach')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 2. Reasoning Steps Comparison
    plt.subplot(2, 2, 2)
    sns.boxplot(x='reasoning_type', y='reasoning_steps', hue='provider', data=df)
    plt.title('Reasoning Steps by Approach')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 3. Ethical Principles Mentioned
    plt.subplot(2, 2, 3)
    ethical_counts = df.groupby(['provider', 'reasoning_type'])['ethical_principles_count'].mean().unstack()
    ethical_counts.plot(kind='bar')
    plt.title('Average Ethical Principles Mentioned')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 4. Decision Distribution
    plt.subplot(2, 2, 4)
    decision_counts = df.groupby(['provider', 'reasoning_type', 'decision']).size().unstack()
    decision_counts.plot(kind='bar', stacked=True)
    plt.title('Decision Distribution by Approach')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, 'reasoning_comparison.png'))
    plt.close()

def plot_provider_specific_analysis(df, output_dir):
    """Create provider-specific analysis plots"""
    for provider in df['provider'].unique():
        provider_df = df[df['provider'] == provider]
        
        plt.figure(figsize=(15, 10))
        
        # 1. Model Performance Comparison
        plt.subplot(2, 2, 1)
        sns.boxplot(x='model', y='word_count', hue='reasoning_type', data=provider_df)
        plt.title(f'{provider} - Response Length by Model')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 2. Reasoning Steps by Model
        plt.subplot(2, 2, 2)
        sns.boxplot(x='model', y='reasoning_steps', hue='reasoning_type', data=provider_df)
        plt.title(f'{provider} - Reasoning Steps by Model')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 3. Decision Patterns
        plt.subplot(2, 2, 3)
        decision_matrix = provider_df.groupby(['model', 'reasoning_type', 'decision']).size().unstack()
        decision_matrix.plot(kind='bar', stacked=True)
        plt.title(f'{provider} - Decision Patterns')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 4. Ethical Principles Analysis
        plt.subplot(2, 2, 4)
        ethical_matrix = provider_df.groupby(['model', 'reasoning_type'])['ethical_principles_count'].mean().unstack()
        ethical_matrix.plot(kind='bar')
        plt.title(f'{provider} - Ethical Principles Mentioned')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(os.path.join(output_dir, f'{provider}_analysis.png'))
        plt.close()

def generate_statistical_summary(df, output_dir):
    """Generate statistical summary of the results"""
    def convert_keys_to_strings(d):
        """Recursively convert tuple keys to strings"""
        if isinstance(d, dict):
            return {str(k): convert_keys_to_strings(v) for k, v in d.items()}
        elif isinstance(d, (list, tuple)):
            return [convert_keys_to_strings(x) for x in d]
        else:
            return d

    # Get statistics
    overall_stats = df.describe().to_dict()
    provider_stats = df.groupby('provider').describe().to_dict()
    reasoning_stats = df.groupby('reasoning_type').describe().to_dict()
    
    # Convert decision distribution to a more JSON-friendly format
    decision_dist = {}
    for (provider, reasoning, decision), count in df.groupby(['provider', 'reasoning_type', 'decision']).size().items():
        if provider not in decision_dist:
            decision_dist[provider] = {}
        if reasoning not in decision_dist[provider]:
            decision_dist[provider][reasoning] = {}
        decision_dist[provider][reasoning][decision] = int(count)
    
    # Convert ethical principles to a more JSON-friendly format
    ethical_principles = {}
    for (provider, reasoning), count in df.groupby(['provider', 'reasoning_type'])['ethical_principles_count'].mean().items():
        if provider not in ethical_principles:
            ethical_principles[provider] = {}
        ethical_principles[provider][reasoning] = float(count)
    
    summary = {
        'Overall Statistics': convert_keys_to_strings(overall_stats),
        'By Provider': convert_keys_to_strings(provider_stats),
        'By Reasoning Type': convert_keys_to_strings(reasoning_stats),
        'Decision Distribution': decision_dist,
        'Ethical Principles': ethical_principles
    }
    
    with open(os.path.join(output_dir, 'statistical_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

def create_heatmap_visualizations(df, output_dir):
    """Create heatmap visualizations for complex relationships"""
    # 1. Provider vs Reasoning Type heatmap for word count
    plt.figure(figsize=(10, 8))
    word_count_heatmap = df.pivot_table(
        values='word_count',
        index='provider',
        columns='reasoning_type',
        aggfunc='mean'
    )
    sns.heatmap(word_count_heatmap, annot=True, cmap='YlOrRd')
    plt.title('Average Word Count by Provider and Reasoning Type')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'word_count_heatmap.png'))
    plt.close()
    
    # 2. Provider vs Reasoning Type heatmap for reasoning steps
    plt.figure(figsize=(10, 8))
    steps_heatmap = df.pivot_table(
        values='reasoning_steps',
        index='provider',
        columns='reasoning_type',
        aggfunc='mean'
    )
    sns.heatmap(steps_heatmap, annot=True, cmap='YlOrRd')
    plt.title('Average Reasoning Steps by Provider and Reasoning Type')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'reasoning_steps_heatmap.png'))
    plt.close()

def analyze_ethical_alignment(df, output_dir):
    """Analyze and visualize ethical alignment patterns"""
    # Define ethical frameworks and their keywords
    ethical_frameworks = {
        'utilitarian': ['utility', 'greatest good', 'happiness', 'consequences', 'benefit', 'harm'],
        'deontological': ['duty', 'right', 'wrong', 'rule', 'principle', 'obligation', 'categorical imperative'],
        'virtue_ethics': ['virtue', 'character', 'excellence', 'moral', 'integrity', 'wisdom'],
        'care_ethics': ['care', 'relationship', 'compassion', 'empathy', 'connection'],
        'rights_based': ['rights', 'freedom', 'liberty', 'autonomy', 'dignity'],
        'justice_based': ['justice', 'fairness', 'equality', 'equity', 'distribution']
    }
    
    # Create a new column for ethical framework
    df['ethical_framework'] = 'other'
    
    # Analyze each response for ethical frameworks
    for idx, row in df.iterrows():
        response = row['response'].lower()
        frameworks_found = []
        
        for framework, keywords in ethical_frameworks.items():
            if any(keyword in response for keyword in keywords):
                frameworks_found.append(framework)
        
        if frameworks_found:
            df.at[idx, 'ethical_framework'] = frameworks_found[0]  # Take the first matching framework
    
    # Create ethical alignment visualizations
    plt.figure(figsize=(15, 10))
    
    # 1. Framework Distribution by Provider
    plt.subplot(2, 2, 1)
    framework_counts = df.groupby(['provider', 'ethical_framework']).size().unstack()
    framework_counts.plot(kind='bar', stacked=True)
    plt.title('Ethical Framework Distribution by Provider')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 2. Framework Distribution by Reasoning Type
    plt.subplot(2, 2, 2)
    reasoning_frameworks = df.groupby(['reasoning_type', 'ethical_framework']).size().unstack()
    reasoning_frameworks.plot(kind='bar', stacked=True)
    plt.title('Ethical Framework Distribution by Reasoning Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 3. Framework vs Decision Heatmap
    plt.subplot(2, 2, 3)
    framework_decision = pd.crosstab(df['ethical_framework'], df['decision'])
    sns.heatmap(framework_decision, annot=True, cmap='YlOrRd')
    plt.title('Ethical Framework vs Decision')
    plt.tight_layout()
    
    # 4. Framework vs Reasoning Steps
    plt.subplot(2, 2, 4)
    sns.boxplot(x='ethical_framework', y='reasoning_steps', data=df)
    plt.title('Reasoning Steps by Ethical Framework')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, 'ethical_alignment_analysis.png'))
    plt.close()
    
    # Convert groupby results to nested dictionaries for JSON serialization
    def convert_groupby_to_dict(groupby_result):
        result = {}
        for key, value in groupby_result.items():
            if isinstance(key, tuple):
                # Convert tuple key to string key
                str_key = '_'.join(str(k) for k in key)
                result[str_key] = int(value) if isinstance(value, (int, np.integer)) else float(value)
            else:
                result[str(key)] = int(value) if isinstance(value, (int, np.integer)) else float(value)
        return result
    
    # Generate detailed ethical alignment statistics
    alignment_stats = {
        'framework_distribution': convert_groupby_to_dict(df['ethical_framework'].value_counts()),
        'provider_framework_distribution': convert_groupby_to_dict(df.groupby(['provider', 'ethical_framework']).size()),
        'reasoning_framework_distribution': convert_groupby_to_dict(df.groupby(['reasoning_type', 'ethical_framework']).size()),
        'framework_decision_correlation': framework_decision.to_dict(),
        'average_reasoning_steps': convert_groupby_to_dict(df.groupby('ethical_framework')['reasoning_steps'].mean())
    }
    
    with open(os.path.join(output_dir, 'ethical_alignment_stats.json'), 'w') as f:
        json.dump(alignment_stats, f, indent=2)
    
    return df

def main():
    parser = argparse.ArgumentParser(description='Analyze DeepEthos research results')
    parser.add_argument('--results', required=True, help='Path to results JSON file')
    parser.add_argument('--output', default='analysis_results', help='Output directory for analysis results')
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Load results
    print("Loading results...")
    results = load_results(args.results)
    
    # Create analysis DataFrame
    print("Creating analysis DataFrame...")
    df = create_comparison_dataframe(results)
    
    # Add response text to DataFrame
    df['response'] = df.apply(lambda row: results[row['provider']][row['model']][row['reasoning_type']]['scenarios'][row['scenario_id']]['response'], axis=1)
    
    # Generate visualizations
    print("Generating visualizations...")
    plot_reasoning_comparison(df, args.output)
    plot_provider_specific_analysis(df, args.output)
    create_heatmap_visualizations(df, args.output)
    
    # Analyze ethical alignment
    print("Analyzing ethical alignment...")
    df = analyze_ethical_alignment(df, args.output)
    
    # Generate statistical summary
    print("Generating statistical summary...")
    generate_statistical_summary(df, args.output)
    
    print(f"Analysis complete! Results saved in {args.output}")

if __name__ == "__main__":
    main() 