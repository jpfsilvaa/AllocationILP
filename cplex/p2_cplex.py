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
    ("V1", 'U1', 150, 2100, 120, 5000),
    ("V2", 'U1', 150, 2200, 220, 5000),
    ("V3", 'U1', 170, 2300, 320, 5000),
    ("V4", 'U1', 180, 2400, 420, 5000),
    ("V5", 'U1', 190, 2500, 520, 5000)
]

# Tuples for Cloudlet, VM and User for accessing data
Cloudlet = namedtuple("Cloudlet", ["c_name", "c_storage", "c_CPU", "c_RAM"])
VM = namedtuple("VM", ["v_name", "v_user","v_storage", "v_CPU", "v_RAM", "v_delayTreshold"])
User = namedtuple("User", ["user", "u_vm", "u_connected_cloudlet"])

# Connecting the data with the tuple
cloudlets = [Cloudlet(*c) for c in CLOUDLETS]
vms = [VM(*v) for v in VMs]

# Each user has a VM to be executed in some Cloudlet (or Cloud) 
# and he is CONNECTED to a Cloudlet (not necessarily with his VM allocated in) at the moment 't'
USERS = [
    ('U1', vms[0], cloudlets[1]),
    ('U2', vms[1], cloudlets[2]),
    ('U3', vms[2], cloudlets[2]),
    ('U4', vms[3], cloudlets[3]),
    ('U5', vms[4], cloudlets[1]),
]

# Delay between the Cloudlets
# Cn: cloudlet  allocated to the user's vm
# Ct: cloudlet that the user is connected to
# d: delay(ms) between Cn and Ct
DELAY_COMBINATION = {
    (cloudlets[0], cloudlets[0]): 0,
    (cloudlets[0], cloudlets[1]): 30000,
    (cloudlets[0], cloudlets[2]): 35000,
    (cloudlets[0], cloudlets[3]): 33000,
    (cloudlets[1], cloudlets[0]): 30000,
    (cloudlets[1], cloudlets[1]): 0,
    (cloudlets[1], cloudlets[2]): 1500,
    (cloudlets[1], cloudlets[3]): 1200,
    (cloudlets[1], cloudlets[0]): 35000,
    (cloudlets[2], cloudlets[1]): 1500,
    (cloudlets[2], cloudlets[2]): 0,
    (cloudlets[2], cloudlets[3]): 1000,
    (cloudlets[3], cloudlets[0]): 33000,
    (cloudlets[3], cloudlets[1]): 1200,
    (cloudlets[3], cloudlets[2]): 1000,
    (cloudlets[3], cloudlets[3]): 0
}

users = [User(*u) for u in USERS]
idx = [(n.c_name,v.v_name) for n in cloudlets for v in vms]

def findDelay(allocatedCloudlet, vm):
    for u in users:
        if u.user == vm.v_user:
            return DELAY_COMBINATION[allocatedCloudlet, u.u_connected_cloudlet]

modl = Model("Delay minimization")

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
modl.minimize(modl.sum(
        findDelay(cloudlets[n], vms[v])*x[cloudlets[n].c_name, vms[v].v_name] for n in range(0, len(cloudlets)) for v in range(0, len(vms))
    )
)

# export the Linear Program model and solve
modl.export_as_lp("/home/jps/pli/cplex")
solution = modl.solve()

# print solution
modl.print_information()
modl.print_solution()