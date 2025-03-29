#!/usr/bin/env python3
"""
Script to help fix import issues in the PhilAlignment codebase.
This script:
1. Copies key files to their reorganized locations
2. Adds import fallbacks to maintain compatibility
3. Updates import statements where possible
"""

import os
import sys
import re
import shutil
from pathlib import Path

# Define the root directory
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define module mappings (old location -> new location)
MODULE_MAPPINGS = {
    "multi_provider_integration.py": "providers/multi_provider_integration.py",
    "openai_integration.py": "providers/openai_integration.py",
    "question_generator.py": "generation/question_generator.py",
    "tester.py": "generation/tester.py",
    "validate_scenarios.py": "analysis/validate_scenarios.py",
    "compare_reasoning_approaches.py": "analysis/compare_reasoning_approaches.py",
    "run_toy_examples.py": "utils/run_toy_examples.py",
}

# Define directories to ensure
DIRECTORIES = [
    "code/core",
    "code/providers",
    "code/generation",
    "code/analysis",
    "code/utils",
    "code/visualization",
    "results",
    "plots"
]

def ensure_directories():
    """Ensure all required directories exist"""
    for directory in DIRECTORIES:
        os.makedirs(ROOT_DIR / directory, exist_ok=True)
        # Create __init__.py if it doesn't exist
        init_file = ROOT_DIR / directory / "__init__.py"
        if not init_file.exists():
            with open(init_file, "w") as f:
                f.write('"""PhilAlignment module."""\n')

def copy_files():
    """Copy files to their new locations"""
    code_dir = ROOT_DIR / "code"
    
    for source, target in MODULE_MAPPINGS.items():
        source_path = code_dir / source
        target_path = code_dir / target
        
        if source_path.exists():
            print(f"Copying {source} to {target}")
            shutil.copy2(source_path, target_path)
        else:
            print(f"Warning: Source file {source} not found")

def add_fallback_imports(file_path):
    """Add fallback imports to handle both old and new import structures"""
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found")
        return
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the file already has fallbacks
    if "try:" in content and "except ImportError:" in content:
        print(f"Skipping {file_path} as it already has fallback imports")
        return
    
    # Find import statements
    import_pattern = re.compile(r'^from ([\w\.]+) import (.+)$', re.MULTILINE)
    matches = list(import_pattern.finditer(content))
    
    if not matches:
        print(f"No imports found in {file_path}")
        return
    
    # Process imports in reverse order to avoid messing up line numbers
    for match in reversed(matches):
        module, imports = match.groups()
        
        # Skip certain imports
        if module.startswith(('os', 'sys', 'time', 're', 'json', 'matplotlib', 'numpy', 'pandas', 'collections')):
            continue
        
        # Create fallback import
        original_import = match.group(0)
        line_start = content[:match.start()].rfind('\n') + 1
        whitespace = content[line_start:match.start()]
        
        # Generate new import with fallback
        new_import = f"{whitespace}try:\n"
        new_import += f"{whitespace}    {original_import}\n"
        new_import += f"{whitespace}except ImportError:\n"
        
        # Create a modified version of the import for fallback
        if '.' in module:
            # For qualified imports, try the last part of the module
            module_parts = module.split('.')
            fallback_module = module_parts[-1]
            new_import += f"{whitespace}    # Fallback import\n"
            new_import += f"{whitespace}    try:\n"
            new_import += f"{whitespace}        from {fallback_module} import {imports}\n"
            new_import += f"{whitespace}    except ImportError:\n"
            new_import += f"{whitespace}        print(f\"Could not import {{{imports}}} from {module} or {fallback_module}\")\n"
        else:
            # For plain imports, try a different path
            if module in MODULE_MAPPINGS:
                new_module = "code." + MODULE_MAPPINGS[module].replace('.py', '').replace('/', '.')
                new_import += f"{whitespace}    # Fallback import\n"
                new_import += f"{whitespace}    try:\n"
                new_import += f"{whitespace}        from {new_module} import {imports}\n"
                new_import += f"{whitespace}    except ImportError:\n"
                new_import += f"{whitespace}        print(f\"Could not import {{{imports}}} from {module} or {new_module}\")\n"
            else:
                # If we don't know the new location, just try a different module path
                new_import += f"{whitespace}    # Fallback import\n"
                new_import += f"{whitespace}    try:\n"
                new_import += f"{whitespace}        from code.{module} import {imports}\n"
                new_import += f"{whitespace}    except ImportError:\n"
                new_import += f"{whitespace}        print(f\"Could not import {{{imports}}} from {module} or code.{module}\")\n"
        
        # Replace the original import with the new one
        content = content[:match.start()] + new_import + content[match.end():]
    
    # Write the modified content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Added fallback imports to {file_path}")

