import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from lift_coefficient import lift_coefficient
from moment_coefficient import moment_coefficient
from camber import naca, custom_camber
from circulation import circulation
from tot_circulation import total_circulation
from vector_field import vector_field
from moment_coefficient import moment_coefficient
from slope_camber import slope_camber
from parameter_getter import AirfoilParams


def main():
    
    airfoil = AirfoilParams("config.json")
    airfoil_params = airfoil.get_all()
    
    names = []
    xs = []
    ycs = []
    v_infs = []
    alphas_group = []
    
    for airfoil in airfoil_params:
        name = airfoil.get('name')
        names.append(name)
        option = airfoil.get('option')
        if option == 1:
            camber = airfoil.get('camber')
            position = airfoil.get('position')
            N = airfoil.get('N', 10000)
            x, yc = naca(camber, position, N)
        else:
            f1 = airfoil.get('f1', '0').strip()
            N = airfoil.get('N', 10000)
            x, yc = custom_camber(f1, N)
        v_inf = airfoil.get('v_inf', 20)
        alpha = airfoil.get('alpha')
        v_infs.append(v_inf)
        alphas_group.append(alpha)
        xs.append(x)
        ycs.append(yc)
    
    xs = np.array(xs)
    ycs = np.array(ycs)
    
    # Plotting the mean camber line
    plt.figure(figsize=(10, 6))
    
    for i in range(len(names)):
        plt.plot(xs[i], ycs[i], label=names[i])
    
    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 0.6)
    plt.xlabel('x (chord length)')
    plt.ylabel('y (chord length)')
    plt.title('Mean Camber Line of Airfoil')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Plotting the slope of the mean camber line
    plt.figure(figsize=(10, 6))
    
    for i in range(len(names)):
        x = xs[i]
        yc = ycs[i]
        name = names[i]
        dy_dx = np.array([slope_camber(x, yc, x_val) for x_val in x if slope_camber(x, yc, x_val) is not None])
        x_dash = np.array([x_val for x_val in x if slope_camber(x, yc, x_val) is not None])
        plt.plot(x_dash, dy_dx, label=f'Slope of {name} Mean Camber Line')
        
    plt.xlabel('x (chord length)')
    plt.ylabel('dy/dx')
    plt.title('Slope of Mean Camber Line')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    data = []
    plt.figure(figsize=(10, 6))
    
    # Computing lift and moment coefficients
    for i in range(len(names)):
        x = xs[i]
        yc = ycs[i]
        alphas = alphas_group[i]
        v_inf = v_infs[i]
        cl_form_array = []
        for alpha in alphas:
            cl_form, cl_comp = lift_coefficient(x, yc, alpha, v_inf, num_terms=100)
            data.append({
                'Airfoil': names[i],
                'Alpha (deg)': alpha,
                'Cl (Formula)': cl_form,
                'Cl (Computed)': cl_comp
            })
            cl_form_array.append(cl_form)
        plt.plot(alphas, cl_form_array, label=f'Lift Coefficient for {names[i]}')
    plt.xlabel(r'$\alpha$ (Angle of Attack in degrees)')
    plt.ylabel(r'$C_l$ (Lift Coefficient)')
    plt.title('Lift Coefficient vs Angle of Attack')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    df = pd.DataFrame(data)
    print(df)
    
    for i in range(len(names)):
        x = xs[i]
        yc = ycs[i]
        alpha = 3
        v_inf = v_infs[i]
        name = names[i]
        cm_form, cm_comp = moment_coefficient(x, yc, alpha, v_inf, num_terms=100)
        print(f'Moment coefficient for {name} at alpha obtained using formula = {alpha}: {cm_form}')
        print(f'Computed Moment for {name} coefficient at alpha = {alpha}: {cm_comp}')
        
        gamma_vals, theta = circulation(x, yc, alpha, v_inf, num_terms=100)
        
        # Plotting the velocity field around the airfoil
        X, Y, U, V, v_max, v_min = vector_field(x, yc, gamma_vals, alpha, v_inf)
        mag = np.sqrt(U**2 + V**2)
        
        print(f'Maximum velocity magnitude for {name}: {v_max}')
        print(f'Minimum velocity magnitude for {name}: {v_min}')
        
        plt.figure(figsize=(10, 6))
        plt.quiver(X, Y, U, V, mag, cmap='viridis', scale_units='xy')
        plt.scatter(x, yc, color='red', marker='o', s=1, label='Discrete Vortices')
        plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
        plt.xlabel('x (chord length)')
        plt.ylabel('y (chord length)')
        plt.title(f'Velocity Field Around the {name} Airfoil')
        plt.colorbar(label='Velocity Magnitude')
        plt.legend()
        plt.grid()
        plt.show()
        
        # Plotting the circulation distribution
        plt.plot(theta, gamma_vals, label='Circulation Distribution')
        plt.xlabel('Theta')
        plt.ylabel('Gamma')
        plt.title(f'Circulation Distribution over Theta for {name}')
        plt.grid(True)
        plt.legend()
        plt.show()
        
        # Computing total circulation
        circ_vortex, circ_line = total_circulation(x, gamma_vals, U, V, ds=X[0, 1] - X[0, 0])
        print(f'Total circulation for {name} using vortex filaments at alpha = {alpha}: {circ_vortex}')
        print(f'Total circulation for {name} using line integral at alpha = {alpha}: {circ_line}')
    
if __name__ == "__main__":
    main()