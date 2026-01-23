import numpy as np
import sys
import os

# Ensure we can import from the project root
sys.path.append(os.getcwd())

from math_core.optimization import OptimizationEngine
from math_core.ffunc_parser import FFuncModel

def test_optimization():
    print("--- Starting Reproduction Test ---")
    
    # 1. Create a dummy model (e.g., Line: y = a*x + b)
    # matching the internal structure expected
    params = {'a': 1.0, 'b': 0.0}
    formula = "a * x + b"
    model = FFuncModel("proportional", params, formula)
    
    # 2. Create dummy data (Line y = 2x + 10)
    x_data = np.linspace(0, 10, 20)
    y_data = 2.0 * x_data + 10.0
    
    # 3. Define options with a specific p0 that is CLOSE to solution
    # If p0 is ignored, and the engine uses defaults (1.0, 1.0), it might take longer or fail in complex cases.
    # But for a line it should converge anyway. 
    # To test if p0 is passed, we can check if LMEngine uses it.
    # However, since I can't easily spy on internal calls without mocking, 
    # I will rely on inspecting the `base_engine.py` code logic mostly, 
    # but run this to see if it CRASHES due to the sequential engine double definition.
    
    print("Running fit with SequentialEngine...")
    result = OptimizationEngine.fit_data(model, x_data.tolist(), y_data.tolist(), engine_type="sequential")
    
    print("Result Success:", result.get('success'))
    print("Parameters:", result.get('parameters'))
    print("Message:", result.get('message'))
    
    if result.get('success'):
        print("Fit seemed to work.")
    else:
        print("Fit FAILED.")

    # 4. Test LM Engine specifically to see if p0 issue matters (simulate 'optimization.py' passing p0)
    # optimization.py passes p0 as a list.
    print("\nRunning fit with LMEngine (checking p0 transfer logic)...")
    # We expect this might use default guesses if p0 is dropped, but should still work for a line.
    result_lm = OptimizationEngine.fit_data(model, x_data.tolist(), y_data.tolist(), engine_type="lm")
    print("LM Success:", result_lm.get('success'))
    print("LM Message:", result_lm.get('message'))

if __name__ == "__main__":
    test_optimization()
