import numpy as np
import sympy as sp

def naca(max_camber, pos, N=10000):
    """
    Generates the mean camber line for a NACA airfoil.
    
    Parameters:
    max_camber (float): Maximum camber of the airfoil.
    pos (float): Position of maximum camber along the chord.
    N (int): Number of points along the chord.
    
    Returns:
    tuple: Arrays of x-coordinates and mean camber line (yc).
    """
    x = np.linspace(1/N, 1, N)
    # Using NACA 4 digit series equation
    #yc indicates the array of camber line points
    yc = np.where(x < pos, 
                  max_camber / pos**2 * (2 * pos * x - x**2),
                  max_camber / (1 - pos)**2 * ((1 - 2 * pos) + 2 * pos * x - x**2))
    return x, yc

def custom_camber(f1, N=10000):
    """
    Generates a custom mean camber line for an airfoil.
    
    Parameters:
    N (int): Number of points along the chord.
    f1 (str): Function of x for the mean camber line.
    
    Returns:
    tuple: Arrays of x-coordinates and mean camber line (yc).
    """
    
    x = np.linspace(1/N, 1, N)
    
    X = sp.symbols('x')
    f1 = sp.sympify(f1)

    # Substitute values in curve
    #yc indicates the array of camber line points
    yc= np.array([np.float32(f1.subs(X, x_val)) for x_val in x])
    
    return x, yc
