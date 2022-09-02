import json, math
import time

class Coordinates:
    def __init__(self, cpu, ram, storage):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

class User:
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
        normalized.append(User(v.id, v.vmType, v.bid, Coordinates(
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

def greedyAlloc(cloudlet, vms):
    normalVms = normalize(cloudlet, vms)
    D = calcDensities(normalVms)
    D.sort(key=lambda a: a[1], reverse=True)

    occupation = 0
    allocatedUsers = []
    socialWelfare = 0
    userPointer = 0

    while occupation <= 1 and userPointer < len(D):
        chosenUser = D[userPointer][0]
        if chosenUser.maxCoord + occupation <= 1:
            occupation += chosenUser.maxCoord
            allocatedUsers.append(chosenUser)
            socialWelfare += chosenUser.bid
        userPointer += 1
    
    print('num allocated users:', len(allocatedUsers))
    print('allocated users:', [user.id for user in allocatedUsers])
    return [socialWelfare, allocatedUsers, D]

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
        vmsList.append(User(user['id'], user['vmType'], int(user['bid']),
                            Coordinates(int(user['v_CPU']), 
                            int(user['v_RAM']),
                            int(user['v_storage']))
                            )
                        )
    return vmsList

def pricing(winners, densities):
    i = 0
    while i < len(winners):
        occupation = 0
        winner = winners[i]
        j = 0
        while occupation + winner.maxCoord <= 1 and j < len(densities):
            if densities[j][0].id != winner.id and occupation + densities[j][0].maxCoord <= 1:
                occupation += densities[j][0].maxCoord
            j += 1
        if j == len(densities):
            winner.price = 0
        else:
            winner.price = densities[j-1][1]*winner.maxCoord
        printResults(winner, densities[j-1][1])
        i += 1
        print("---------")

    return [{user.id: (user.bid, str(user.price).replace('.', ','))} for user in winners]

def printResults(winner, criticalValue):
    print('-----------')
    print('user id ->', winner.id)
    print('vmType ->', winner.vmType)
    print('critical value (b_j/w_j)->', criticalValue)
    print('winner density (b_i/w_i)->', winner.bid/winner.maxCoord)
    print('winner bid (b_i)->', winner.bid)
    print('winner maxCoord (w_i)->', winner.maxCoord)
    print('winner price->', winner.price)

def main():
    jsonFilePath = '/home/jps/allocation_models/greedy_vs_exact/instances/vDelta/clE/clE_10.json'
    data = readJSONData(jsonFilePath)
    cloudlet = buildCloudlet(data['Cloudlets'])
    userVms = buildUserVms(data['UserVMs'])
    startTime = time.time()
    result = greedyAlloc(cloudlet, userVms)
    endTime = time.time()

    print('social welfare:', result[0])
    print('execution time:', str(endTime-startTime).replace('.', ','))
    print('\nprices (user: (bid, price)) : ', pricing(winners=result[1], densities=result[2]))

if __name__ == "__main__":
    main()
