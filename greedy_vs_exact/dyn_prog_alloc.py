import sys
import json, math
import time
import numpy as np

class Coordinates:
    def __init__(self, cpu, ram, storage):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

class UserVM:
    def __init__(self, id, vmType, bid, coords):
        self.id = id
        self.vmType = vmType
        self.bid = bid
        self.price = 0
        self.maxCoord = 0
        self.coords = coords

class Cloudlet:
    def __init__(self, id, coords):
        self.id = id
        self.coords = coords

def normalize(cloudlet, vms):
    normalized = []
    for v in vms:
        normalized.append(UserVM(v.id, v.vmType, v.bid, Coordinates(
            v.coords.cpu/cloudlet.coords.cpu,
            v.coords.ram/cloudlet.coords.ram,
            v.coords.storage/cloudlet.coords.storage
        )))
    return normalized

def calcDensities(vms):
    dens = []
    for v in vms:
        v.maxCoord = max(v.coords.cpu, v.coords.ram, v.coords.storage)
        dens.append((v, v.bid/v.maxCoord))
    
    return dens

def readJSONData(jsonFilePath):
    jsonFile = open(jsonFilePath)
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def buildCloudlet(jsonData):
    cloudlets = []
    for cloudlet in jsonData:
        cloudlets.append(Cloudlet(cloudlet['id'], 
                            Coordinates(int(cloudlet['c_CPU']), 
                            int(cloudlet['c_RAM']),
                            int(cloudlet['c_storage']))
                            )
                        )
    return cloudlets[0]

def buildUserVms(jsonData):
    vmsList = []
    for user in jsonData:
        vmsList.append(UserVM(user['id'], user['vmType'], int(user['bid']),
                            Coordinates(int(user['v_CPU']), 
                            int(user['v_RAM']),
                            int(user['v_storage']))
                            )
                        )
    return vmsList

def dynProgAlloc(cloudlet, userVms):
    CPU_UNIT = 2000
    GB_UNIT = 1024
    CLOUDLET_CPU = int(cloudlet.coords.cpu/CPU_UNIT)+1
    CLOUDLET_RAM = int(cloudlet.coords.ram/GB_UNIT)+1
    CLOUDLET_STORAGE = int(cloudlet.coords.storage/GB_UNIT)+1
    print()

    T = np.full((len(userVms)+1, 
                    CLOUDLET_CPU, 
                    CLOUDLET_RAM, 
                    CLOUDLET_STORAGE), 0)
    
    for i in range(len(userVms)):
        for j in range(CLOUDLET_CPU):
            for k in range(CLOUDLET_RAM):
                for l in range(CLOUDLET_STORAGE):
                    userCPU = int(userVms[i].coords.cpu/CPU_UNIT)
                    userRAM = int(userVms[i].coords.ram/GB_UNIT)
                    userSTORAGE = int(userVms[i].coords.storage/GB_UNIT)
                    if (userCPU <= j 
                        and userRAM <= k 
                        and userSTORAGE <= l):
                            if i == 0:
                                T[i][j][k][l] = max(T[0][j][k][l],
                                                T[0][j-userCPU][k-userRAM][l-userSTORAGE]+userVms[i].bid)
                            else:
                                T[i][j][k][l] = max(T[i-1][j][k][l],
                                                T[i-1][j-userCPU][k-userRAM][l-userSTORAGE]+userVms[i].bid)
                    else:
                        T[i][j][k][l] = T[i-1][j][k][l]
    
    S = []
    socialWelfare = 0
    alpha = CLOUDLET_CPU-1 # descreasing 1 for acessing the array values
    beta = CLOUDLET_RAM-1
    gama = CLOUDLET_STORAGE-1
    for i in range(len(userVms)-1, -1, -1):
        if i == 18:
            print('------')
            print(userVms[i].id)
            print(T[i-1, alpha, beta, gama], T[i, alpha, beta, gama])
            print('------')
        if T[i-1, alpha, beta, gama] != T[i, alpha, beta, gama]:
            S.append(userVms[i])
            socialWelfare += userVms[i].bid
            alpha -= int(userVms[i].coords.cpu/CPU_UNIT)
            beta -= int(userVms[i].coords.ram/GB_UNIT)
            gama -= int(userVms[i].coords.storage/GB_UNIT)
    
    print('num allocated users:', len(S))
    print('allocated users:', [(user.id, user.vmType) for user in S])
    normalVms = normalize(cloudlet, S)
    D = calcDensities(normalVms)
    D.sort(key=lambda a: a[1], reverse=True)
    return [socialWelfare, normalVms, D]

def userFits(user, occupation):
    return (user.coords.cpu + occupation.cpu <= 1
            and user.coords.ram + occupation.ram <= 1 
            and user.coords.storage + occupation.storage <= 1)

def printResults(winner, criticalValue):
    print('-----------')
    print('user id ->', winner.id)
    print('vmType ->', winner.vmType)
    print('critical value (b_j/w_j)->', criticalValue)
    print('winner density (b_i/w_i)->', winner.bid/winner.maxCoord)
    print('winner bid (b_i)->', winner.bid)
    print('winner maxCoord (w_i)->', winner.maxCoord)
    print('winner price->', winner.price)

def allocate(user, occupation):
    occupation.cpu += user.coords.cpu
    occupation.ram += user.coords.ram
    occupation.storage += user.coords.storage

def pricing(winners, densities):
    i = 0
    while i < len(winners):
        occupation = Coordinates(0, 0, 0)
        winner = winners[i]
        j = 0
        while userFits(winner, occupation) and j < len(densities):
                if densities[j][0].id != winner.id and userFits(densities[j][0], occupation):
                        allocate(densities[j][0], occupation)
                j += 1
        if j == len(densities):
            winner.price = 0
        else:
            winner.price = densities[j-1][1]*winner.maxCoord
        printResults(winner, densities[j-1][1])
        i += 1

    return [{user.id: (user.bid, str(user.price).replace('.', ','))} for user in winners]

def main(jsonFilePath):
    data = readJSONData(jsonFilePath)
    cloudlet = buildCloudlet(data['Cloudlets'])
    userVms = buildUserVms(data['UserVMs'])
    startTime = time.time()
    result = dynProgAlloc(cloudlet, userVms)
    endTime = time.time()

    print('social welfare:', result[0])
    print('execution time:', str(endTime-startTime).replace('.', ','))
    # print('\nprices (user: (bid, price)) : ', pricing(winners=result[1], densities=result[2]))

if __name__ == "__main__":
    inputFilePath = sys.argv[1:][0]
    main(inputFilePath)