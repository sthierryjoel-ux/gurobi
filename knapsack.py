
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def generate_knapsack(num_items):
    # Fix seed value
    rng = np.random.default_rng(seed=150)
    # Item values, weights
    values = rng.uniform(low=1, high=25, size=num_items)
    weights = rng.uniform(low=5, high=100, size=num_items)
    # Knapsack capacity
    capacity = 0.7 * weights.sum()

    return values, weights, capacity


def solve_knapsack_model(values, weights, capacity):
    num_items = len(values)
    # Turn values and weights numpy arrays to dict
    # ...
    values_dict = {i: v for i, v in enumerate(values)}
    weights_dict = {i: v for i, v in enumerate(weights)}

    with gp.Env() as env:
        with gp.Model(name="knapsack", env=env) as model:
            # Define decision variables using the Model.addVars() method
            indices = range(num_items)
            x = model.addVars(indices, vtype=GRB.BINARY, name="x")

            # Define objective function using the Model.setObjective() method
            # Build the LinExpr using the tupledict.prod() method

            expr = x.prod(values_dict)

            model.setObjective(expr, GRB.MAXIMIZE)

            # Define capacity constraint using the Model.addConstr() method
            contr = x.prod(weights_dict)

            model.addConstr(contr <= capacity, name="c")

            model.optimize()


data = generate_knapsack(10000)
solve_knapsack_model(*data)
