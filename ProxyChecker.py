import os
try:
    import requests
except ImportError:
    print("Installing.. Libs")
    os.system("python -m pip install requests")
    try:
        import requests
    except ImportError:
        print("You need python")
        exit()


httpFileName = input("What is the name of HTTP proxy file | Enter for none > ")
httpsFileName = input("What is the name of HTTPS proxy file | Enter for none > ")
sock4FileName = input("What is the name if SOCKS4 proxy file | Enter for none > ")
sock5FileName = input("What is the name of SOCKS5 proxy file | Enter for none > ")

http = []
https = []
sock4 = []
sock5 = []
if httpFileName != "":
    http = [htt.replace('\n', '') for htt in open(httpFileName, "rt") ]
if httpsFileName != "":
    https = [htt1.replace('\n', '') for htt1 in open(httpsFileName, "rt")]
if sock4FileName != "":
    sock4 = [sock.replace('\n', '') for sock in open(sock4FileName, "rt")]
if sock5FileName != "":
    sock5 = [sock2.replace('\n', '') for sock2 in open(sock5FileName, "rt")]

print("Proxies:")
print("HTTP > "+str(len(http)))
print("HTTPS > "+str(len(https)))
print("SOCK4 > "+str(len(sock4)))
print("SOCK5 > "+str(len(sock5)))
print()

url = "https://api.ipify.org"
print('Checking HTTPS proxies')
for h in https:
    try:
        requests.get(url, proxies={"http": "https://"+h, "https": "https://"+h}, timeout=5)
    except Exception:
        continue
    else:
        file = open("httpsWorking.txt", "a")
        file.write(h+'\n')
        file.close()
        print(h+" - http")

print("Checking HTTP proxies")
for h in http:
    try:
        requests.get(url, proxies={"http": "http://"+h, "https": "http://"+h}, timeout=5)
    except Exception:
        continue
    else:
        file = open("httpWorking.txt", "a")
        file.write(h+'\n')
        file.close()
        print(h+" - http")

print("Checking SOCKS5 proxies")
for s5 in sock5:
    try:
        requests.get(url, proxies={"http": "socks5://"+s5, "https": "socks5://" + s5}, timeout=5)
    except Exception:
        continue
    else:
        file = open("socks5Working.txt", "a")
        file.write(s5+"\n")
        file.close()
        print(s5+" - socks5")

print("Checking SOCKS4 proxies")
for s4 in sock4:
    try:
        requests.get(url, proxies={"http": "socks4://" + s4, "https": "socks4://" + s4}, timeout=5)
    except Exception:
        continue
    else:
        file = open("socks4Working.txt", "a")
        file.write(s4+"\n")
        file.close()
        print(s4+" - sock4")

print("Done...")

