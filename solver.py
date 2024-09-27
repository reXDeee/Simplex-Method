# solver.py
import pulp

def solve_lp(objective_coeffs, problem_type, constraints):
    # Define the problem
    if problem_type == 'Maximize':
        prob = pulp.LpProblem('LP_Problem', pulp.LpMaximize)
    else:
        prob = pulp.LpProblem('LP_Problem', pulp.LpMinimize)

    # Decision variables
    num_vars = len(objective_coeffs)
    var_names = [f'x{i+1}' for i in range(num_vars)]
    x = [pulp.LpVariable(var_names[i], lowBound=0) for i in range(num_vars)]  # Assuming variables >= 0

    # Objective function
    prob += pulp.lpDot(objective_coeffs, x)

    # Constraints
    for constr in constraints:
        lhs = pulp.lpDot(constr['coefficients'], x)
        if constr['relation'] == '<=':
            prob += lhs <= constr['rhs']
        elif constr['relation'] == '>=':
            prob += lhs >= constr['rhs']
        else:
            prob += lhs == constr['rhs']

    # Solve the problem
    prob.solve()

    # Check the solution status
    if prob.status != pulp.LpStatusOptimal:
        raise ValueError("No optimal solution found.")

    # Extract the solution
    solution = {v.name: v.varValue for v in prob.variables()}
    objective_value = pulp.value(prob.objective)

    return solution, objective_value
