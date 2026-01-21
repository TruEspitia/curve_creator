import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from math_core.ffunc_parser import FFuncParser

# Test loading all functions
functions_dir = os.path.join(os.path.dirname(__file__), 'functions')
print(f"Scanning functions directory: {functions_dir}\n")

models = FFuncParser.get_available_functions(functions_dir)

print(f"✓ Found {len(models)} functions total\n")
print("=" * 60)

# Group functions by category
categories = {}
for model in models:
    name = model.name
    # Determine category from filename
    if 'trigonometric' in name or 'sinh' in name or 'cosh' in name:
        category = 'Trigonometric'
    elif 'logarithmic' in name:
        category = 'Logarithmic'
    elif 'power' in name:
        category = 'Power'
    elif 'polynomial' in name:
        category = 'Polynomial'
    elif 'exponential' in name:
        category = 'Exponential'
    elif 'binding' in name:
        category = 'Binding'
    elif 'folding' in name:
        category = 'Folding'
    elif 'statistical' in name:
        category = 'Statistical'
    elif 'special' in name:
        category = 'Special'
    elif 'rational' in name:
        category = 'Rational'
    elif 'lineshapes' in name or 'gaussian' in name or 'lorentzian' in name:
        category = 'Lineshapes'
    elif 'logistic' in name:
        category = 'Logistic'
    else:
        category = 'Other'
    
    if category not in categories:
        categories[category] = []
    categories[category].append(model)

# Print by category
for category in sorted(categories.keys()):
    print(f"\n{category} Functions ({len(categories[category])})")
    print("-" * 60)
    for model in sorted(categories[category], key=lambda m: m.name):
        params = ', '.join(f"{k}={v}" for k, v in sorted(model.parameters.items()))
        print(f"  • {model.name}")
        print(f"    Parameters: {params}")
        print(f"    Formula: {model.formula_str}")
        print()

print("=" * 60)
print(f"\n✓ All functions loaded successfully!")
print(f"✓ Total: {len(models)} functions available")
