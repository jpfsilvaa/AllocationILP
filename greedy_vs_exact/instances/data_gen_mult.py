import json
import random
import sys
from itertools import product

def vmGen(vmsQtt):
    VMs = []
    # units: storage(MB), cpu(MIPS), RAM(MB)
    simMIPS = 2000
    for i in range(0, 125):
        VMs.append({
                "id": f'v{i}', 
                "vmType": 'gp1',
                "bid": int(random.gauss(100, 10)),
                "v_storage": int(random.gauss(3 * 1024, 300)), 
                "v_CPU": int(random.gauss(2 * simMIPS, 400)), 
                "v_RAM": int(random.gauss(4 * 1024, 400))
            })
    for j in range(125, 250):
        VMs.append({  
                "id": f'v{j}',  
                "vmType": 'gp2',
                "bid": int(random.gauss(100, 10)),
                "v_storage": int(random.gauss(16 * 1024, 1600)), 
                "v_CPU": int(random.gauss(4 * simMIPS, 800)), 
                "v_RAM": int(random.gauss(16 * 1024, 1600))
            })
    for k in range(250, 375):
        VMs.append({
                "id": f'v{k}',
                "vmType": 'ramInt',
                "bid": int(random.gauss(150, 10)),
                "v_storage": int(random.gauss(16 * 1024, 1600)), 
                "v_CPU": int(random.gauss(8 * simMIPS, 800)), 
                "v_RAM": int(random.gauss(64 * 1024, 6400))
            })
    for l in range(375, 500):
        VMs.append({
                "id": f'v{l}', 
                "vmType": 'cpuInt',
                "bid": int(random.gauss(150, 10)),
                "v_storage": int(random.gauss(16 * 1024, 1600)), 
                "v_CPU": int(random.gauss(16 * simMIPS, 3200)), 
                "v_RAM": int(random.gauss(32 * 1024, 3200))
            })
    return VMs

def cloudletGen(cloudletQtt):
    Cloudlets = []
    simMIPS = 2000
    # units: storage(MB), cpu(MIPS), RAM(MB)

    # for i in range(0, 2):
    #     Cloudlets.append({ "id": f"cA_{i}",
    #         "c_storage": 250 * 1024, 
    #         "c_CPU": 12 * simMIPS,
    #         "c_RAM": 16 * 1024
    #         })
    
    # for j in range(2, 4):
    #     Cloudlets.append({ "id": f"cB_{j}",
    #             "c_storage": 500 * 1024, 
    #             "c_CPU": 16 * simMIPS,
    #             "c_RAM": 32 * 1024
    #         })
    
    # for k in range(4, 6):
    #     Cloudlets.append({ "id": f"cC_{k}",
    #             "c_storage": 1000 * 1024, 
    #             "c_CPU": 22 * simMIPS,
    #             "c_RAM": 64 * 1024
    #         })

    # for l in range(6, 8):
    #     Cloudlets.append({ "id": f"cD_{l}",
    #             "c_storage": 2 * 1000 * 1024, 
    #             "c_CPU": 32 * simMIPS,
    #             "c_RAM": 256 * 1024
    #         })

    for m in range(50):
        Cloudlets.append({ "id": f"cE_{m}",
                "c_storage": 4 * 2 * 1000 * 1024, 
                "c_CPU": 60 * 2 * simMIPS,
                "c_RAM": 512 * 2 * 1024
            })

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