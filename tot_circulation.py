import numpy as np

def total_circulation(x, gamma_vals):
    """
    Computes total circulation by integrating gamma over theta.
    
    Parameters:
    x (array): Array of x-coordinates.
    gamma_vals (array): Circulation distribution.
    N (int): Number of points.
    
    Returns:
    float: Total circulation.
    """
    delta_x = x[1] - x[0]
    return np.sum(gamma_vals * delta_x)