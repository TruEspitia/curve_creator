from .base_engine import BaseEngine
from .lm_engine import LMEngine
from .de_engine import DEEngine
import numpy as np
import time

class SequentialEngine(BaseEngine):
    def fit(self, model, x_data, y_data, options=None):
        options = options or {}
        
        # Phase 1: Global Search (DE)
        de_engine = DEEngine()
        de_result = de_engine.fit(model, x_data, y_data, options)
        
        if not de_result["success"]:
            return de_result # Propagate error
            
        # Phase 2: Local Refinement (LM)
        # Use DE result as p0 for LM
        lm_options = options.copy()
        lm_options['p0'] = de_result['popt']
        
        lm_engine = LMEngine()
        lm_result = lm_engine.fit(model, x_data, y_data, lm_options)
        
        # Merge info
        lm_result['engine'] = "Sequential (DE + LM)"
        lm_result['phases'] = [
            {"name": "Differential Evolution", "time": de_result.get('time', 0)},
            {"name": "Levenberg-Marquardt", "time": lm_result.get('time', 0)}
        ]
        
        return lm_result
