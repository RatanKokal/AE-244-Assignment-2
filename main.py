import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from camber import naca, custom_camber
from circulation import circulation
from vector_field import vector_field
import traceback

# Global variables for colorbar reference and fixed colormap scaling
cbar = None
vmax_global = None

def update_plots(*args):
    global cbar, vmax_global  # Use global colorbar reference and max velocity
    try:
        option = option_var.get()
        v_inf = v_inf_slider.get()
        alpha = alpha_slider.get()
        N = 10000
        
        if option == 1:
            max_camber = float(max_camber_entry.get())
            pos = float(pos_entry.get())
            x, yc = naca(max_camber, pos, N)
        else:
            equation = equation_entry.get().strip()
            x, yc = custom_camber(equation, N)
        
        # Clear and plot mean camber line
        ax1.clear()
        ax1.plot(x, yc, label='Camber Line')
        ax1.set_title('Mean Camber Line')
        ax1.set_ylim(-0.2, 0.6)  # Set y-limits
        
        # Add airflow direction vector ending at the leading edge
        leading_x, leading_y = x[0], yc[0]
        vector_length = 0.1  # Length of airflow vector
        start_x = leading_x - vector_length * np.cos(np.radians(alpha))  # Start before leading edge
        start_y = leading_y - vector_length * np.sin(np.radians(alpha))
        ax1.arrow(start_x, start_y, leading_x - start_x, leading_y - start_y, head_width=0.015, head_length=0.015, fc='green', ec='green', label='Airflow Direction')
        
        ax1.legend()
        
        # Clear and plot velocity field
        ax2.clear()
        gamma_vals, theta = circulation(x, yc, alpha, v_inf, num_terms=100)
        X, Y, U, V, _, _ = vector_field(x, yc, gamma_vals, alpha, v_inf, grid_size=(80, 60))
        mag = np.sqrt(U**2 + V**2)
        
        # Update global vmax if necessary
        if vmax_global is None or np.max(mag) > vmax_global:
            vmax_global = np.max(mag)
        
        ax2.quiver(X, Y, U, V, mag, cmap='viridis', scale_units='xy')
        ax2.scatter(x, yc, color='red', marker='o', s=1, label='Discrete Vortices')
        ax2.axhline(0, color='black', linestyle='--', linewidth=0.5)
        ax2.set_title(f'Velocity Field Around the Airfoil')

        # Update or create colorbar with fixed scaling from 0 to vmax_global
        if cbar is None:
            cbar = fig.colorbar(plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=vmax_global)), ax=ax2, label='Velocity Magnitude')
        else:
            cbar.update_normal(plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=vmax_global)))

        ax2.legend()
        canvas.draw()
    except Exception as e:
        error_label.config(text=f'Error: {str(e)}')
        traceback.print_exc()  # Print full error details to the console

# Initialize Tkinter window
root = tk.Tk()
root.title("Airfoil Analysis GUI")
root.geometry("1000x800")  # Adjusted for vertical layout

# Frames for layout
frame_top = tk.Frame(root)
frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame_middle = tk.Frame(root)
frame_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame_bottom = tk.Frame(root)
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X)

# Create Matplotlib figure with two subplots (stacked vertically)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=frame_top)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Add Matplotlib navigation toolbar for zooming
toolbar = NavigationToolbar2Tk(canvas, frame_top)
toolbar.update()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Radio buttons for selection
option_var = tk.IntVar(value=1)
tk.Radiobutton(frame_bottom, text="Use NACA Parameters", variable=option_var, value=1).pack(side=tk.LEFT)
tk.Radiobutton(frame_bottom, text="Use Custom Equation", variable=option_var, value=2).pack(side=tk.LEFT)

# Entry for NACA parameters
max_camber_entry = tk.Entry(frame_bottom, width=10)
max_camber_entry.pack(side=tk.LEFT)
max_camber_entry.insert(0, "0.02")

pos_entry = tk.Entry(frame_bottom, width=10)
pos_entry.pack(side=tk.LEFT)
pos_entry.insert(0, "0.4")

# Sliders for velocity and angle of attack (Real-time updates)
v_inf_slider = tk.Scale(frame_bottom, from_=1, to=100, orient=tk.HORIZONTAL, label="Velocity (V_inf)", command=lambda _: update_plots())
v_inf_slider.pack(side=tk.LEFT)
v_inf_slider.set(20)

alpha_slider = tk.Scale(frame_bottom, from_=-10, to=20, orient=tk.HORIZONTAL, label="Angle of Attack (Alpha)", command=lambda _: update_plots())
alpha_slider.pack(side=tk.LEFT)
alpha_slider.set(5)

# Entry for custom equation
equation_entry = tk.Entry(frame_bottom, width=20)
equation_entry.pack(side=tk.LEFT)
equation_entry.insert(0, "x**2")

# Update button
update_button = tk.Button(frame_bottom, text="Update Plots", command=update_plots)
update_button.pack(side=tk.LEFT)

# Error message label
error_label = tk.Label(frame_bottom, text="", fg="red")
error_label.pack(side=tk.LEFT)

root.mainloop()
