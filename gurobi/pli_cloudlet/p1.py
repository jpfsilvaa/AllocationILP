from gurobipy import *
from dataclasses import dataclass

# Cloud (c0) and cloudlets
# units: storage(MB), cpu(MIPS), RAM(MB)
cloudlets, c_storage, c_CPU, c_RAM = multidict({
    'c0': [500000, 3000000, 120000],
    'c1': [510, 3100, 420],
    'c2': [520, 3200, 540],
    'c3': [530, 5300, 680]
})

# units: storage(MB), cpu(MIPS), RAM(MB), delayThreshold(ms)
VMs, v_storage, v_CPU, v_RAM, v_delayThreshold = multidict({
    'v1': [150, 2100, 120, 5000],
    'v2': [150, 2200, 220, 5000],
    'v3': [170, 2300, 320, 5000],
    'v4': [180, 2400, 420, 5000],
    'v5': [190, 2500, 520, 5000],
})

m = Model('Cloudlet Resource Allocation')

# decision variables
x = m.addVars(cloudlets, VMs, vtype=GRB.BINARY, name="allocate")

# storage constraint
for n in cloudlets:
    m.addConstr((
        quicksum(v_storage[v]*x[n,v] for v in VMs) <= c_storage[n]
    ), name='storage[%s]'%n)

# CPU constraint
for n in cloudlets:
    m.addConstr((
        quicksum(v_CPU[v]*x[n,v] for v in VMs) <= c_CPU[n]
    ), name='CPU[%s]'%n)

# RAM constraint
for n in cloudlets:
    m.addConstr((
        quicksum(v_RAM[v]*x[n,v] for v in VMs) <= c_RAM[n]
    ), name='RAM[%s]'%n)

# allocation constraint: a VM must be allocated (even in cloud), 
# but only in one place (i.e., a VM must not be allocated in two places)
allocationConstr = m.addConstrs((x.sum('*', v) == 1 for v in VMs), 'allocate')

# objective function
m.setObjective((x.sum(cloudlets[0], '*')), GRB.MINIMIZE)
m.write('gurobi/pli_cloudlet/RA.lp')

# Run the optimization engine
m.optimize()

# Display optimal values of decision variables
for v in m.getVars():
    if (abs(v.x) > 1e-6):
        print(v.varName, v.x)