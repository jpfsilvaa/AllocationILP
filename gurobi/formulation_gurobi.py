from gurobipy import *
import sys

PLI_USAGE = "Insert right argument: <1 or 2> representing PLI 1 or PLI 2" 
SWITCH_PLI = 1 #1 FOR p1 and 2 for p2

# Cloud (c0) and cloudlets
# units: storage(MB), cpu(MIPS), RAM(MB)
cloudlets, c_storage, c_CPU, c_RAM = multidict({
    'c0': [500000, 3000000, 120000],
    'c1': [510, 3100, 420],
    'c2': [520, 3200, 540],
    'c3': [530, 5300, 680]
})

# units: storage(MB), cpu(MIPS), RAM(MB), delayThreshold(ms)
VMs, v_user, v_storage, v_CPU, v_RAM, v_delayThreshold = multidict({
    'v1': ['u1', 150, 2100, 120, 5000],
    'v2': ['u2', 150, 2200, 220, 5000],
    'v3': ['u3', 170, 2300, 320, 5000],
    'v4': ['u4', 180, 2400, 420, 5000],
    'v5': ['u5', 190, 2500, 520, 5000]
})

# Each user has a VM to be executed in some Cloudlet (or Cloud) 
# and he is CONNECTED to a Cloudlet (not necessarily with his VM allocated in) at the moment 't'
user, u_vm, u_cloudlet = multidict({
    'u1':  [VMs[0], cloudlets[1]],
    'u2':  [VMs[1], cloudlets[2]],
    'u3':  [VMs[2], cloudlets[2]],
    'u4':  [VMs[3], cloudlets[3]],
    'u5':  [VMs[4], cloudlets[1]]
})

# Delay between the Cloudlets (n, ct): d
# n: cloudlet  allocated to the user's vm
# ct: cloudlet that the user is connected to
# d: delay(ms) between n and ct
combination, delay = multidict({
    (cloudlets[0], cloudlets[0]): 0,
    (cloudlets[0], cloudlets[1]): 30000,
    (cloudlets[0], cloudlets[2]): 35000,
    (cloudlets[0], cloudlets[3]): 33000,
    (cloudlets[1], cloudlets[0]): 30000,
    (cloudlets[1], cloudlets[1]): 0,
    (cloudlets[1], cloudlets[2]): 1500,
    (cloudlets[1], cloudlets[3]): 1200,
    (cloudlets[2], cloudlets[0]): 35000,
    (cloudlets[2], cloudlets[1]): 1500,
    (cloudlets[2], cloudlets[2]): 0,
    (cloudlets[2], cloudlets[3]): 1000,
    (cloudlets[3], cloudlets[0]): 33000,
    (cloudlets[3], cloudlets[1]): 1200,
    (cloudlets[3], cloudlets[2]): 1000,
    (cloudlets[3], cloudlets[3]): 0
})

m = Model('Cloudlet-VM Allocation')
x = m.addVars(cloudlets, VMs, vtype=GRB.BINARY, name="allocate")

def defineVarAndConstrs():
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
    for v in VMs:
        m.addConstr((
            quicksum(x[n,v] for n in cloudlets) == 1
        ), name='allocate[%s]'%v)

def findUserCloudletByVM(vm):
    return u_cloudlet[v_user[vm]]

def optimizeAndWrite(pliOption):
    expr = None

    if pliOption == "1":
        expr = (x.sum(cloudlets[0], '*'))
    elif pliOption == "2":
        expr = (quicksum(delay[n, findUserCloudletByVM(v)]*x[n,v] for n in cloudlets for v in VMs))

    m.setObjective(expr, GRB.MINIMIZE)

    fileName = f"/home/jps/pli/gurobi/p{pliOption}_formulation.lp"
    m.write(fileName)

    m.optimize()
    printSolution()

# Display optimal values of decision variables
def printSolution():
    for v in m.getVars():
        if (abs(v.x) > 1e-6):
            print(v.varName, v.x)

def validateArgs(args):
    if args:
        if args[0] == "1" or args[0] == "2":
            return True
        else:
            return False
    else:
        return False

def main():
    args = sys.argv[1:]
    if validateArgs(args):
        defineVarAndConstrs()
        optimizeAndWrite(pliOption=args[0])
    

if __name__ == "__main__":
    main()
