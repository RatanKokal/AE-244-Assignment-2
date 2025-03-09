import numpy as np
from slope_camber import slope_camber

def fourier_coefficients(x, yc, alpha, num_terms=100):
    """
    Computes the Fourier coefficients A0 and An for the mean camber line.
    
    Parameters:
    x (array): Array of x-coordinates.
    yc (array): Mean camber line values.
    alpha (float): Angle of attack in radians.
    num_terms (int): Number of Fourier terms.
    
    Returns:
    tuple: A0 and list of An coefficients.
    """
    theta = np.linspace(0, np.pi, x.shape[0])
    x_cords = 0.5 * (1 - np.cos(theta))
    dz_dx = np.array([slope_camber(x, yc, x_cord) for x_cord in x_cords])
    # Prune the None values
    valid_indices = [i for i, val in enumerate(dz_dx) if val is not None]
    dz_dx = np.array([dz_dx[i] for i in valid_indices])
    theta = np.array([theta[i] for i in valid_indices])
    
    delta_theta = np.pi / x.shape[0]
    # Using the formula given in slides
    a0 = alpha * np.pi / 180 - (1 / np.pi) * np.sum(dz_dx * delta_theta)
    an = [2 / np.pi * np.sum(dz_dx * np.cos(n * theta) * delta_theta) for n in range(1, num_terms + 1)]
    
    return a0, an