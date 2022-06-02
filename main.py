# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyomo.environ as pyo

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    model = pyo.ConcreteModel()
    model.x_1 = pyo.Var(within=pyo.NonNegativeReals)
    model.x_2 = pyo.Var(within=pyo.NonNegativeReals)
    model.obj = pyo.Objective(expr=model.x_1 + 2*model.x_2)
    model.con_1 = pyo.Constraint(expr=3*model.x_1 + 4*model.x_2 >= 1)
    model.con_2 = pyo.Constraint(expr=2*model.x_1 + 5*model.x_2 >= 1)

    opt = pyo.SolverFactory('gurobi')
    results = opt.solve(model)
    pyo.assert_optimal_termination(results)
    model.display()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
