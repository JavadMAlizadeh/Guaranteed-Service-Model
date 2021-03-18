
#Multi-echelon Inventory Systems
#Guaranteed-service Model
#Serial System

import gurobipy as gp
from gurobipy import GRB
import math

from random import seed
from random import randint

mu = 100
sigma = 25
z = 1.645
numEchelon = 50

H = {}
L = {}

seed(1)
for j in range(numEchelon):
    H[j] = randint(5, 25)

for j in range(numEchelon):
    L[j] = randint(5, 15)

m = gp.Model()

S_in = {}
S_out = {}
Tau = {}
X = {}
S = {}

for j in range(numEchelon):
    S_in[j] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="S_in%g" % j)
    S_out[j] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="S_out%g" % j)
    Tau[j] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Tau%g" % j)
    X[j] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="X%g" % j)

m.addConstr(S_in[0] <= 0)
m.addConstr(S_out[numEchelon - 1] <= 0)

for j in range(numEchelon - 1):
    m.addConstr(S_out[j] <= S_in[j + 1])

for j in range(numEchelon):
    m.addConstr(Tau[j] == S_in[j] + L[j] - S_out[j])

for j in range(numEchelon):
    m.addConstr(S_out[j] - S_in[j] <= L[j])

m.params.NonConvex = 2

for j in range(numEchelon):
    m.addQConstr(Tau[j], GRB.EQUAL, X[j] * X[j])

m.setObjective(gp.quicksum(z * sigma * H[j] * X[j] for j in range(numEchelon)), GRB.MINIMIZE)

m.optimize()


def printSolution():
    if m.status == GRB.Status.OPTIMAL:
        objVal = sum(z * sigma * H[j] * math.sqrt(Tau[j].x) for j in range(numEchelon))
        print('\nTotal Cost (Solution): %g' % m.objVal)
        print('Total Cost (Correct): ', objVal)
        print('\nSolution:')
        for j in range(numEchelon):
            S[j] = mu * Tau[j].x + z * sigma * math.sqrt(Tau[j].x)
            print('S_in[%s]:%g' % (j, S_in[j].x))
            print('S_out[%s]:%g' % (j, S_out[j].x))
            print('X[%s]:%g' % (j, X[j].x))
            print('Tau[%s]:%g' % (j, Tau[j].x))
            print('S[%s]:%g' % (j, S[j]))


printSolution()
