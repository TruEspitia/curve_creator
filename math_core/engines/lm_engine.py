import numpy as np
import time
from scipy.optimize import curve_fit
from .base_engine import BaseEngine

class LMEngine(BaseEngine):
    def fit(self, model, x_data, y_data, options=None):
        options = options or {}
        p0 = options.get('p0')
        bounds = options.get('bounds', (-np.inf, np.inf))
        
        # Prepare wrapper
        def wrapper(x, *params):
            return model.evaluate(x, *params)
            
        try:
            start_time = time.time()
            popt, pcov = curve_fit(
                wrapper, 
                x_data, 
                y_data, 
                p0=p0, 
                bounds=bounds,
                method='trf' if np.isfinite(bounds).all() else 'lm',
                maxfev=options.get('max_iter', 2000)
            )
            
            # Identify standard errors
            if pcov is None or np.isinf(pcov).any():
                perr = np.zeros_like(popt)
            else:
                perr = np.sqrt(np.diag(pcov))
                
            return {
                "success": True,
                "popt": popt,
                "perr": perr,
                "message": "Optimization converged",
                "engine": "Levenberg-Marquardt",
                "time": time.time() - start_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "engine": "Levenberg-Marquardt"
            }
