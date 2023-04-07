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
    http = [htt for htt in open(httpFileName, "rt")]
if httpsFileName != "":
    https = [htt1 for htt1 in open(httpsFileName, "rt")]
if sock4FileName != "":
    sock4 = [sock for sock in open(sock4FileName, "rt")]
if sock5FileName != "":
    sock5 = [sock2 for sock2 in open(sock5FileName, "rt")]

print("Proxies:")
print("HTTP > "+str(len(http)))
print("HTTPS > "+str(len(https)))
print("SOCK4 > "+str(len(sock4)))
print("SOCK5 > "+str(len(sock5)))
print()

url = "https://api.ipify.org"

for h in https:
    prox = {
        "http": "https://"+h,
        "https": "https://"+h
    }
    working = False
    try:
        res = requests.get(url, proxies=prox, timeout=10).text
        working = True
    except Exception:
        continue
    if working:
        file = open("httpsWorking.txt", "a")
        file.write(res+'\n')
        file.close()
    print(res+" - http")
print()

for h in http:
    prox = {
        "http": "http://"+h,
        "https": "http://"+h
    }
    working = False
    try:
        res = requests.get(url, proxies=prox, timeout=10).text
        working = True
    except Exception:
        continue
    if working:
        file = open("httpWorking.txt", "a")
        file.write(res+'\n')
        file.close()
    print(res+" - http")
print()
for s5 in sock5:
    prox = {
        "http": "socks5://"+s5,
        "https": "socks5://" + s5
    }
    working = False
    try:
        res = requests.get(url, proxies=prox, timeout=10).text
        working = True
    except Exception:
        continue
    if working:
        file = open("socks5Working.txt", "a")
        file.write(res+"\n")
        file.close()
    print(res+" - sock5")
print()
for s4 in sock4:
    prox = {
        "http": "socks4://" + s4,
        "https": "socks4://" + s4
    }
    working = False
    try:
        res = requests.get(url, proxies=prox, timeout=10).text
        working = True
    except Exception:
        continue
    if working:
        file = open("socks4Working.txt", "a")
        file.write(res+"\n")
        file.close()
    print(res+" - sock4")

print("Done...")
