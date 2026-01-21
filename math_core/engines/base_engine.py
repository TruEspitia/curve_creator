from abc import ABC, abstractmethod

class BaseEngine(ABC):
    @abstractmethod
    def fit(self, model, x_data, y_data, options=None):
        """
        Abstract method for fitting data.
        
        Args:
            model: FFuncModel instance
            x_data: numpy array
            y_data: numpy array
            options: dict of options
            
        Returns:
            dict with 'success', 'parameters', 'errors', 'r_squared', etc.
        """
        pass
