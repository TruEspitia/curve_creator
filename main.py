import eel
import sys
import os

from math_core.data_loader import DataLoader
from math_core.ffunc_parser import FFuncParser, FFuncModel
from math_core.optimization import OptimizationEngine

# Initialize Eel with the web folder
eel.init('web')

import tkinter as tk
from tkinter import filedialog

GLOBAL_DATA = {} # To store loaded data in memory temporarily

@eel.expose
def app_ready():
    print("Frontend is ready!")
    return "Backend Connected"

@eel.expose
def pick_file():
    root = tk.Tk()
    root.withdraw() # Hide main window
    root.wm_attributes('-topmost', 1) # Bring to front
    file_path = filedialog.askopenfilename(
        filetypes=[("Data Files", "*.csv *.xlsx *.xls *.txt")]
    )
    return file_path

@eel.expose
def load_data_file(filepath):
    print(f"Loading file: {filepath}")
    result = DataLoader.load_file(filepath)
    if not "error" in result:
        GLOBAL_DATA['current_data'] = result
    return result

@eel.expose
def get_functions_list():
    functions_dir = os.path.join(os.getcwd(), 'functions')
    print(f"Scanning functions in: {functions_dir}")
    models = FFuncParser.get_available_functions(functions_dir)
    # Serialize for JS
    return [{
        "name": m.name, 
        "parameters": m.parameters, 
        "formula": m.formula_str
    } for m in models]

@eel.expose
def run_fit(function_name, col_x, col_y):
    print(f"Fitting {function_name} using X={col_x}, Y={col_y}...")
    if 'current_data' not in GLOBAL_DATA:
        return {"error": "No data loaded"}
        
    data_info = GLOBAL_DATA['current_data']
    raw_data = data_info['data']
    
    # Extract selected columns
    try:
        x_data = [d[col_x] for d in raw_data]
        y_data = [d[col_y] for d in raw_data]
    except KeyError:
        return {"error": "Invalid column selection"}

    # Find the model
    functions_dir = os.path.join(os.getcwd(), 'functions')
    models = FFuncParser.get_available_functions(functions_dir)
    model = next((m for m in models if m.name == function_name), None)
    
    if model is None:
        return {"error": f"Function '{function_name}' not found"}
    
    result = OptimizationEngine.fit_data(model, x_data, y_data)
    print(f"Fit result: {result}")
    return result

@eel.expose
def run_custom_fit(formula_str, params_str, col_x, col_y):
    print(f"Custom Fit: {formula_str} with {params_str} on X={col_x}, Y={col_y}")
    if 'current_data' not in GLOBAL_DATA:
        return {"error": "No data loaded"}
        
    data_info = GLOBAL_DATA['current_data']
    raw_data = data_info['data']

    # Parse parameters: "a=1, b=2" -> {"a": 1, "b": 2}
    params = {}
    if params_str:
        try:
            for p in params_str.split(','):
                if '=' in p:
                    name, val = p.split('=')
                    params[name.strip()] = float(val.strip())
        except Exception as e:
            return {"error": f"Error parsing parameters: {e}"}

    # Extract selected columns
    try:
        x_data = [d[col_x] for d in raw_data]
        y_data = [d[col_y] for d in raw_data]
    except KeyError:
        return {"error": "Invalid column selection"}

    # Create temporary model
    model = FFuncModel("custom", params, formula_str)
    
    return OptimizationEngine.fit_data(model, x_data, y_data)

def start_app():
    # Attempt to start with Chrome/Edge, fallback to default browser
    try:
        eel.start('index.html', size=(1200, 800))
    except EnvironmentError:
        # If Chrome isn't found, fallback to other browsers
        eel.start('index.html', mode='default', size=(1200, 800))

if __name__ == "__main__":
    start_app()
