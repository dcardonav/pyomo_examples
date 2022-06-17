import pandas as pd
import pyomo.environ as pyo

from wl_concrete import create_warehouse_model

df = pd.read_excel('data.xlsx', 'Sheet1', header=0, index_col=0)

N = list(df.index.map(str))
M = list(df.columns.map(str))
d = {(r, c):df.at[r, c] for r in N for c in M}
P = 2

model = create_warehouse_model(N, M, d, P)

solver = pyo.SolverFactory('glpk')
solver.solve(model)
model.y.pprint()

