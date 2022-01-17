from gurobipy import *
import sys
import json

def readJSONData(jsonFilePath):
    jsonFile = open(jsonFilePath)
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def buildVMsDict(vmsJsonData):
    return multidict(
        (vm['name'], [vm['user'], vm['v_storage'], vm['v_CPU'], vm['v_RAM'], vm['v_delayThreshold']])
            for vm in vmsJsonData
    )

def buildCloudletsDict(cloudletsJsonData):
    return multidict(
        (cloudlet['name'], [cloudlet['c_storage'], cloudlet['c_CPU'], cloudlet['c_RAM']])
            for cloudlet in cloudletsJsonData
    )

def buildUsersDict(usersJsonData):
    return multidict(
        (user['name'], [user['u_vm'], user['u_cloudlet']])
            for user in usersJsonData
    )

def buildDelaysDict(delaysJsonData):
    return multidict(
        ((cloudlet['source'], cloudlet['destiny']), cloudlet['delay'])
            for cloudlet in delaysJsonData
    )

def findUserCloudletByVM(u_cloudlet, v_user, vm):
    return u_cloudlet[v_user[vm]]

# Display optimal values of decision variables
def printSolution(modelOpt):
    for v in modelOpt.getVars():
        if (abs(v.x) > 1e-6):
            print(v.varName, v.x)

def build(pliOption, jsonFilePath, outFilePath):
    data = readJSONData(jsonFilePath)

    v_names, v_user, v_storage, v_CPU, v_RAM, v_delayThreshold = buildVMsDict(data['VMs'])
    c_names, c_storage, c_CPU, c_RAM = buildCloudletsDict(data['Cloudlets'])
    users, u_vm, u_cloudlet = buildUsersDict(data['Users'])
    combinations, delay = buildDelaysDict(data['DelayBetweenCloudlets'])

    m = Model('Cloudlet-VM Allocation')
    x = m.addVars(c_names, v_names, vtype=GRB.BINARY, name="allocate")

    # storage constraint
    for n in c_names:
        m.addConstr((
            quicksum(v_storage[v]*x[n,v] for v in v_names) <= c_storage[n]
        ), name='storage[%s]'%n)

    # CPU constraint
    for n in c_names:
        m.addConstr((
            quicksum(v_CPU[v]*x[n,v] for v in v_names) <= c_CPU[n]
        ), name='CPU[%s]'%n)

    # RAM constraint
    for n in c_names:
        m.addConstr((
            quicksum(v_RAM[v]*x[n,v] for v in v_names) <= c_RAM[n]
        ), name='RAM[%s]'%n)

    # allocation constraint: a VM must be allocated (even in cloud), 
    # but only in one place (i.e., a VM must not be allocated in two places)
    for v in v_names:
        m.addConstr((
            quicksum(x[n,v] for n in c_names) == 1
        ), name='allocate[%s]'%v)

    if pliOption == "1":
        expr = (x.sum(c_names[0], '*'))
    elif pliOption == "2":
        expr = (quicksum(delay[n, findUserCloudletByVM(u_cloudlet, v_user, v)]*x[n,v] for n in c_names for v in v_names))

    m.setObjective(expr, GRB.MINIMIZE)

    fileName = f"{outFilePath}/p{pliOption}_formulation.lp"
    m.write(fileName)

    m.optimize()
    printSolution(m)
    
def validateArgs(args):
    if args:
        if args[0] == "1" or args[0] == "2":
            return True
        else:
            return False
    else:
        return False

def main():
    # python formulation_gurobi_json.py <1 for PLI 1 or 2 for PLI 2> <json file path> <out file path directory>
    args = sys.argv[1:]
    if validateArgs(args):
        build(args[0], args[1], args[2])

if __name__ == "__main__":
    main()