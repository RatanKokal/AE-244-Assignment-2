import numpy as np
import sympy as sp
from matplotlib import pyplot as plt

def naca(max_camber, pos, N=1000):
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
    yc = np.where(x < pos,
                  max_camber / pos**2 * (2 * pos * x - x**2),
                  max_camber / (1 - pos)**2 * ((1 - 2 * pos) + 2 * pos * x - x**2))
    return x, yc

def custom_camber(N=1000):
    """
    Generates a custom mean camber line for an airfoil.
    """
    
    x = np.linspace(1/N, 1, N)
    
    f1 = input("Enter the first function: ")
    f2 = input("Enter the second function: ")
    
    X = sp.symbols('x')
    f1 = sp.sympify(f1)
    f2 = sp.sympify(f2)
    
    y_top = np.array([np.float32(f1.subs(X, x_val)) for x_val in x])
    y_bot = np.array([np.float32(f2.subs(X, x_val)) for x_val in x])
    
    yc = (y_top + y_bot)/2
    return x, yc

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

def fourier_coefficients(x, yc, alpha, num_terms=10):
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
    valid_indices = [i for i, val in enumerate(dz_dx) if val is not None]
    dz_dx = np.array([dz_dx[i] for i in valid_indices])
    theta = np.array([theta[i] for i in valid_indices])
    
    delta_theta = np.pi / x.shape[0]
    a0 = alpha - (1 / np.pi) * np.sum(dz_dx * delta_theta)
    an = [2 / np.pi * np.sum(dz_dx * np.cos(n * theta) * delta_theta) for n in range(1, num_terms + 1)]
    
    return a0, an

def circulation(x, yc, alpha, vel_inf=1, num_terms=10):
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
    theta = np.arccos(1 - 2 * x)
    gamma_vals = 2 * vel_inf * a0 * (1 + np.cos(theta)) / np.sin(theta)
    for n in range(1, num_terms + 1):
        gamma_vals += 2 * vel_inf * an[n-1] * np.sin(n * theta)
    return gamma_vals, theta

def total_circulation(x, gamma_vals, N=1000):
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

def lift_coefficient(x, yc, alpha, num_terms=10):
    """
    Computes lift coefficient from Fourier coefficients.
    
    Parameters:
    x (array): Array of x-coordinates.
    yc (array): Mean camber line values.
    alpha (float): Angle of attack in radians.
    num_terms (int): Number of Fourier terms.
    
    Returns:
    float: Lift coefficient (Cl).
    """
    a0, an = fourier_coefficients(x, yc, alpha, num_terms=num_terms)
    return np.pi * (2 * a0 + an[0])

def vector_field(x, yc, gamma_vals, vel_inf=1, grid_size=(300, 400)):
    """
    Computes and plots the vector field around the airfoil using discrete vortex summation.
    """
    x_grid = np.linspace(-1, 3, grid_size[1])  # 4c domain along x
    y_grid = np.linspace(-1.5, 1.5, grid_size[0])  # 3c domain along y
    X, Y = np.meshgrid(x_grid, y_grid)
    x_vortices, y_vortices = x, yc
    U, V = np.zeros_like(X), np.zeros_like(Y)
    
    for i in range(len(x_vortices)):
        dx, dy = X - x_vortices[i], Y - y_vortices[i]
        r2 = dx**2 + dy**2 + 1e-12  # Avoid singularities
        U += (gamma_vals[i] / (2 * np.pi)) * (dy / r2) + vel_inf
        V += (gamma_vals[i] / (2 * np.pi)) * (-dx / r2)
    
    plt.figure(figsize=(10, 6))
    plt.quiver(X, Y, U, V, np.sqrt(U**2 + V**2), cmap='viridis', scale_units='xy')
    plt.scatter(x_vortices, y_vortices, color='red', marker='o', s=1, label='Discrete Vortices')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.xlabel('x (chord length)')
    plt.ylabel('y (chord length)')
    plt.title('Velocity Field Around the Airfoil')
    plt.colorbar(label='Velocity Magnitude')
    plt.legend()
    plt.grid()
    plt.show()

def main():
    """Main function to compute circulation and lift coefficient for a NACA airfoil."""
    N = 10000
    x, yc = custom_camber(N)
    alpha = 0
    cl = lift_coefficient(x, yc, alpha)
    gamma_vals, theta = circulation(x, yc, alpha, num_terms=100)
    circ = total_circulation(x, gamma_vals, N)
    
    print(f'Lift coefficient at alpha = {alpha}: {cl}')
    print(f'Total circulation at alpha = {alpha}: {circ}')
    
    vector_field(x, yc, gamma_vals)
    plt.plot(theta, gamma_vals, label='Circulation Distribution')
    plt.xlabel('Theta')
    plt.ylabel('Gamma')
    plt.title('Circulation Distribution over Theta')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
