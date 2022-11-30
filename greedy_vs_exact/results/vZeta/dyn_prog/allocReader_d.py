def readSW():
    cTypes_u = ['A_gp1', 'A_mix', 'E_200']
    cTypes_l = ['a_gp1', 'a_mix', 'e_200']

    for i in range(len(cTypes_u)):
        for j in range(100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/dyn_prog/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("social welfare: ") != -1:
                        print(line.split(' ')[2][:-1])
        print(fileName)
        print('-----------')

def readNumberVMs():
    cTypes_u = ['A_gp1', 'A_mix', 'E_200']
    cTypes_l = ['a_gp1', 'a_mix', 'e_200']

    for i in range(len(cTypes_u)):
        for j in range (100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/dyn_prog/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("num allocated users: ") != -1:
                        print(line.split(' ')[3][:-1])
        print(fileName)
        print('-----------')

def readRunningTime():
    cTypes_u = ['A_gp1', 'A_mix', 'E_200']
    cTypes_l = ['a_gp1', 'a_mix', 'e_200']

    for i in range(len(cTypes_u)):
        for j in range (100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/dyn_prog/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.find("execution time: ") != -1:
                        print(line.split(' ')[2][:-1])
        print(fileName)
        print('-----------')

def readAllocatedUsers():
    cTypes_u = ['A_gp1', 'A_mix', 'E_200']
    cTypes_l = ['a_gp1', 'a_mix', 'e_200']

    for i in range(len(cTypes_u)):
        for j in range (100):
            fileName = f'/home/jps/allocation_models/greedy_vs_exact/results/vZeta/dyn_prog/cl{cTypes_u[i]}/cl{cTypes_l[i]}_{j}.txt'

            with open(fileName, 'r') as f:
                for line in f:
                    if line.startswith('allocated users: ['):
                        result = line.split(' ')[2:]
                        print("".join(result)[1:-2])
        print(fileName)
        print('-----------')


def main():
    readSW()
    readNumberVMs()
    readRunningTime()
    readAllocatedUsers()

if __name__ == "__main__":
    main()