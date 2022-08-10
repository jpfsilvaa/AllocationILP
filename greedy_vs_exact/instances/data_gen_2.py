import json
import random
import sys
from itertools import product

def vmGen(vmsQtt):
    VMs = []
    for i in range(1, vmsQtt+1):
        # units: storage(MB), cpu(MIPS), RAM(MB)
        simStorage = 512 * 1024
        simCPU = 2000
        simRAM = 64
        VMs.append({
                "id": f"v{i}",
                "bid": random.randint(60, 100),
                "v_storage": random.randint(int(0.5*simStorage), simStorage), 
                "v_CPU": random.randint(int(0.5*simCPU), simCPU), 
                "v_RAM": random.randint(int(0.5*simRAM), simRAM), 
            })
    
    return VMs

def cloudletGen(cloudletQtt):
    Cloudlets = []
    # units: storage(MB), cpu(MIPS), RAM(MB)
    Cloudlets.append({
                "id": "c1",
                "c_storage": 16 * 1024 * 1024, 
                "c_CPU": 3234,
                "c_RAM": 1024
            })
    
    return Cloudlets

def build(args):
    vmsArg = int(args[0])
    cloudletsArg = int(args[1])
    outFilePath = args[2]

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
    # python data_gen.py <number of vms> <number of cloudlets> <output file path>
    args = sys.argv[1:]
    if validateArgs(args):
        build(args)

if __name__ == "__main__":
    main()