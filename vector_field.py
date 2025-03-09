import numpy as np

def vector_field(x, yc, gamma_vals, alpha, vel_inf=20, grid_size=(400, 300)):
    """
    Computes the vector field around the airfoil using discrete vortex summation.
    
    Parameters:
    x (array): Array of x-coordinates.
    yc (array): Mean camber line values.
    gamma_vals (array): Circulation distribution.
    alpha (float): Angle of attack in radians.
    vel_inf (float): Freestream velocity.
    grid_size (tuple): Grid size.
    
    Returns:
    tuple: X, Y, U, V, v_max, v_min.
    """
    x_grid = np.linspace(-1, 3, grid_size[0])  # 4c domain along x
    y_grid = np.linspace(-1.5, 1.5, grid_size[1])  # 3c domain along y
    X, Y = np.meshgrid(x_grid, y_grid)
    U, V = np.zeros_like(X), np.zeros_like(Y)
    
    # Freestream velocity components
    U += vel_inf * np.cos(alpha*np.pi/180)
    V += vel_inf * np.sin(alpha*np.pi/180)
    
    for i in range(len(x)):
        dx, dy = X - x[i], Y - yc[i]
        r2 = dx**2 + dy**2 + 1e-12  # Avoid singularities
        # The velocity field due to a vortex is given by the Biot-Savart law and components due to a vortex
        U += (gamma_vals[i] * (x[1] - x[0]) / (2 * np.pi)) * (dy / r2) 
        V += (gamma_vals[i] * (x[1] - x[0]) / (2 * np.pi)) * (-dx / r2)
        
    mag = np.sqrt(U**2 + V**2)
    v_max = np.max(mag)
    v_min = np.min(mag)
    
    return X, Y, U, V, v_max, v_min