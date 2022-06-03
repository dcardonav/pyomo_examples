import pyomo.environ as pyo
import pyomo.opt

def IC_model(A, h, d, c, b, u):

    model = pyo.ConcreteModel(name='(H)')

    def x_bounds(m, i):
        return (0, u[i])
    model.x = pyo.Var(A, bounds=x_bounds)

    def z_rule(model):
        return sum(h[i] * (model.x[i] - (model.x[i]/d[i])**2) for i in A)

    model.z = pyo.Objective(rule=z_rule, sense=pyo.maximize)
    model.budgetconstr = pyo.Constraint(expr=sum(c[i]*model.x[i] for i in A) <= b)

    return model


def IC_model_dict(ICD):

    model = pyo.ConcreteModel(name="(H)")

    model.A = pyo.Set(initialize=ICD["A"])

    model.h = pyo.Param(model.A, initialize=ICD["h"])
    model.d = pyo.Param(model.A, initialize=ICD["d"])
    model.c = pyo.Param(model.A, initialize=ICD["c"])
    model.b = pyo.Param(initialize=ICD["b"])
    model.u = pyo.Param(model.A, initialize=ICD["u"])

    def xbounds_rule(model, i):
        return (0, model.u[i])

    model.x = pyo.Var(model.A, bounds=xbounds_rule)

    def obj_rule(model):
        return sum(model.h[i] * (model.x[i] - (model.x[i]/model.d[i])**2) \
                   for i in model.A)

    model.z = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

    def budget_rule(model):
        return sum(model.c[i]*model.x[i] for i in model.A) <= model.b

    model.budgetconstr = pyo.Constraint(rule=budget_rule)

    return model

if __name__ == '__main__':
    ICD = {
        "A" : ['IC_Scoops', 'Peanuts'],
        "h" : {'IC_Scoops':1, 'Peanuts':0.1},
        "d" : {'IC_Scoops': 5, 'Peanuts': 27},
        "c" : {'IC_Scoops': 3.14, 'Peanuts': 0.2718},
        "u" : {'IC_Scoops': 100, 'Peanuts': 40.6},
        "b" : 12
    }

    model = IC_model_dict(ICD)
    opt = pyo.SolverFactory('gurobi')
    results = opt.solve(model)
    pyo.assert_optimal_termination(results)

    model.display()