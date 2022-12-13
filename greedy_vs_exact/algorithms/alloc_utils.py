import json, math

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

def userFits(user, occupation):
    return (user.coords.cpu + occupation.cpu <= 1
            and user.coords.ram + occupation.ram <= 1 
            and user.coords.storage + occupation.storage <= 1)

def allocate(user, occupation):
    occupation.cpu += user.coords.cpu
    occupation.ram += user.coords.ram
    occupation.storage += user.coords.storage

def isNotFull(occupation):
    return (occupation.cpu <= 1 and occupation.ram <= 1 
            and occupation.storage <= 1)

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