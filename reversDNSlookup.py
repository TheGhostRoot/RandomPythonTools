# pip install dnspython
import dns.resolver, dns.reversename

ip = input("IP: ")
addrs = dns.reversename.from_address(ip)
print(addrs)
print(str(dns.resolver.resolve(addrs,"PTR")[0]))