import os
import numpy as np

class FFuncModel:
    def __init__(self, name, parameters, formula_str):
        self.name = name
        self.parameters = parameters # dict of {param_name: default_value}
        self.formula_str = formula_str
        self.compiled_formula = None

    def evaluate(self, x, *params):
        """
        Evaluates the function.
        x: numpy array of x values
        params: list of parameter values in alphabetical order of keys (A0, A1, ...)
        """
        # Create a local context with numpy functions available
        local_context = {
            'x': x,
            'np': np,
            'exp': np.exp,
            'sin': np.sin,
            'cos': np.cos,
            'log': np.log,
            'log10': np.log10,
            'sqrt': np.sqrt,
            'pi': np.pi,
            'power': np.power
        }
        
        # Sort parameter names to match the *params order
        param_names = sorted(self.parameters.keys())
        
        if len(params) != len(param_names):
             raise ValueError(f"Expected {len(param_names)} parameters, got {len(params)}")

        for name, val in zip(param_names, params):
            local_context[name] = val

        # Evaluate
        # We replace 'y =' part if it exists
        formula = self.formula_str
        if "=" in formula:
            formula = formula.split("=")[1].strip()
            
        return eval(formula, {"__builtins__": {}}, local_context)

class FFuncParser:
    @staticmethod
    def parse_file(filepath):
        name = os.path.basename(filepath).replace(".ffunc", "")
        parameters = {}
        formula_lines = []
        
        mode = None # 'PARAMETERS' or 'FORMULA'
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                if line == "<PARAMETERS>":
                    mode = "PARAMETERS"
                    continue
                elif line == "<FORMULA>":
                    mode = "FORMULA"
                    continue
                
                if mode == "PARAMETERS":
                    # Parse "Name, Value"
                    parts = line.split(",")
                    if len(parts) >= 2:
                        p_name = parts[0].strip()
                        try:
                            p_val = float(parts[1].strip())
                            parameters[p_name] = p_val
                        except ValueError:
                            pass # Skip invalid params
                
                elif mode == "FORMULA":
                    if line.startswith("#"): continue
                    formula_lines.append(line)
        
        formula_str = " ".join(formula_lines)
        return FFuncModel(name, parameters, formula_str)

    @staticmethod
    def get_available_functions(functions_dir):
        models = []
        if not os.path.exists(functions_dir):
            return models
            
        for root, dirs, files in os.walk(functions_dir):
            for file in files:
                if file.endswith(".ffunc"):
                    full_path = os.path.join(root, file)
                    try:
                        model = FFuncParser.parse_file(full_path)
                        models.append(model)
                    except Exception as e:
                        print(f"Error parsing {file}: {e}")
        return models
