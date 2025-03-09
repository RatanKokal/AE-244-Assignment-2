import json

class AirfoilParams:
    def __init__(self, filename):
        """Load airfoil parameters from a JSON file."""
        with open(filename, "r") as f:
            self.params = json.load(f)

    def get_param(self, airfoil_index, param_name):
        """Retrieve a parameter for a specific airfoil."""
        if 0 <= airfoil_index < len(self.params["airfoils"]):
            airfoil = self.params["airfoils"][airfoil_index]
            return airfoil.get(param_name, f"'{param_name}' not found")
        else:
            return "Invalid airfoil index"

    def get_all(self):
        """Retrieve all airfoil parameters."""
        return self.params["airfoils"]