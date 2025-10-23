import json
import gurobipy as gp
from gurobipy import GRB
from pathlib import Path

# ----- Load data from JSON -----
with open("C:/Users/ThierryJoëlSANT'ANNA/data/data/lot_sizing_data.json", "r") as f:
    data = json.load(f)

name = data["name"]
H    = int(data["H"])
d    = [float(val) for val in data["demand"]]
c    = [float(val) for val in data["var_cost"]]
f    = [float(val) for val in data["setup_cost"]]
h    = [float(val) for val in data["hold_cost"]]
Qmin = float(data["Qmin"])




Qmax = float(data["Qmax"])
I0   = float(data["I0"])

# Basic validation
assert len(d) == H and len(c) == H and len(f) == H and len(h) == H
assert 0 <= Qmin <= Qmax

# ----- Build model -----
with gp.Env() as env, gp.Model(name, env=env) as model:
    
    indices = range(H)
    

    # Variables de décision
    x = model.addVars(indices, lb = 0, ub = Qmax, name = "x")
    y = model.addVars(indices, vtype=GRB.BINARY, name = "y")
    I = model.addVars(indices, lb = 0, name = "I")
    
    #model.addConstr(I[0] == I0)
    
    
    expr = 0
    for i in range(H):
        expr += c[i]*x[i] + f[i]*y[i] + h[i]*I[i]
    model.setObjective(expr, GRB.MINIMIZE)
    
    # Constraints    
    for i in range (H) : 
        model.addConstr(x[i] <= Qmax*y[i], name = "")
        model.addConstr(x[i] >= Qmin*y[i], name = "")
       
    # for i in range (H-1) :
    #     model.addConstr(I[i+1] == I[i]+x[i+1]-d[i+1], name = "")
        
        
        # Inventory balance
    for t in range(H):
        prev_I = I0 if t == 0 else I[t-1]
        model.addConstr(prev_I + x[t] - d[t] == I[t], name=f"balance[{t}]")
        
    
    # Optimize
    model.write("lot-sizing.lp")
    model.optimize()

    if model.SolCount:
        assert model.ObjVal == 1198.5
        print(f"Total cost = {model.ObjVal:.2f}")
        for t in range(H):
            print(f"t={t:2d}: y={int(y[t].X)} x={x[t].X:.1f} I={I[t].X:.1f}")

