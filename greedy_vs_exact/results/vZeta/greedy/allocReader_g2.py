def readSW(cTypes_u, cTypes_l):
    for i in range(len(cTypes_u)):
        for j in range(100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/greedy/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("social welfare: ") != -1:
                        print(line.split(' ')[2][:-1])
        print(fileName)
        print('-----------')

def readNumberVMs(cTypes_u, cTypes_l):
    for i in range(len(cTypes_u)):
        for j in range (100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/greedy/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("num allocated users: ") != -1:
                        print(line.split(' ')[3][:-1])
        print(fileName)
        print('-----------')

def readRunningTime(cTypes_u, cTypes_l):
    for i in range(len(cTypes_u)):
        for j in range (100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/greedy/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("execution time: ") != -1:
                        print(line.split(' ')[2][:-1])
        print(fileName)
        print('-----------')

def readAllocatedUsers(cTypes_u, cTypes_l):
    for i in range(len(cTypes_u)):
        for j in range (100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/greedy/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.startswith('allocated users: ['):
                        result = line.split(' ')[2:]
                        print("".join(result)[1:-2])
        print(fileName)
        print('-----------')


def main():
    cTypes_u = ['A_2']
    cTypes_l = ['a_2']
    readSW(cTypes_u, cTypes_l)
    readNumberVMs(cTypes_u, cTypes_l)
    readRunningTime(cTypes_u, cTypes_l)
    readAllocatedUsers(cTypes_u, cTypes_l)

if __name__ == "__main__":
    main()