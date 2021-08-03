from docplex.mp.model import Model
from collections import namedtuple
from sys import stdout

# Initializing data
# Cloud (c0) and cloudlets
# units: storage(MB), cpu(MIPS), RAM(MB)
CLOUDLETS = [
    ("C0", 500000, 3000000, 120000),
    ("C1", 510, 3100, 420),
    ("C2", 520, 3100, 420),
    ("C3", 530, 5300, 680)
]

# units: storage(MB), cpu(MIPS), RAM(MB), delayThreshold(ms)
VMs = [
    ("V1", 150, 2100, 120, 5000),
    ("V2", 150, 2200, 220, 5000),
    ("V3", 170, 2300, 320, 5000),
    ("V4", 180, 2400, 420, 5000),
    ("V5", 190, 2500, 520, 5000)
]

# Data tuple
Cloudlet = namedtuple("Cloudlet", ["c_name", "c_storage", "c_CPU", "c_RAM"])
VM = namedtuple("VM", ["v_name", "v_storage", "v_CPU", "v_RAM", "v_delayTreshold"])

# COnnecting the data with the tuple
cloudlets = [Cloudlet(*c) for c in CLOUDLETS]
vms = [VM(*v) for v in VMs]
idx = [(n.c_name,v.v_name) for n in cloudlets for v in vms]

modl = Model("Cloudlet-VM Allocation")

# creating variables
x = modl.binary_var_dict(idx, name="allocate")

# storage contraint
for n in range(0, len(cloudlets)):
    modl.add_constraint(
            modl.sum(
                    vms[v].v_storage*x[cloudlets[n].c_name, vms[v].v_name] for v in range(0, len(vms))
            ) <= cloudlets[n].c_storage
    , ctname="storageConstr")

# cpu contraint
for n in range(0, len(cloudlets)):
    modl.add_constraint(
            modl.sum(
                    vms[v].v_CPU*x[cloudlets[n].c_name, vms[v].v_name] for v in range(0, len(vms))
            ) <= cloudlets[n].c_CPU
    , ctname="cpuConstr")

# ram contraint
for n in range(0, len(cloudlets)):
    modl.add_constraint(
            modl.sum(
                    vms[v].v_RAM*x[cloudlets[n].c_name, vms[v].v_name] for v in range(0, len(vms))
            ) <= cloudlets[n].c_RAM
    , ctname="ramConstr")

# allocation constraint: a VM must be allocated (even in cloud), 
# but only in one place (i.e., a VM must not be allocated in two places)
for v in range(0, len(vms)):
    modl.add_constraint(
            modl.sum(
                x[cloudlets[n].c_name, vms[v].v_name] for n in range(0, len(cloudlets))
            ) == 1
    , ctname="AllocationConst")

# objective function
modl.minimize(modl.sum(x[cloudlets[0].c_name, vms[v].v_name] for v in range(0, len(vms))))

# export the Linear Program model and solve
modl.export_as_lp("/home/jps/pli/cplex")
solution = modl.solve()

# print solution
modl.print_information()
modl.print_solution()