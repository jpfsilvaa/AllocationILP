import json
import random
import sys
from itertools import product

def vmGen(vmsQtt):
    VMs = []
    for i in range(1, vmsQtt+1): # valor dado pelo argumetno
        # units: storage(MB), cpu(MIPS), RAM(MB), delayThreshold(ms)
        VMs.append({
                "name": f"v{i}",
                "user": f"u{i}",
                "v_storage": random.randint(150, 500), 
                "v_CPU": random.randint(1500, 3500), 
                "v_RAM": random.randint(100, 400), 
                "v_delayThreshold": random.randint(3000, 5000)
            })
    
    return VMs

def cloudletGen(cloudletQtt):
    Cloudlets = []
    # units: storage(MB), cpu(MIPS), RAM(MB)
    Cloudlets.append({
                "name": "c0",
                "c_storage": 50*pow(10, 6), 
                "c_CPU": 3*pow(10, 6),
                "c_RAM": 200*pow(10, 3)
            })
    
    for i in range(1, cloudletQtt+1): # valor dado pelo argumento
        # units: storage(MB), cpu(MIPS), RAM(MB)
        Cloudlets.append({
                "name": f"c{i}",
                "c_storage": random.randint(300, 1500),
                "c_CPU": random.randint(3000, 7500) ,
                "c_RAM": random.randint(400, 8500)
            })
    
    return Cloudlets

def userGen(userQtt, cloudletQtt):
    Users = []
    for i in range(1, userQtt+1):
            Users.append({
            "name": f"u{i}",
            "u_vm": f"v{i}",
            "u_cloudlet": f"c{random.randint(1, i)}"
        })
    
    return Users

def delayGen(cloudlets):
    Delays = []
    cloudletNames = [c['name'] for c in cloudlets]

    pairs = product(cloudletNames, repeat=2)
    for pair in pairs:
        if pair[0] == pair[1]:
            Delays.append({
                "source": f"{pair[0]}", "destiny": f"{pair[1]}", "delay": 0
            })
        else:
            Delays.append({
                "source": f"{pair[0]}", "destiny": f"{pair[1]}", "delay": random.randint(3000, 30000)
            })
        
    return Delays

def build(args):
    vmsArg = int(args[0])
    cloudletsArg = int(args[1])

    cloudlets = cloudletGen(cloudletsArg)
    mainObject = {"VMs": vmGen(vmsArg), 
                    "Cloudlets": cloudlets, 
                    "Users": userGen(vmsArg, cloudletsArg),
                    "DelayBetweenCloudlets": delayGen(cloudlets)}

    jsonString = json.dumps(mainObject, indent=4)
    jsonFile = open("/home/jps/pli/data/instances.json", "w")
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
    # python data_gen.py <number of vms> <number of cloudlets>
    args = sys.argv[1:]
    if validateArgs(args):
        build(args)

if __name__ == "__main__":
    main()