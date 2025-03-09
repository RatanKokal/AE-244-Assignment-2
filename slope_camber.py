import numpy as np

def slope_camber(x, yc, x_cord):
    """
    Computes the slope of the mean camber line at a given x-coordinate using finite differences.
    
    Parameters:
    x (array): Array of x-coordinates.
    yc (array): Array of camber line values.
    x_cord (float): Specific x-coordinate.
    
    Returns:
    float or None: Slope at x_cord or None if out of range.
    """
    idx = np.searchsorted(x, x_cord)
    if 0 < idx < len(x):
        return (yc[idx] - yc[idx-1]) / (x[idx] - x[idx-1])
    return None