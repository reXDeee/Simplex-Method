# visualization.py
import matplotlib.pyplot as plt
import numpy as np

def plot_feasible_region(objective_coeffs, constraints, solution):
    if len(objective_coeffs) != 2:
        return  # Visualization is only for 2-variable problems

    x1_vals = np.linspace(0, 20, 400)  # Adjust range as needed
    x2_vals = np.linspace(0, 20, 400)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    plt.figure(figsize=(8, 6))

    # Plot constraints
    for constr in constraints:
        coeffs = constr['coefficients']
        relation = constr['relation']
        rhs = constr['rhs']

        if len(coeffs) != 2:
            continue  # Skip constraints that don't have exactly 2 coefficients

        lhs = coeffs[0]*X1 + coeffs[1]*X2
        if relation == '<=':
            plt.contourf(X1, X2, lhs <= rhs, alpha=0.2)
        elif relation == '>=':
            plt.contourf(X1, X2, lhs >= rhs, alpha=0.2)
        else:
            plt.contour(X1, X2, lhs, levels=[rhs], colors='black')

    # Plot objective function
    z = objective_coeffs[0]*X1 + objective_coeffs[1]*X2
    plt.contour(X1, X2, z, levels=20, cmap='viridis', alpha=0.5)

    # Plot optimal solution
    x_sol = [solution['x1'], solution['x2']]
    plt.plot(x_sol[0], x_sol[1], 'ro', label='Optimal Solution')

    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Feasible Region and Optimal Solution')
    plt.legend()
    plt.grid(True)
    plt.show()
