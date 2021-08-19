from docplex.mp.model import Model
from collections import namedtuple
import sys
import json

def readJSONData(jsonFilePath):
    jsonFile = open(jsonFilePath)
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def buildVMTuples(vmsJsonData):
    VMS = [
        (vm['name'], vm['user'], vm['v_storage'], vm['v_CPU'], vm['v_RAM'], vm['v_delayThreshold'])
            for vm in vmsJsonData
    ]

    VM = namedtuple("VM", ["v_name", "v_user","v_storage", "v_CPU", "v_RAM", "v_delayTreshold"])
    return [VM(*v) for v in VMS]


def buildCloudletTuples(cloudletsJsonData):
    CLOUDLETS = [
        (cloudlet['name'], cloudlet['c_storage'], cloudlet['c_CPU'], cloudlet['c_RAM'])
            for cloudlet in cloudletsJsonData
    ]

    Cloudlet = namedtuple("Cloudlet", ["c_name", "c_storage", "c_CPU", "c_RAM"])
    return [Cloudlet(*c) for c in CLOUDLETS]

def buildUsersDict(usersJsonData):
    USERS = [
        (user['name'], user['u_vm'], user['u_cloudlet'])
            for user in usersJsonData
    ]

    User = namedtuple("User", ["user", "u_vm", "u_connected_cloudlet"])
    return [User(*u) for u in USERS]

def buildDelaysDict(delaysJsonData):
    return {
        (cloudlet['source'], cloudlet['destiny']): cloudlet['delay']
            for cloudlet in delaysJsonData
    }

def findDelay(allocatedCloudlet, vm, users, delays):
    for u in users:
        if u.user == vm.v_user:
            return delays[allocatedCloudlet.c_name, u.u_connected_cloudlet]

def printSolution(modelOpt):
    modelOpt.print_information()
    modelOpt.print_solution()

def build(pliOption, jsonFilePath):
    data = readJSONData(jsonFilePath)

    cloudlets = buildCloudletTuples(data['Cloudlets'])
    vms = buildVMTuples(data['VMs'])
    users = buildUsersDict(data['Users'])
    idx = [(n.c_name,v.v_name) for n in cloudlets for v in vms]
    delays = buildDelaysDict(data['DelayBetweenCloudlets'])

    modl = Model(f"p{pliOption}_formulation")

    x = modl.binary_var_dict(idx, name="allocate")

    # storage contraint
    for n in range(0, len(cloudlets)):
        modl.add_constraint(
                modl.sum(
                        vms[v].v_storage*x[cloudlets[n].c_name, vms[v].v_name] 
                            for v in range(0, len(vms))
                ) <= cloudlets[n].c_storage
        , ctname="storageConstr")

    # cpu contraint
    for n in range(0, len(cloudlets)):
        modl.add_constraint(
                modl.sum(
                        vms[v].v_CPU*x[cloudlets[n].c_name, vms[v].v_name] 
                            for v in range(0, len(vms))
                ) <= cloudlets[n].c_CPU
        , ctname="cpuConstr")

    # ram contraint
    for n in range(0, len(cloudlets)):
        modl.add_constraint(
                modl.sum(
                        vms[v].v_RAM*x[cloudlets[n].c_name, vms[v].v_name] 
                            for v in range(0, len(vms))
                ) <= cloudlets[n].c_RAM
        , ctname="ramConstr")

    # allocation constraint: a VM must be allocated (even in cloud), 
    # but only in one place (i.e., a VM must not be allocated in two places)
    for v in range(0, len(vms)):
        modl.add_constraint(
                modl.sum(
                    x[cloudlets[n].c_name, vms[v].v_name] 
                        for n in range(0, len(cloudlets))
                ) == 1
        , ctname="AllocationConst")

    expr = ()
    # objective function
    if pliOption == "1":
        expr = (modl.sum(x[cloudlets[0].c_name, vms[v].v_name] 
            for v in range(0, len(vms))))
    elif pliOption == "2":
        expr = (modl.sum(
            findDelay(cloudlets[n], vms[v], users, delays)*x[cloudlets[n].c_name, vms[v].v_name] 
                for n in range(0, len(cloudlets)) for v in range(0, len(vms))
        ))

    modl.minimize(expr)

    modl.export_as_lp("/home/jps/pli/cplex")
    solution = modl.solve()

    printSolution(modl)

def validateArgs(args):
    if args:
        if args[0] == "1" or args[0] == "2":
            return True
        else:
            return False
    else:
        return False

def main():
    # python formulation_cplex_json.py <1 for PLI 1 or 2 for PLI 2>
    args = sys.argv[1:]
    if validateArgs(args):
        build(args[0], args[1])

if __name__ == "__main__":
    main()