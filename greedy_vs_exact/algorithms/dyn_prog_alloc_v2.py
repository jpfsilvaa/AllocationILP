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

def findLType(alpha, beta, gama):
    if alpha <= beta and beta <= gama:
        return 1
    elif alpha <= gama and gama <= beta:
        return 2
    elif beta <= alpha and alpha <= gama:
        return 3
    elif beta <= gama and gama <= alpha:
        return 4
    elif gama <= alpha and alpha <= beta:
        return 5
    elif gama <= beta and beta <= alpha:
        return 6

def dynProgAlloc(cloudlet, userVms):
    CLOUDLET_CPU = 1
    CLOUDLET_RAM = 1
    CLOUDLET_STORAGE = 1
    COMBINATIONS_L = 6

    normalizedVms = normalize(cloudlet, vms)
    P = sum(normalizedVms[i].bid for i in normalizedVms)
    normalizedVms.insert(0, UserVM('', '', 0, Coordinates(0, 0, 0))) # adding 'empty' user in the first position of the list for the algorithm

    T = np.full((len(normalizedVms)+1, 
                    P+1, 
                    COMBINATIONS_L+1), (0, 0, 0))
    
    for i in range(len(normalizedVms)+1):
        for p in range(P+1):
            for l in range(COMBINATIONS_L+1):
                if p <= normalizedVms[i].bid:
                    T[i][p][l] = T[i-1][p][l]
                else:   
                    (alpha, beta, gama) = T[i-1][p][l]
                    l_ = findLType(alpha + normalizedVms[i].coords.cpu,
                            beta + normalizedVms[i].coords.ram,
                            gama + normalizedVms[i].coords.storage)
                    if (alpha + normalizedVms[i].coords.cpu <= CLOUDLET_CPU and
                            beta + normalizedVms[i].coords.ram <= CLOUDLET_RAM and
                            gama + normalizedVms[i].coords.storage <= CLOUDLET_STORAGE):
                            T[i][p][l_] = min(T[i-1][p][l_], 
                                                (alpha + normalizedVms[i].coords.cpu, 
                                                beta + normalizedVms[i].coords.ram, 
                                                gama + normalizedVms[i].coords.storage)) # TODO: HOW CAN I GET THE MININUM BETWEEN TRIPLETS?
    
    v_star = 0 # TODO: THE MAXIMUM VALUE P SUCH THAR T[n][v_star][l] <= (CLOUDLET_CPU, CLOUDLET_RAM, CLOUDLET_STORAGE) FOR l = 1 TO 6
    l = 0 # TODO: LET l BE THE STATE WHERE T[n][v_star][l] <= (CLOUDLET_CPU, CLOUDLET_RAM, CLOUDLET_STORAGE)
    S = []
    (A, B, C) = T[n][v_star][l]
    for i in range(len(userVms)-1, 0, -1):
        if T[i-1][v][l] != T[i][v][l]:
            S.append(userVms[i])
            ()
            alpha -= int(userVms[i].coords.cpu/CPU_UNIT)
            beta -= int(userVms[i].coords.ram/GB_UNIT)
            gama -= int(userVms[i].coords.storage/GB_UNIT)
    
    print('num allocated users:', len(S))
    print('allocated users:', [(user.id, user.vmType) for user in S])
    
    #preparing data for the pricing algorithm
    normalWinners = normalize(cloudlet, S)
    calcDensities(normalWinners) # this function update the maxCoord value of eah user

    del userVms[0]
    normalVms = normalize(cloudlet, userVms)
    D = calcDensities(normalVms)
    D.sort(key=lambda a: a[1], reverse=True)

    return [socialWelfare, normalWinners, D]

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