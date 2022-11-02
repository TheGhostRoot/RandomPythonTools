import os
from string import ascii_lowercase

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

try:
    import random_word
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
            wordlist = input(
                "Subdomain list (ex: file.txt) [press Enter for none] - the subdomains that are going to be checked: ")
            if wordlist != "":
                try:
                    wl = open(wordlist, "rt")
                except Exception as e:
                    print(e)
                    continue
                else:
                    subdomains = []
                    for line in wl:
                        if "\n" in line:
                            line = line.replace("\n", "")
                        if line != "":
                            subdomains.append(line)
                    break
            else:
                numWords = input("Amount of words to be generated (ex: 100) : ")
                if numWords != "":
                    try:
                        numWords = int(numWords)
                    except Exception:
                        print("Only numbers!")
                        continue
                    else:
                        break
    except KeyboardInterrupt:
        break

n = 0
subs = []


def checkSubdomains(domain, subdomainsToCheck):
    global n, subs
    for subdomain in subdomainsToCheck:
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
                else:
                    print(f"Found {n} - {subdomain}.{domain} - {ip}")
        else:
            n += 1
            subs.append(f"{subdomain}.{domain}")
            try:
                ip = gethostbyname(f"{subdomain}.{domain}")
            except Exception:
                print(f"Found {n} - {subdomain}.{domain}")
            else:
                print(f"Found {n} - {subdomain}.{domain} - {ip}")


if wordlist == "":
    checkSubdomains(domain, ascii_lowercase.split())
    words = []
    randWords = random_word.RandomWords()
    for w in range(numWords + 1):
        w = randWords.get_random_word()
        word = str(w).lower()
        word2 = str(w).lower()
        while " " in word:
            word = word.replace(" ", "")
        while " " in word2:
            word2 = word2.replace(" ", "-")
        words.append(word)
        words.append(word2)
    checkSubdomains(domain, words)
else:
    checkSubdomains(domain, subdomains)

while True:
    try:
        save = input("File name (ex: file.txt) [press Enter for none]: ")
        if save != "":
            file = open(save, 'a')
            for item in subs:
                file.write(str(item) + '\n')
            file.close()
            print("Saved!")
            break
        else:
            break
    except KeyboardInterrupt:
        break

print("Done...")
