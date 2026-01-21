import numpy as np
import time
from scipy.optimize import differential_evolution, curve_fit
from .base_engine import BaseEngine

# Cost function must be top-level for multiprocessing pickling
def _de_cost_low_level(params, model, x_data, y_data):
    try:
        y_est = model.evaluate(x_data, *params)
        if np.any(np.isnan(y_est)) or np.any(np.isinf(y_est)):
            return np.inf
        return np.sum((y_data - y_est) ** 2)
    except Exception:
        return np.inf

class DEEngine(BaseEngine):
    def fit(self, model, x_data, y_data, options=None):
        options = options or {}
        bounds_list = options.get('bounds_list') # Must be list of (min, max) tuples
        
        if not bounds_list:
            return {"success": False, "error": "Bounds are required for Differential Evolution"}

        try:
            start_time = time.time()
            
            # Enforce 5s timeout check inside callback or via maxiter
            # DE doesn't support simple timeout arg easily, so we use maxiter approx
            # or rely on the caller to kill it, but we want to be safe.
            # We'll use a conservative maxiter for now as "5s" is handled by the main thread timeout usually,
            # but here we can limit generations.
            
            result = differential_evolution(
                _de_cost_low_level, 
                bounds_list,
                args=(model, x_data, y_data),
                strategy='best1bin',
                maxiter=5000, # Limit iterations to keep it fast enough
                popsize=10,
                tol=0.01,
                seed=None,
                workers=-1
            )
            
            if not result.success:
                 return {
                    "success": False,
                    "error": result.message,
                    "engine": "Differential Evolution"
                }

            popt = result.x
            
            # DE doesn't calculate covariance, so we do a quick single-step curve_fit 
            # at the optimum to get errors, with fixed p0
            try:
                def wrapper(x, *params):
                    return model.evaluate(x, *params)
                    
                # Small refinement and error estimation
                popt_ref, pcov = curve_fit(wrapper, x_data, y_data, p0=popt, maxfev=100)
                popt = popt_ref
                if pcov is None or np.isinf(pcov).any():
                    perr = np.zeros_like(popt)
                else:
                    perr = np.sqrt(np.diag(pcov))
            except:
                perr = np.zeros_like(popt)

            return {
                "success": True,
                "popt": popt,
                "perr": perr,
                "message": "Optimization converged (Global)",
                "engine": "Differential Evolution",
                "time": time.time() - start_time
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "engine": "Differential Evolution"
            }
