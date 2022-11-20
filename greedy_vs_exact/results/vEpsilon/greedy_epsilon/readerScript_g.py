def readSW():
    cTypesU = ['A', 'B', 'C', 'D', 'E']
    cTypesL = ['a', 'b', 'c', 'd', 'e']

    for i in range(len(cTypesU)):
        for j in range (11, 31):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vEpsilon/greedy_epsilon/cl{cTypesU[i]}/cl{cTypesL[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("social welfare: ") != -1:
                        print(line.split(' ')[2][:-1])
        print(fileName)
        print('-----------')

def readNumberVMs():
    cTypesU = ['A', 'B', 'C', 'D', 'E']
    cTypesL = ['a', 'b', 'c', 'd', 'e']

    for i in range(len(cTypesU)):
        for j in range (11, 31):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vEpsilon/greedy_epsilon/cl{cTypesU[i]}/cl{cTypesL[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("num allocated users: ") != -1:
                        print(line.split(' ')[3][:-1])
        print(fileName)
        print('-----------')

def readRunningTime():
    cTypesU = ['A', 'B', 'C', 'D', 'E']
    cTypesL = ['a', 'b', 'c', 'd', 'e']

    for i in range(len(cTypesU)):
        for j in range (11, 31):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vEpsilon/greedy_epsilon/cl{cTypesU[i]}/cl{cTypesL[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("execution time: ") != -1:
                        print(line.split(' ')[2][:-1])
        print(fileName)
        print('-----------')

def readAllocatedUsers():
    cTypesU = ['A', 'B', 'C', 'D', 'E']
    cTypesL = ['a', 'b', 'c', 'd', 'e']

    for i in range(len(cTypesU)):
        for j in range (11, 31):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vEpsilon/greedy_epsilon/cl{cTypesU[i]}/cl{cTypesL[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("allocated users: ") != -1 and line.split(' ')[0] != 'num':
                        print(line.split('[')[1][:-2])
        print(fileName)
        print('-----------')


def main():
    # readSW()
    # readNumberVMs()
    # readRunningTime()
    readAllocatedUsers()

if __name__ == "__main__":
    main()