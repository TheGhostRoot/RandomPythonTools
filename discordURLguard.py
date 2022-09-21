try:
    import os
    from discord.ext import commands
    import requests
    import time
    import socket
    from urllib.parse import urlparse
except ImportError:
    os.system("pip install discord.py")
    os.system("pip install requests")
    os.system("pip install urllib")
    os.system("pip install time")
    os.system("pip install socket")
    try:
        from urllib.parse import urlparse
        import os
        import time
        import socket
        from discord.ext import commands
        import requests
    except ImportError:
        print(" Use python 3.7.9 https://python.org")
        exit()

name = "cool python thingy"
logo = """
█████████████████████████████████████████████████████████
███▄─██─▄█▄─▄▄▀██─██████─▄▄▄▄█▄─██─▄██▀▄─██▄─▄▄▀█▄─▄▄▀███
████─██─███─▄─▄██─██████─██▄─██─██─███─▀─███─▄─▄██─██─███
████▄▄▄▄██▄▄█▄▄██▄▄▄▄███▄▄▄▄▄██▄▄▄▄██▄▄█▄▄█▄▄█▄▄█▄▄▄▄████
"""


def checker(domain):
    HEADER = {'Content-Type': 'application/json'}
    src1 = requests.get("https://api.phisherman.gg/v1/domains/" + str(domain), headers=HEADER)
    if src1.status_code == 404:
        print("API is invalid: https://api.phisherman.gg/v1/domains/" + str(domain))
    if src1.status_code == 429:
        print(" | Rate Limited | - Phisherman")
    return src1


def getDomain(link):
    # https://www.fyou.com/fefef/ferfefr
    domain = urlparse(link).netloc
    return domain


"""
m = ""
for char in logo:
    time.sleep(0.2)
    m = m + char
    print(m)
"""
print(logo)

while True:
    # token = input(" [<?>} Enter the token of the account you want to protect >> ")
    token = "NjM2OTUwOTYyMjQ1NzMwMzI0.GdAqZS.Kf8reauzGeWsu-AVEtqOR_GkjWgT_WgrWUb210"
    if token != "":
        try:
            Header = {'Content-Type': 'application/json', 'authorization': token}
            src = requests.get("https://discordapp.com/api/v6/users/@me/library", headers=Header)
            if src.status_code == 404:
                print("API is invalid: https://discordapp.com/api/v6/users/@me/library")
            if src.status_code == 429:
                print(" | Rate Limited |")
            if src.status_code == 200:
                # print("Valid: " + token)
                print(" Logging into.onto this account.")
                break
            else:
                print("Invalid Token: " + token)
                break
        except:
            print("Error withe checking the token!")
            break
bot = commands.Bot(command_prefix="?", self_bot=True)


@bot.event
async def on_message(ctx):
    message = ctx.content
    if message != "":
        try:
            print("message: " + str(message))
        except:
            pass
    filtered = message.split()
    if message != "":
        if "http://" or "https://" in filtered:
            for word in filtered:
                dom = getDomain(word)
                if "http" in word:
                    if dom == "discord.gift":
                        # nitro
                        code = word.replace("https://discord.gift/", "")
                        if len(code) == 13:
                            redeemheaders = {
                                    'Authorization': token,  # dont replace this.
                                    'content-type': 'application/json',
                                    'payment_source_id': 'null'
                            }
                            r = requests.post(
                                    'https://ptb.discordapp.com/api/v6/entitlements/gift-codes/' + code + '/redeem',
                                    headers=redeemheaders)
                            print(r.status_code)
                            if r.status_code == 202:
                                print(" Valid gift: " + word + " was claimed")
                            elif r.status_code == 201:
                                print(" Valid gift: " + word + " was claimed")
                            elif r.status_code == 400:
                                print(" Invalid gift: "+word)
                    else:
                        checked = checker(dom)
                        idk = bool("exe" or "mp4" or "mp3" or "php" or "jpg" or "js" or "py" or "sh" in word)
                        idk2 = bool("watch" or "@" or "#" or "!" or "^" or "$" or "web" or "listen" in word)
                        short = bool("bit.ly" or "shorturl.at" or "tinyurl.com" or "rotf.lol" or "tiny.one" in dom)
                        short3 = bool("tinyurl.com" in dom)
                        short2 = bool("cutt.ly" or "rb.gy" or "" in dom)
                        if checked.content == b"true" or idk or idk2 or short or short2 or short3:
                            if "*" or ".mov" or "'" or "\"" or "png" or "css" or "html" or "http" in word:
                                try:
                                    socket.gethostbyname(dom)
                                    if socket.gethostbyname(dom) != "0.0.0.0":
                                        if checked.content == b"true":
                                            print("{!} WARNING: " + str(word) + " IP: " + str(
                                                socket.gethostbyname(dom)) + " Domain: " + dom + "Scanned by "
                                                                                                 "phishermans")
                                        else:
                                            print("{!} WARNING: " + str(word) + " IP: " + str(
                                                socket.gethostbyname(dom)) + " Domain: " + dom)
                                except:
                                    print("{!} WARNING: " + str(word) + " Domain: " + str(dom))
                        else:
                            try:
                                socket.gethostbyname(dom)
                                if socket.gethostbyname(dom) != "0.0.0.0":
                                    print("[.] Seems good: " + str(word) + " IP: " + str(
                                        socket.gethostbyname(dom)) + " Domain: " + str(dom))
                            except:
                                print("[.] Seems good: " + str(word) + " Domain: " + str(dom))


# http://get.org
# https://get.com
@bot.event
async def on_ready():
    print(" The Guard is ready")


bot.run(token, bot=False)
