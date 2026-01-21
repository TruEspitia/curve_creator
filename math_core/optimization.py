import numpy as np
from scipy.optimize import curve_fit
from .ffunc_parser import FFuncModel

class OptimizationEngine:
    @staticmethod
    def fit_data(func_model: FFuncModel, x_data, y_data):
        """
        Performs curve fitting.
        
        Args:
            func_model: FFuncModel instance
            x_data: list or array of x values
            y_data: list or array of y values
        
        Returns:
            Dictionary with results: {
                "success": bool,
                "parameters": {name: value},
                "errors": {name: standard_error},
                "r_squared": value
            }
        """
        x_arr = np.array(x_data, dtype=float)
        y_arr = np.array(y_data, dtype=float)
        
        # Initial guesses from default parameters
        param_names = sorted(func_model.parameters.keys())
        p0 = [func_model.parameters[name] for name in param_names]
        
        # Wrapper function for curve_fit that explodes parameters
        def fit_wrapper(x, *params):
            return func_model.evaluate(x, *params)
            
        try:
            popt, pcov = curve_fit(fit_wrapper, x_arr, y_arr, p0=p0)
            
            # Calculate Standard Errors (handle case where covariance couldn't be estimated)
            if np.isinf(pcov).any():
                perr = np.zeros(len(popt))
            else:
                perr = np.sqrt(np.diag(pcov))
            
            # Calculate R-squared
            residuals = y_arr - fit_wrapper(x_arr, *popt)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y_arr - np.mean(y_arr))**2)
            r_squared = 1 - (ss_res / ss_tot)
            
            # Result formatting
            result_params = {}
            result_errors = {}
            for i, name in enumerate(param_names):
                result_params[name] = float(popt[i])
                result_errors[name] = float(perr[i])
                
            return {
                "success": True,
                "parameters": result_params,
                "errors": result_errors,
                "r_squared": r_squared,
                 # Return fitted curve for visualization convenience
                "fitted_curve": fit_wrapper(x_arr, *popt).tolist()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
