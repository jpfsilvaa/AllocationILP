from gurobipy import *
import sys
import json
import time

def readJSONData(jsonFilePath):
    jsonFile = open(jsonFilePath)
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def buildVMsDict(vmsJsonData):
    return multidict(
        (vm['id'], [vm['bid'], vm['v_storage'], vm['v_CPU'], vm['v_RAM']])
            for vm in vmsJsonData
    )

def buildCloudletsDict(cloudletsJsonData):
    return multidict(
        (cloudlet['id'], [cloudlet['c_storage'], cloudlet['c_CPU'], cloudlet['c_RAM']])
            for cloudlet in cloudletsJsonData
    )

# Display optimal values of decision variables
def printSolution(modelOpt):
    numAlloc = 0
    for v in modelOpt.getVars():
        if (abs(v.x) > 1e-6):
            numAlloc += 1
            print(v.varName, v.x)
    print("num allocated users:", numAlloc)
    print("social welfare:", modelOpt.objVal)

def build(jsonFilePath):
    data = readJSONData(jsonFilePath)

    v_ids, v_bid, v_storage, v_CPU, v_RAM = buildVMsDict(data['UserVMs'])
    c_ids, c_storage, c_CPU, c_RAM = buildCloudletsDict(data['Cloudlets'])

    m = Model('Cloudlet-VM Allocation')
    x = m.addVars(c_ids, v_ids, vtype=GRB.BINARY, name="allocate")

    # storage constraint
    for n in c_ids:
        m.addConstr((
            quicksum(v_storage[v]*x[n,v] for v in v_ids) <= c_storage[n]
        ), name='storage[%s]'%n)

    # CPU constraint
    for n in c_ids:
        m.addConstr((
            quicksum(v_CPU[v]*x[n,v] for v in v_ids) <= c_CPU[n]
        ), name='CPU[%s]'%n)

    # RAM constraint
    for n in c_ids:
        m.addConstr((
            quicksum(v_RAM[v]*x[n,v] for v in v_ids) <= c_RAM[n]
        ), name='RAM[%s]'%n)

    expr = (quicksum(v_bid[v]*x[n,v] for n in c_ids for v in v_ids))

    m.setObjective(expr, GRB.MAXIMIZE)

    # fileName = "/home/jps/allocation_models/greedy_vs_exact/exact_formulation.lp"
    # m.write(fileName)

    startTime = time.time()
    m.optimize()
    endTime = time.time()
    optResult = getResult()
    printSolution(m)
    print('execution time:', (endTime-startTime))
    print('prices->', pricing())

def getResult():
    ILPResult = dict()
    

def pricing():
    socialWelfareValue = 0
    clarkeValue = 0
    

def main():    
    jsonFilePath = '/home/jps/allocation_models/greedy_vs_exact/instances/vGama/clE.json'    
    build(jsonFilePath)

if __name__ == "__main__":
    main()