import os

FUNCTIONS_DIR = r"c:\Users\miguel.espitia\Desktop\CurveCreator\functions"

# Mapping of partial name (or full name) to complexity
# 1: Simple (LM safe)
# 2: Moderate (DE/Seq recommended)
# 3: Complex (Seq only)

COMPLEXITY_MAP = {
    # Polynomials (Safe)
    "polynomial": 1,
    "linear": 1,
    
    # Exponentials
    "exponential_single": 1,
    "exponential_double": 2, # Harder for LM
    "exponential_plateau": 2,
    
    # Binding/Growth
    "binding": 1,
    "michaelis": 1,
    "gompertz": 3, # Double exp inside
    "weibull": 3,
    "logistic": 3,
    "sigmoid": 2,
    
    # Trigonometric
    "sine": 2, # Periodic is hard for LM if guess is wrong
    "cosine": 2,
    "tangent": 2,
    "damped_sine": 3, # Very hard
    "sinh": 2,
    "cosh": 2,
    
    # Power
    "power": 1,
    "sqrt": 1,
    
    # Statistical
    "gaussian": 2,
    "lorentzian": 2,
    "tanh": 1,
    
    # Special
    "rational": 2,
    "folding": 3, # Usually complex
}

def get_complexity(filename):
    name = filename.lower()
    best_match = 1
    for key, val in COMPLEXITY_MAP.items():
        if key in name:
            best_match = max(best_match, val)
    return best_match

def update_files():
    count = 0
    for root, dirs, files in os.walk(FUNCTIONS_DIR):
        for file in files:
            if file.endswith(".ffunc"):
                fullpath = os.path.join(root, file)
                
                # Check if already has metadata
                with open(fullpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "<METADATA>" in content:
                    continue # Skip if already has metadata
                
                complexity = get_complexity(file)
                
                # Append metadata
                metadata_block = f"\n<METADATA>\ncomplexity: {complexity}\n"
                
                with open(fullpath, 'a', encoding='utf-8') as f:
                    f.write(metadata_block)
                
                print(f"Updated {file} -> Complexity {complexity}")
                count += 1
                
    print(f"Updated {count} files.")

if __name__ == "__main__":
    update_files()
