from decimal import Decimal

class MobFogSimData:
    def __init__(self):
        self.disconnectecTimeAvg = 0
        self.attainedUsers = 0
        # talvez criar algo que cruze os dados de: quantas vezes o usuario perdeu e quantas vezes ele migrou

class AuctionData:
    def __init__(self):
        self.prices = 0
        self.socialWelfare = 0
        self.profit = 0

def readPricesAndSWelfare(contentLine):
    pricesPos = contentLine.find("PRICES: ")
    sWelfarePos = contentLine.find("SOCIAL WELFARE: ")
    priceValue = Decimal(contentLine[pricesPos+8:sWelfarePos-3])
    sWelfareValue = Decimal(contentLine[sWelfarePos+16:])
    return [priceValue, sWelfareValue]

def readDisconnectedTime(contentLine):
    return Decimal(contentLine[31:])

def readAttainedUsers(contentLine):
    pass

def printResults(mfsData, auctionData):
    print("Total prices for each auction: ", [str(p.prices) for p in auctionData])
    print("\nTotal social welfares for each auction: ", [str(p.socialWelfare) for p in auctionData])
    print("\nProfits for each auction: ", [str(p.profit) for p in auctionData])
    print("\nDisconnected time avg: ", mfsData.disconnectecTimeAvg)

def main():
    fileName = 'out.txt'
    mfsData = MobFogSimData()
    auctionData = list()

    with open(fileName, 'r') as f:
        for line in f:
            if line.find("PRICES: ") != -1:
                currAuctionData = AuctionData()
                result = readPricesAndSWelfare(line)
                currAuctionData.prices = result[0]
                currAuctionData.socialWelfare = result[1]
                if (currAuctionData.socialWelfare > 0):
                    currAuctionData.profit = currAuctionData.prices/currAuctionData.socialWelfare
                auctionData.append(currAuctionData)
            if line.find("Average of without connection: ") != -1:
                mfsData.disconnectecTimeAvg = readDisconnectedTime(line)
            # if line.find(sub) != -1:
            #    readAttainedUsers(contentLine)
    
    printResults(mfsData, auctionData)

if __name__ == '__main__':
    main()