def fix_imports_in_directory(directory):
    """Add fallback imports to all Python files in a directory"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                add_fallback_imports(file_path)

def create_init_files():
    """Create __init__.py files for key modules"""
    
    # Create root __init__.py
    with open(ROOT_DIR / "code" / "__init__.py", "w") as f:
        f.write('"""PhilAlignment - A Framework for Analyzing Philosophical Alignment in AI Models"""\n\n')
        f.write('__version__ = "0.1.0"\n')
        f.write('__author__ = "PhilAlignment Team"\n\n')
        f.write('# Optional direct imports for convenience\n')
        f.write('# Uncomment these once the modules are properly refactored\n')
        f.write('# from code.core.philalignment import main\n')
        f.write('# from code.providers.multi_provider_integration import run_comparison, PROVIDERS, MODELS\n')
        f.write('# from code.generation.question_generator import generate_scenarios\n')
    
    print("Created/updated code/__init__.py")

def add_path_fix_to_scripts():
    """Add sys.path adjustments to key script files"""
    script_files = [
        ROOT_DIR / "code/providers/multi_provider_integration.py",
        ROOT_DIR / "code/analysis/compare_reasoning_approaches.py",
        ROOT_DIR / "code/generation/question_generator.py",
    ]
    
    path_adjustment = '\n# Ensure code directory is in the Python path\nimport sys, os\nsys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))\n\n'
    
    for file_path in script_files:
        if file_path.exists():
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if path adjustment is already there
            if "sys.path.append" not in content:
                # Find the position after imports
                first_import = content.find('import ')
                if first_import == -1:
                    # If no imports, add at the beginning
                    content = path_adjustment + content
                else:
                    # Find the end of the imports section
                    lines = content.split('\n')
                    in_imports = False
                    last_import_line = 0
                    
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            in_imports = True
                            last_import_line = i
                        elif in_imports and line.strip() and not line.startswith('#'):
                            in_imports = False
                            break
                    
                    # Insert after the imports
                    lines.insert(last_import_line + 1, path_adjustment)
                    content = '\n'.join(lines)
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"Added path adjustment to {file_path}")

def main():
    """Main function to run all fixes"""
    print("Starting PhilAlignment code refactoring...")
    
    print("\n1. Ensuring directories exist...")
    ensure_directories()
    
    print("\n2. Copying files to new locations...")
    copy_files()
    
    print("\n3. Creating/updating __init__.py files...")
    create_init_files()
    
    print("\n4. Adding path fixes to key scripts...")
    add_path_fix_to_scripts()
    
    print("\n5. Adding fallback imports to Python files...")
    fix_imports_in_directory(ROOT_DIR / "code/providers")
    fix_imports_in_directory(ROOT_DIR / "code/generation")
    fix_imports_in_directory(ROOT_DIR / "code/analysis")
    
    print("\nRefactoring complete!")
    print("You can now run your research using:")
    print("  ./compare_reasoning.py --provider openai --model gpt-4o --samples 3")
    print("or:")
    print("  ./philalignment.sh multi-provider --providers openai anthropic --reasoning standard cot induced_cot")

if __name__ == "__main__":
    main() 