import sys
import os
import numpy as np

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from math_core.ffunc_parser import FFuncParser, FFuncModel
from math_core.optimization import OptimizationEngine

def generate_test_data(model, params, noise=0.0):
    x = np.linspace(0, 10, 20)
    y_true = model.evaluate(x, *params)
    y_noise = y_true + np.random.normal(0, noise, size=len(x))
    return x.tolist(), y_noise.tolist()

def text_engine(engine_name):
    print(f"\n Testing Engine: {engine_name} ".center(60, "="))
    
    # 1. Test Linear (Simple) with LM
    print("\n[Test 1] Linear Model (Simple)")
    model = FFuncModel("linear", {"A0": 0, "A1": 1}, "y = A1 * x + A0")
    x, y = generate_test_data(model, [10, 2], noise=0.1) # A0=10, A1=2
    
    result = OptimizationEngine.fit_data(model, x, y, engine_type=engine_name)
    
    if result['success']:
        print(f"✓ Success! R²: {result['r_squared']:.4f}")
        print(f"  Params: {result['parameters']}")
        print(f"  Engine Info: {result.get('engine', 'N/A')}")
    else:
        print(f"✗ Failed: {result.get('error')}")

    # 2. Test Exponential (Moderate) 
    print("\n[Test 2] Exponential Model (Moderate)")
    model_exp = FFuncModel("exp", {"A": 1, "k": 1}, "y = A * exp(-k * x)")
    x_exp, y_exp = generate_test_data(model_exp, [100, 0.5], noise=0.5) 
    
    result = OptimizationEngine.fit_data(model_exp, x_exp, y_exp, engine_type=engine_name)
    
    if result['success']:
        print(f"✓ Success! R²: {result['r_squared']:.4f}")
        print(f"  Params: {result['parameters']}")
    else:
        print(f"✗ Failed: {result.get('error')}")

if __name__ == "__main__":
    print("Optimization Engine Verification Script")
    
    try:
        text_engine("lm")
        text_engine("de")
        text_engine("sequential")
        print("\nAll tests completed.")
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
