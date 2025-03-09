import numpy as np
from matplotlib import pyplot as plt
from lift_coefficient import lift_coefficient
from moment_coefficient import moment_coefficient
from camber import naca, custom_camber
from circulation import circulation
from tot_circulation import total_circulation
from vector_field import vector_field
from moment_coefficient import moment_coefficient
from slope_camber import slope_camber
from parameter_getter import read_parameters


def main():
    
    # Parameters for NACA airfoil
    params = read_parameters('input.txt')
    # Option to choose
    option = int(params.get('option', 1))
    # Number of points
    N = int(params.get('N', 10000))
    # Angle of attack
    alpha = params.get('alpha', 3)
    # Freestream velocity
    v_inf = params.get('v_inf', 20)
    
    if option == 1:
        # Camber parameters for NACA airfoil
        camber = params.get('camber', 0.059)
        position = params.get('position', 0.41)
        x, yc = naca(camber, position, N)
    else:
        f1 = params.get('f1', '0.02*x**2').strip()
        x, yc = custom_camber(f1, N)
    
    # Plotting the mean camber line
    plt.figure(figsize=(10, 6))
    plt.plot(x, yc, label='Mean Camber Line')
    plt.xlabel('x (chord length)')
    plt.ylabel('y (chord length)')
    plt.title('Mean Camber Line of Airfoil')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Plotting the slope of the mean camber line
    dy_dx = np.array([slope_camber(x, yc, x_val) for x_val in x if slope_camber(x, yc, x_val) is not None])
    x_dash = np.array([x_val for x_val in x if slope_camber(x, yc, x_val) is not None])
    plt.figure(figsize=(10, 6))
    plt.plot(x_dash, dy_dx, label='Slope of Mean Camber Line')
    plt.xlabel('x (chord length)')
    plt.ylabel('dy/dx')
    plt.title('Slope of Mean Camber Line')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Computing lift and moment coefficients
    cl_form, cl_comp = lift_coefficient(x, yc, alpha, v_inf, num_terms=100)
    print(f'Lift coefficient at alpha obtained using formula = {alpha}: {cl_form}')
    print(f'Computed Lift coefficient at alpha = {alpha}: {cl_comp}')
    cm_form, cm_comp = moment_coefficient(x, yc, alpha, v_inf, num_terms=100)
    print(f'Moment coefficient at alpha obtained using formula = {alpha}: {cm_form}')
    print(f'Computed Moment coefficient at alpha = {alpha}: {cm_comp}')
    
    gamma_vals, theta = circulation(x, yc, alpha, v_inf, num_terms=100)
    
    # Plotting the velocity field around the airfoil
    X, Y, U, V, v_max, v_min = vector_field(x, yc, gamma_vals, alpha, v_inf)
    mag = np.sqrt(U**2 + V**2)
    
    print(f'Maximum velocity magnitude: {v_max}')
    print(f'Minimum velocity magnitude: {v_min}')
    
    plt.figure(figsize=(10, 6))
    plt.quiver(X, Y, U, V, mag, cmap='viridis', scale_units='xy')
    plt.scatter(x, yc, color='red', marker='o', s=1, label='Discrete Vortices')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.xlabel('x (chord length)')
    plt.ylabel('y (chord length)')
    plt.title('Velocity Field Around the Airfoil')
    plt.colorbar(label='Velocity Magnitude')
    plt.legend()
    plt.grid()
    plt.show()
    
    # Plotting the circulation distribution
    plt.plot(theta, gamma_vals, label='Circulation Distribution')
    plt.xlabel('Theta')
    plt.ylabel('Gamma')
    plt.title('Circulation Distribution over Theta')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Computing total circulation
    circ = total_circulation(x, gamma_vals)
    print(f'Total circulation at alpha = {alpha}: {circ}')
    
if __name__ == "__main__":
    main()