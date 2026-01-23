import numpy as np
import sys
import os
import time

sys.path.append(os.getcwd())

from math_core.optimization import OptimizationEngine
from math_core.ffunc_parser import FFuncModel

def reproduce_failure():
    print("--- Reproducing DE Failure ---")
    
    # Model: y = a*x + b
    params = {'a': 1.0, 'b': 0.0}
    formula = "a * x + b"
    model = FFuncModel("linear", params, formula)
    
    x_data = np.linspace(0, 10, 100)
    y_data = 2.0 * x_data + 5.0 # True: a=2, b=5
    
    # Force a failure by setting tiny timeout
    # Sequential engine splits time: 60% DE. If total is small, DE might just fail or run out of time.
    # However, DE is fast for this model. We might need to mock or subclass to force failure if we can't do it via options.
    # Let's try simulating a complex surface by using a bad model or just very strictly low max_iter if possible.
    # But max_iter is hardcoded to min(opt.max_iter, 100).
    
    # Actually, the user error said "DE phase failed...". 
    # Let's try to patch the DE engine temporarily in this script to always fail.
    
    from math_core.engines import sequential_engine
    
    # Monkey patch DE engine's optimize to return failure
    original_de_optimize = sequential_engine.DEEngine._optimize
    
    def mock_fail_optimize(self, model, x, y, options):
        from math_core.engines.base_engine import FitResult, OptimizationStatus
        res = FitResult(
            success=False,
            status=OptimizationStatus.CONVERGENCE_FAILED,
            parameters={'a': 1.8, 'b': 4.8},
            errors={},
            r_squared=0.0,
            rmse=0.5,
            message="Mocked DE Fail"
        )
        return res
        
    sequential_engine.DEEngine._optimize = mock_fail_optimize
    
    try:
        print("Running fit with SequentialEngine (Mocked DE Failure)...")
        # We expect this to FAIL currently because of the aggressive check
        result = OptimizationEngine.fit_data(model, x_data.tolist(), y_data.tolist(), engine_type="sequential")
        
        print(f"Result Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        
        if "DE phase failed" in result.get('message', '') or "Mocked DE Fail" in result.get('message', ''):
             if not result.get('success'):
                 print("REPRODUCTION SUCCESSFUL: The engine aborted because DE failed.")
             else:
                 print("UNEXPECTED: The engine succeeded despite DE failure?")
        else:
            print("Did not see expected failure message.")
            
    finally:
        # Restore
        sequential_engine.DEEngine._optimize = original_de_optimize

if __name__ == "__main__":
    reproduce_failure()
