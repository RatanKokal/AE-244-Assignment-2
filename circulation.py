import numpy as np
from fourier_coefficients import fourier_coefficients

def circulation(x, yc, alpha, vel_inf=20, num_terms=100):
    """
    Computes circulation distribution using Fourier coefficients.
    
    Parameters:
    x (array): Array of x-coordinates.
    yc (array): Mean camber line values.
    alpha (float): Angle of attack in radians.
    vel_inf (float): Freestream velocity.
    num_terms (int): Number of Fourier terms.
    
    Returns:
    tuple: Gamma values and corresponding theta values.
    """
    a0, an = fourier_coefficients(x, yc, alpha, num_terms=num_terms)
    # x is evenly spaced from 0 to 1, coefficients are calculated for corresponding theta values
    # x = c/2 * (1 - cos(theta)), theta = arccos(1 - 2x)
    theta = np.arccos(1 - 2 * x)
    # Formula as discussed in thin airfoil theory class
    gamma_vals = 2 * vel_inf * a0 * (1 + np.cos(theta)) / np.sin(theta)
    for n in range(1, num_terms + 1):
        gamma_vals += 2 * vel_inf * an[n-1] * np.sin(n * theta)
    return gamma_vals, theta