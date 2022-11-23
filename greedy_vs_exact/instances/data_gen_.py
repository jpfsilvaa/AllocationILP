import json
import random
import sys
from itertools import product

def vmGen(vmsQtt):
    VMs = []
    # units: storage(MB), cpu(MIPS), RAM(MB)
    simMIPS = 2000

    for i in range(int(0.1*vmsQtt)):
        chosenVm = {
                "id": f'v{i}', 
                "vmType": 'gp1',
                "bid": int(random.gauss(100, 1)),
                "v_storage": 3 * 1024, 
                "v_CPU": 2 * simMIPS, 
                "v_RAM": 4 * 1024
            }
        VMs.append(chosenVm)
    
    for j in range(3, 3+int(0.9*vmsQtt)):
        chosenVm = {  
                "id": f'v{j}',  
                "vmType": 'gp2',
                "bid": int(random.gauss(100, 1)),
                "v_storage": 16 * 1024, 
                "v_CPU": 4 * simMIPS, 
                "v_RAM": 16 * 1024
            }
        VMs.append(chosenVm)
    return VMs

def cloudletGen(cloudletQtt):
    Cloudlets = []
    simMIPS = 2000
    # units: storage(MB), cpu(MIPS), RAM(MB)

    clA = { "id": "cA",
            "c_storage": 250 * 1024, 
            "c_CPU": 12 * simMIPS,
            "c_RAM": 16 * 1024
          }
    
    clB = { "id": "cB",
            "c_storage": 500 * 1024, 
            "c_CPU": 16 * simMIPS,
            "c_RAM": 32 * 1024
          }
    
    clC = { "id": "cC",
            "c_storage": 1000 * 1024, 
            "c_CPU": 22 * simMIPS,
            "c_RAM": 64 * 1024
          }
    
    clD = { "id": "cD",
            "c_storage": 2 * 1000 * 1024, 
            "c_CPU": 32 * simMIPS,
            "c_RAM": 256 * 1024
          }

    clE = { "id": "cE",
            "c_storage": 4 * 1000 * 1024, 
            "c_CPU": 60 * simMIPS,
            "c_RAM": 512 * 1024
          }

    Cloudlets.append(clA)
    return Cloudlets

def build(args):
    vmsArg = int(args[0])
    cloudletsArg = int(args[1])
    outFilePath = args[2]
    random.seed(args[3])

    cloudlets = cloudletGen(cloudletsArg)
    mainObject = {
                    "UserVMs": vmGen(vmsArg), 
                    "Cloudlets": cloudlets
                 }

    jsonString = json.dumps(mainObject, indent=4)
    jsonFile = open(outFilePath, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def validateArgs(args):
    if args:
        if args[0] and args[0]:
            return True
        else:
            return False
    else:
        return False

def main():
    # python data_gen.py <number of vms> <number of cloudlets> <output file path> <seed>
    args = sys.argv[1:]
    if validateArgs(args):
        build(args)

if __name__ == "__main__":
    main()