import numpy as np
from fourier_coefficients import fourier_coefficients
from circulation import circulation

def moment_coefficient(x, yc, alpha, v_inf=20, num_terms=10):
    """
    Computes lift coefficient from Fourier coefficients.
    
    Parameters:
    x (array): Array of x-coordinates.
    yc (array): Mean camber line values.
    alpha (float): Angle of attack in radians.
    v_inf (float): Freestream velocity.
    num_terms (int): Number of Fourier terms.
    
    Returns:
    float: Moment coefficient calculated using formula (Cm).
    float: Moment coefficient calculated using computational method.
    """
    _, an = fourier_coefficients(x, yc, alpha, num_terms=num_terms)
    a1, a2 = an[0], an[1]
    # Formula for moment coefficient, deriving using thin airfoil theory
    cm_form = np.pi * (a1 - a2) / 4
    # Moment coefficient calculated using computational method
    gamma_vals, _ = circulation(x, yc, alpha, v_inf, num_terms=num_terms)
    dx = x[1] - x[0]
    # Moment coefficient about c/4
    cm_comp = 2 * np.sum((x - 1/4) * gamma_vals * dx) / v_inf
    return cm_form, cm_comp