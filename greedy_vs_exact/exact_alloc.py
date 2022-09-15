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
            print(str(v.varName)[-4:-1].replace(',', ''), end=', ')
    print("\nnum allocated users:", numAlloc)
    print("social welfare:", modelOpt.objVal)

def build(jsonFilePath):
    data = readJSONData(jsonFilePath)

    v_ids, v_bid, v_storage, v_CPU, v_RAM = buildVMsDict(data['UserVMs'])
    c_ids, c_storage, c_CPU, c_RAM = buildCloudletsDict(data['Cloudlets'])

    m = Model('Cloudlet-VM Allocation')
    m.Params.LogToConsole = 0
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
    optResult = getResult(m, c_ids, v_ids)
    printSolution(m)
    prices = pricing(m, m.ObjVal, optResult, v_bid, v_ids)
    print('total price->', prices[1])
    print('prices->', prices[0])
    print('allocation execution time:', str(endTime-startTime).replace('.', ','))
    

def getResult(model, cloudlets, vms):
    ILPResult = dict()
    for cl in cloudlets:
        for vm in vms:
            if abs(model.getVarByName(f"allocate[{cl},{vm}]").x) > 1e-6:
                ILPResult[vm] = cl
    return ILPResult
    

def pricing(model, optValue, optResult, v_bids, v_ids):
    totalPrices = 0
    userPrice = dict()
    for vm in v_ids:
        if vm in optResult.keys():
            socialWelfare = optValue - v_bids[vm]
            clarkeValue = clarkePivotRule(model, vm, optResult[vm])
            priceToPay = clarkeValue - socialWelfare
            userPrice[vm] = priceToPay
            totalPrices += priceToPay
        else:
            userPrice[vm] = 0
    return [userPrice, totalPrices]

def clarkePivotRule(model, vm, cloudlet):
    model.getVarByName(f"allocate[{cloudlet},{vm}]").ub = 0
    model.optimize()
    clarkeResult = model.ObjVal
    model.getVarByName(f"allocate[{cloudlet},{vm}]").ub = 1
    return clarkeResult

def main():    
    jsonFilePath = '/home/jps/allocation_models/greedy_vs_exact/instances/vEpsilon/clE/cle_10.json'    
    build(jsonFilePath)

if __name__ == "__main__":
    main()