import json, math

class Coordinates:
    def __init__(self, cpu, ram, storage):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

class User:
    def __init__(self, id, bid, maxCoord, coords):
        self.id = id
        self.bid = bid
        self.maxCoord = maxCoord
        self.coords = coords

class Cloudlet:
    def __init__(self, id, coords):
        self.id = id
        self.coords = coords

def normalize(cloudlet, vms):
    normalized = []
    for v in vms:
        normalized.append(User(v.id, v.bid, v.maxCoord, Coordinates(
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
            allocatedUsers.append(chosenUser.id)
            socialWelfare += chosenUser.bid
        userPointer += 1
    print("allocated users -> ", allocatedUsers)
    return socialWelfare

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
        vmsList.append(User(user['id'], int(user['bid']), 0, 
                            Coordinates(int(user['v_CPU']), 
                            int(user['v_RAM']),
                            int(user['v_storage']))
                            )
                        )
    return vmsList

def main():
    jsonFilePath = '/home/jps/allocation_models/greedy_vs_exact/instances/test_1000_instances.json'
    data = readJSONData(jsonFilePath)
    cloudlet = buildCloudlet(data['Cloudlets'])
    userVms = buildUserVms(data['UserVMs'])
    print('FINAL SOCIAL WELFARE -> ', greedyAlloc(cloudlet, userVms))

if __name__ == "__main__":
    main()
