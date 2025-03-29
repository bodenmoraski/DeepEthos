#!/usr/bin/env python3
"""
PhilAlignment - A Framework for Analyzing Philosophical Alignment in AI Models

This module serves as the central interface to the PhilAlignment framework,
providing access to scenario generation, validation, and analysis capabilities
across multiple LLM providers.
"""

import os
import sys
import argparse

# Ensure the code directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import main functionality from submodules
try:
    from code.generation.question_generator import generate_scenarios
    from code.generation.tester import test_generator
    from code.analysis.validate_scenarios import validate_scenarios
    from code.analysis.compare_reasoning_approaches import compare_reasoning_approaches
    from code.providers.multi_provider_integration import run_comparison, PROVIDERS, MODELS, REASONING_APPROACHES
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Falling back to direct imports...")
    try:
        from question_generator import generate_scenarios
        from tester import test_generator
        from validate_scenarios import validate_scenarios
        from compare_reasoning_approaches import compare_reasoning_approaches
        from multi_provider_integration import run_comparison, PROVIDERS, MODELS, REASONING_APPROACHES
    except ImportError as e:
        print(f"Failed to import modules: {e}")
        print("Please make sure all required modules are properly installed and accessible.")
        sys.exit(1)


def main():
    """
    Main entry point for the PhilAlignment framework.
    Provides a CLI interface to all main functionality.
    """
    parser = argparse.ArgumentParser(
        description="PhilAlignment - A framework for analyzing philosophical alignment in AI models"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate scenarios command
    gen_parser = subparsers.add_parser("generate", help="Generate philosophical test scenarios")
    gen_parser.add_argument("--num", type=int, default=25, help="Number of scenarios to generate")
    gen_parser.add_argument("--output", type=str, default="generated_moral_machine_scenarios.csv", 
                           help="Output file for generated scenarios")
    
    # Validate scenarios command
    val_parser = subparsers.add_parser("validate", help="Validate generated scenarios")
    val_parser.add_argument("--input", type=str, default="generated_moral_machine_scenarios.csv",
                           help="Input file containing scenarios to validate")
    val_parser.add_argument("--verbose", action="store_true", help="Print detailed validation information")
    
    # Compare reasoning approaches command
    comp_parser = subparsers.add_parser("compare-reasoning", 
                                       help="Compare different reasoning approaches with OpenAI models")
    comp_parser.add_argument("--model", type=str, default="gpt-4o", help="OpenAI model to use")
    comp_parser.add_argument("--samples", type=int, default=10, help="Number of scenarios to sample")
    comp_parser.add_argument("--categories", type=str, nargs="+", help="Categories to test")
    
    # Multi-provider comparison command
    multi_parser = subparsers.add_parser("multi-provider", 
                                       help="Compare philosophical alignment across multiple LLM providers")
    multi_parser.add_argument("--providers", type=str, nargs="+", choices=PROVIDERS.keys(),
                             default=list(PROVIDERS.keys()), help="LLM providers to use")
    multi_parser.add_argument("--models", type=str, nargs="+", 
                             help=f"Models to test. Available models: {', '.join(MODELS.keys())}")
    multi_parser.add_argument("--reasoning", type=str, nargs="+", choices=REASONING_APPROACHES,
                             default=["standard"], help="Reasoning approaches to test")
    multi_parser.add_argument("--samples", type=int, default=10, help="Number of scenarios to sample")
    multi_parser.add_argument("--max-tokens", type=int, default=2000, help="Maximum tokens for response generation")
    multi_parser.add_argument("--categories", type=str, nargs="+", help="Ethical categories to test")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        print(f"Generating {args.num} scenarios...")
        generate_scenarios(args.num, args.output)
        
    elif args.command == "validate":
        print(f"Validating scenarios in {args.input}...")
        validate_scenarios(args.input, args.verbose)
        
    elif args.command == "compare-reasoning":
        print(f"Comparing reasoning approaches with {args.model}...")
        compare_reasoning_approaches(
            model=args.model,
            num_samples=args.samples,
            categories=args.categories
        )
        
    elif args.command == "multi-provider":
        print(f"Running multi-provider comparison...")
        run_comparison(
            providers=args.providers,
            models=args.models,
            reasoning_types=args.reasoning,
            num_samples=args.samples,
            max_tokens=args.max_tokens,
            categories=args.categories
        )
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 