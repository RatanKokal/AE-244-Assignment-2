import numpy as np

def total_circulation(x, gamma_vals, U=None, V=None, ds=0.01):
    """
    Computes total circulation by integrating gamma over theta.
    
    Parameters:
    x (array): Array of x-coordinates.
    gamma_vals (array): Circulation distribution.
    N (int): Number of points.
    
    Returns:
    float: Total circulation using vortex filament.
    float: Total circulation using line integral.
    """
    delta_x = x[1] - x[0]
    total_circ_vortex = np.sum(gamma_vals * delta_x)
    # Calculate line integral using v.ds, grid size (400, 300) assumed
    # If line integral is to be calculated, U and V must be provided
    if U is None and V is None:
        return total_circ_vortex, None
    # Line integral using v.ds
    total_circ_line = (np.sum(V[75:225, 50]) + np.sum(U[225, 50:350]) - np.sum(V[75:225, 350]) - np.sum(U[75, 50:350])) * ds
    return total_circ_vortex, total_circ_line