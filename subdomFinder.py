import os

try:
    import requests
except ImportError:
    if os.name != "nt":
        if os.name.startswith("win"):
            os.system("python -m pip install requests")
        else:
            os.system("python3 -m pip install requests")

try:
    from socket import gethostbyname
except ImportError:
    if os.name != "nt":
        if os.name.startswith("win"):
            os.system("python -m pip install socket")
        else:
            os.system("python3 -m pip install socket")

while True:
    try:
        domain = input("Domain: ")
        if domain != "":
            wordlist = input("Subdomain list (ex: file.txt) [press Enter for none] - the subdomains that are going to be checked: ")
            if wordlist != "":
                try:
                    wl = open(wordlist)
                    con = wl.read()
                    subdomains = con.splitlines()
                    break
                except Exception as e:
                    print(e)
                    continue
            else:
                break
    except KeyboardInterrupt:
        break

if wordlist == "":
    subs = requests.get(f"https://sonar.omnisint.io/subdomains/{domain}").json()
    n = 0
    for s in subs:
        n += 1
        try:
            ip = gethostbyname(s)
        except Exception:
            print(f"Found {n} - {s}")
        print(f"Found {n} - {s} - {ip}")
else:
    n = 0
    subs = []
    for subdomain in subdomains:  # main loop
        full_path = f"http://{subdomain}.{domain}"
        try:
            requests.get(full_path)
        except requests.ConnectionError:
            try:
                requests.get(f"https://{subdomain}.{domain}")
            except requests.ConnectionError:
                continue
            else:
                n += 1
                subs.append(f"{subdomain}.{domain}")
                try:
                    ip = gethostbyname(f"{subdomain}.{domain}")
                except Exception:
                    print(f"Found {n} - {subdomain}.{domain}")
                print(f"Found {n} - {subdomain}.{domain} - {ip}")
        else:
            n += 1
            subs.append(f"{subdomain}.{domain}")
            try:
                ip = gethostbyname(f"{subdomain}.{domain}")
            except Exception:
                print(f"Found {n} - {subdomain}.{domain}")
            print(f"Found {n} - {subdomain}.{domain} - {ip}")

while True:
    try:
        save = input("File name (ex: file.txt) [press Enter for none]: ")
        if save != "":
            file = open(save, 'a')
            for item in subs:
                file.write(str(item) +'\n')
            file.close()
            print("Saved!")
            break
        else:
            break
    except KeyboardInterrupt:
        break

print("Done...")