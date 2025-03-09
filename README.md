
# AE 244 Assignment 2

This project is designed to analyze the aerodynamic properties of airfoils using various computational methods. The project includes functions to compute the mean camber line, circulation distribution, lift coefficient, moment coefficient, and the velocity field around the airfoil.

## Project Structure
### Role of Each File

- **camber.py**: Contains functions to generate the mean camber line for NACA and custom airfoils.
- **circulation.py**: Computes the circulation distribution using Fourier coefficients.
- **fourier_coefficients.py**: Computes the Fourier coefficients for the mean camber line.
- **config.json**: Contains input parameters for the analysis.
- **lift_coefficient.py**: Computes the lift coefficient from Fourier coefficients and circulation.
- **main.py**: Main script to run the analysis, plot results, and display outputs.
- **moment_coefficient.py**: Computes the moment coefficient from Fourier coefficients and circulation.
- **parameter_getter.py**: Reads parameters from a json file.
- **slope_camber.py**: Computes the slope of the mean camber line at a given x-coordinate.
- **tot_circulation.py**: Computes the total circulation by integrating gamma over theta.
- **vector_field.py**: Computes the vector field around the airfoil using discrete vortex summation.

## How to Run the Project

1. **Install Dependencies**:
    Ensure you have the following dependencies installed:
    - `pandas`
    - `numpy`
    - `sympy`
    - `matplotlib`

    You can install them using pip:
    ```sh
    pip install numpy sympy matplotlib pandas
    ```

2. **Prepare Input File**:
    Edit the [config.json](./config.json) file to set the desired parameters for the analysis.
    To add a new airfoil just add a new set of braces and paramters inside it, if option 1 is chosen f1 can be null and if option 2 is chosen camber and position can be null.
    
    Parameters :
    - name : Name of the airfoil
    - option : 1 for NACA airfoil and 2 for custom
    - f1 : function of mean camber line if custom chosen
    - camber : Camber of desired NACA airfoil
    - position : Position of max camber of desired NACA Airfoil
    - N : Number of points to be chosen for sampling along chord length
    - alpha : Angle of attack in degrees
    - v_inf : Freestream velocity in m/s

3. **Run the Main Script**:
    Execute the [main.py](./main.py) script to run the analysis and generate plots:
    ```sh
    python main.py
    ```

## Dependencies

- [numpy](http://_vscodecontentref_/16): For numerical computations.
- [sympy](http://_vscodecontentref_/17): For symbolic mathematics.
- [matplotlib](http://_vscodecontentref_/18): For plotting graphs and visualizations.
- [pandas](http://_vscodecontentref_/19) : For beter presentation.

## Example

To run the project with the default parameters in [config.json](./config.json), simply execute:
```sh
python main.py