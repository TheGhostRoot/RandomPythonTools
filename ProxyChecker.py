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

url = "https://api.ipify.org"

sock4 = []
sock5 = []
http = []

httpFileName = input("What is the name of HTTP proxy file | Enter for none > ")
sock5FileName = input("What is the name of SOCKS5 proxy file | Enter for none > ")
sock4FileName = input("What is the name if SOCKS4 proxy file | Enter for none > ")

if httpFileName != "":
    httpFile = open(httpFileName, "rt")
    for htt in httpFile:
        http.append(htt)
if sock4FileName != "":
    sock4File = open("socks4.txt", "rt")
    for sock in sock4File:
        sock4.append(sock)
if sock5FileName != "":
    sock5File = open("socks5.txt", "rt")
    for sock2 in sock5File:
        sock5.append(sock2)

print("Proxies:")
print("HTTP > "+str(len(http)))
print("SOCK4 > "+str(len(sock4)))
print("SOCK5 > "+str(len(sock5)))
print("")

for h in http:
    prox = {
        "http": "http://"+h,
        "https": "https://"+h
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
print("")
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
print("")
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
