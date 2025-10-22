import json
import pandas as pd
import numpy as np
import gurobipy as gp
from gurobipy import GRB

with open("C:/Users/ThierryJoëlSANT'ANNA/data/data/portfolio-example.json", "r") as f:
    data = json.load(f)

n = data["num_assets"]
sigma = np.array(data["covariance"])
mu = np.array(data["expected_return"])
mu_0 = data["target_return"]
k = data["portfolio_max_size"]


with gp.Model("portfolio") as model:
    # Name the modeling objects to retrieve them
    # ...
    indices = range(n)
    x = model.addVars (indices, vtype = GRB.CONTINUOUS, name ="x" )
    y = model.addVars (indices, vtype = GRB.BINARY, name ="y" )
    
    vp = 0
    for i in indices :
        for j in indices : 
            vp += sigma[i][j]*x[i]*x[j]
     
    
    model.setObjective(vp, GRB.MINIMIZE)
    
    
    somme = 0
    for i in indices :
        somme += x[i]*mu[i]
    model.addConstr(somme >= mu_0, name = "c1")
    for i in indices :
        model.addConstr(x[i] <= y[i], name = "c4")
    model.addConstr(x.sum() == 1, name = "c2")
    model.addConstr(y.sum() <= k, name = "c3")
   

    model.optimize()

    # Write the solution into a DataFrame
    # portfolio = [var.X for var in model.getVars() if "x" in var.VarName]
    # risk = model.ObjVal
    
    # expected_return = model.getRow(model.getConstrByName("return")).getValue()
    # df = pd.DataFrame(
    #     data=portfolio + [risk, expected_return],
    #     index=[f"asset_{i}" for i in range(n)] + ["risk", "return"],
    #     columns=["Portfolio"],
    #)
    # print(df)
