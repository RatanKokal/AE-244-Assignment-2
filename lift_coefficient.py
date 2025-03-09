import numpy as np
from fourier_coefficients import fourier_coefficients
from circulation import circulation
from tot_circulation import total_circulation

def lift_coefficient(x, yc, alpha, v_inf=20, num_terms=100):
    """
    Computes lift coefficient from Fourier coefficients.
    
    Parameters:
    x (array): Array of x-coordinates.
    yc (array): Mean camber line values.
    alpha (float): Angle of attack in radians.
    tot_circualtion (float): Total circulation.
    v_inf (float): Freestream velocity
    num_terms (int): Number of Fourier terms.
    
    Returns:
    float: Lift coefficient using formula (Cl).
    float: Lift coefficient using computational method.
    """
    a0, an = fourier_coefficients(x, yc, alpha, num_terms=num_terms)
    # Formula for lift coefficient, deriving using thin airfoil theory
    cl_form = np.pi * (2 * a0 + an[0])
    # Lift coefficient calculated using computational method
    gamma_vals, _ = circulation(x, yc, alpha, v_inf, num_terms=num_terms)
    tot_circualtion, _ = total_circulation(x, gamma_vals)
    # Using relation between lift coefficient and total circulation
    cl_comp = 2 * tot_circualtion / v_inf
    return cl_form, cl_comp