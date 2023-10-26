import re

def binaryConverter(decimalString=str):
    decimalList = decimalString.split('.')

    binaryList = list()
    for octet in decimalList:
        binaryOctet = bin(int(octet))[2:]
        binaryOctet = '{:0>8}'.format(binaryOctet)
        binaryList.append(binaryOctet)
    
    return ''.join(binaryList)


def decimalConverter(binaryList=list):
    outputList = list()
    for string in binaryList:
        outputList.append(str(int(string, 2)))

    return outputList


def subCalc(ipAddress=str, mask=str, numofsubnets=int):
    availableNetworks = 0
    necessaryBits = 0

    # obtain the number of necessary bits for the number of subnets
    while availableNetworks < numofsubnets:
        availableNetworks = 2 ** necessaryBits
        necessaryBits += 1
    necessaryBits -= 1

    #Convert the ip and subnet mask into binary
    binaryIP = binaryConverter(ipAddress)
    binaryMask = binaryConverter(mask)

    #calculate the subnetmask for the subnets
    networkPortion = binaryMask.find('0')

    #create the subnets based on binary
    subnets = list()
    for i in range(availableNetworks):
        subnets.append('{:0>{}}'.format(int(bin(i)[2:]), necessaryBits))

    fullsubnets = list()
    n = 8
    for subnet in subnets:
        tempList2 = list()
        network = '{:0<32}'.format(binaryIP[:networkPortion] + subnet)
        firstHost = '{:0<31}1'.format(binaryIP[:networkPortion] + subnet)
        lastHost = '{:1<31}0'.format(binaryIP[:networkPortion] + subnet)
        broadcast = '{:1<32}'.format(binaryIP[:networkPortion] + subnet)
        
        networkList = re.findall('.'*n, network)    
        fHostList = re.findall('.'*n, firstHost)
        lHostList = re.findall('.'*n, lastHost)
        broadList = re.findall('.'*n, broadcast)

        #convert them back into decimal
        network = '.'.join(decimalConverter(networkList))
        firstHost = '.'.join(decimalConverter(fHostList))
        lastHost = '.'.join(decimalConverter(lHostList))
        broadcast = '.'.join(decimalConverter(broadList))

        tempList2.append(network)
        tempList2.append(firstHost)
        tempList2.append(lastHost)
        tempList2.append(broadcast)

        fullsubnets.append(tempList2)
        

    #return a dictionary of all of the subnets
    networkDict = dict()
    count = 0

    for net in fullsubnets:
        networkDict.update({f'network {count}' : net})
        count += 1

    return networkDict


print(subCalc('10.0.0.0', '255.255.0.0', 11))