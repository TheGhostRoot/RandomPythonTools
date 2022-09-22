#!/usr/bin/python3
# Emre Ovunc info@emreovunc.com

# IP & Subnet
def Int2Bin(integer):
    binary = '.'.join([bin(int(x)+256)[3:] for x in integer.split('.')])
    return binary

IP = input('Enter an IP address: ')
Subnet = input('Enter the Subnet mask: ')
IP_binary = Int2Bin(IP)
Subnet_binary = Int2Bin(Subnet)

print('\nIP:', IP, "->", IP_binary)
print('Subnet:', Subnet, "->", Subnet_binary)

# Wild Card
def complement(number):
    if number == '0':
        number = '1'
    elif number == '.':
        pass
    else:
        number = '0'
    return number

def find_wildcard(binary_subnet):
    binary_list = list(binary_subnet)
    wildcard = ''.join(complement(binary_list[y]) for y in range(len(binary_list)))
    return wildcard

def convert_decimal(wildcard_Binary):
    binary = {}
    for x in range(4):
        binary[x] = int(wildcard_Binary.split(".")[x], 2)
    dec = ".".join(str(binary[x]) for x in range(4))
    return dec

wildcard_binary = find_wildcard(Int2Bin(Subnet))
WildCard = convert_decimal(wildcard_binary)
print('Wildcard:', WildCard, '->', wildcard_binary)

# Network ID
def andOP(IP1, IP2):
    ID_list = {}
    for y in range(4):
        ID_list[y] = int(IP1.split(".")[y]) & int(IP2.split(".")[y])
    ID = ".".join(str(ID_list[z]) for z in range(4))
    return ID

networkID = andOP(IP, Subnet)
network_Binary = Int2Bin(networkID)
print('Network ID:', networkID, "->", network_Binary)

# Broadcast IP
def orOP(IP1, IP2):
    Broadcast_list = {}
    for z in range(4):
        Broadcast_list[z] = int(IP1.split(".")[z]) | int(IP2.split(".")[z])
    broadcast = ".".join(str(Broadcast_list[c]) for c in range(4))
    return broadcast

broadcastIP = orOP(networkID, WildCard)
broadcastIP_binary = Int2Bin(broadcastIP)
print('Broadcast IP:', broadcastIP, "->", broadcastIP_binary)

# Max IP
def maxiIP(brdcstIP):
    maxIPs = brdcstIP.split(".")
    if int(brdcstIP.split(".")[3]) - 1 == 0:
        if int(brdcstIP.split(".")[2]) - 1 == 0:
            if int(brdcstIP.split(".")[1]) - 1 == 0:
                maxIPs[0] = int(brdcstIP.split(".")[0]) - 1
            else:
                maxIPs[1] = int(brdcstIP.split(".")[1]) - 1
        else:
            maxIPs[2] = int(brdcstIP.split(".")[2]) - 1
    else:
        maxIPs[3] = int(brdcstIP.split(".")[3]) - 1
    return ".".join(str(maxIPs[x]) for x in range(4))

maxIP = maxiIP(broadcastIP)
maxIP_binary = Int2Bin(maxIP)
print('Max. IP:', maxIP, "->", maxIP_binary)

# Min IP
def miniIP(ntwrkID):
    miniIPs = ntwrkID.split(".")
    if int(ntwrkID.split(".")[3]) + 1 == 256:
        if int(ntwrkID.split(".")[2]) + 1 == 256:
            if int(ntwrkID.split(".")[1]) + 1 == 256:
                miniIPs[0] = int(ntwrkID.split(".")[0]) + 1
                miniIPs[1] = 0
                miniIPs[2] = 0
                miniIPs[3] = 0
            else:
                miniIPs[1] = int(ntwrkID.split(".")[1]) + 1
                miniIPs[2] = 0
                miniIPs[3] = 0
        else:
            miniIPs[2] = int(ntwrkID.split(".")[2]) + 1
            miniIPs[3] = 0
    else:
        miniIPs[3] = int(ntwrkID.split(".")[3]) + 1
    return ".".join(str(miniIPs[x]) for x in range(4))

minIP = miniIP(networkID)
minIP_binary = Int2Bin(networkID)
print('Min. IP:', minIP, "->", minIP_binary)
