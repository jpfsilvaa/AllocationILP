import json
import random
import sys
from itertools import product

def vmGen(vmsQtt):
    VMs = []
    # units: storage(MB), cpu(MIPS), RAM(MB)
    simStorage = 512 * 1024
    simCPU = 2000
    simRAM = 64

    for i in range(1, int((vmsQtt)/2)):
        groupA = {  "id": f"v{i}",
                    "bid": random.randint(80, 120),
                    "v_storage": random.randint(int(0.9*(0.5*simStorage)), int(1.1*(0.5*simStorage))), 
                    "v_CPU": random.randint(int(0.9*(0.5*simCPU)), int(1.1*(0.5*simCPU))), 
                    "v_RAM": random.randint(int(0.9*(0.5*simRAM)), int(1.1*(0.5*simRAM)))
                 }

        groupB = {  "id": f"v{i}",
                    "bid": random.randint(80, 120),
                    "v_storage": random.randint(int(0.9*simStorage), int(1.1*simStorage)), 
                    "v_CPU": random.randint(int(0.9*simCPU), int(1.1*simCPU)), 
                    "v_RAM": random.randint(int(0.9*simRAM), int(1.1*simRAM))
                 }

        groupC = {  "id": f"v{i}",
                    "bid": random.randint(80, 120),
                    "v_storage": random.randint(int(0.9*(1.5*simStorage)), int(1.1*(1.5*simStorage))), 
                    "v_CPU": random.randint(int(0.9*(1.5*simCPU)), int(1.1*(1.5*simCPU))), 
                    "v_RAM": random.randint(int(0.9*(1.5*simRAM)), int(1.1*(1.5*simRAM)))
                 }

        VMs.append(groupB)

    for i in range(int((vmsQtt)/2), vmsQtt+1):
        groupA = {  "id": f"v{i}",
                    "bid": random.randint(80, 120),
                    "v_storage": random.randint(int(0.9*(0.5*simStorage)), int(1.1*(0.5*simStorage))), 
                    "v_CPU": random.randint(int(0.9*(0.5*simCPU)), int(1.1*(0.5*simCPU))), 
                    "v_RAM": random.randint(int(0.9*(0.5*simRAM)), int(1.1*(0.5*simRAM)))
                }

        groupB = {  "id": f"v{i}",
                    "bid": random.randint(80, 120),
                    "v_storage": random.randint(int(0.9*simStorage), int(1.1*simStorage)), 
                    "v_CPU": random.randint(int(0.9*simCPU), int(1.1*simCPU)), 
                    "v_RAM": random.randint(int(0.9*simRAM), int(1.1*simRAM))
                }

        groupC = {  "id": f"v{i}",
                    "bid": random.randint(80, 120),
                    "v_storage": random.randint(int(0.9*(1.5*simStorage)), int(1.1*(1.5*simStorage))), 
                    "v_CPU": random.randint(int(0.9*(1.5*simCPU)), int(1.1*(1.5*simCPU))), 
                    "v_RAM": random.randint(int(0.9*(1.5*simRAM)), int(1.1*(1.5*simRAM)))
                }

        VMs.append(groupC)
    
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