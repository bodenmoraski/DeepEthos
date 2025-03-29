#!/usr/bin/env python3
"""
Simple wrapper script to compare reasoning approaches
"""

import os
import sys
import argparse

def main():
    """Main function to run the comparison"""
    parser = argparse.ArgumentParser(
        description="Compare reasoning approaches for philosophical alignment"
    )
    
    parser.add_argument("--provider", type=str, default="openai", 
                        choices=["openai", "anthropic", "google"],
                        help="Provider to use for testing")
    parser.add_argument("--model", type=str, default="gpt-4o",
                        help="Model to use for testing")
    parser.add_argument("--samples", type=int, default=2,
                        help="Number of samples to test")
    parser.add_argument("--categories", type=str, nargs="+", 
                        default=["Species", "SocialValue"],
                        help="Categories to test")
    
    args = parser.parse_args()
    
    print(f"Starting comparison of reasoning approaches...")
    print(f"Provider: {args.provider}")
    print(f"Model: {args.model}")
    print(f"Samples: {args.samples}")
    print(f"Categories: {args.categories}")
    
    # Direct call to specific implementation
    if args.provider == "openai":
        try:
            from code.compare_reasoning_approaches import compare_reasoning_approaches
            compare_reasoning_approaches(
                model=args.model,
                num_samples=args.samples,
                categories=args.categories
            )
        except ImportError:
            print("Failed to import compare_reasoning_approaches. Make sure the file exists.")
            sys.exit(1)
    else:
        try:
            from code.multi_provider_integration import run_comparison
            run_comparison(
                providers=[args.provider],
                models=[args.model],
                reasoning_types=["standard", "cot", "induced_cot"],
                num_samples=args.samples,
                categories=args.categories
            )
        except ImportError:
            print("Failed to import multi_provider_integration. Make sure the file exists.")
            sys.exit(1)
    
    print("\nComparison completed.")

if __name__ == "__main__":
    main() 