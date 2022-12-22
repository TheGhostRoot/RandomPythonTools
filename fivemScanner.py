import fivempy
from rcon.source import Client as SrcClient
from rcon.battleye import Client as BEClient
import mctools
import requests as rq

ips = []
ports = []
file = None
outputFile = None
t = 50

def setCFXforIP():
    while True:
        inp = input("Enter the cfx link ( ex: cfx.re/join/7tg28c ) >> ")
        if inp != "" and "cfx.re/join/" in inp:
            id = inp.replace("cfx.re/join/", "")
            data = getIPfromCFX(id)
            print("Server IP:PORT >> " + data)
            h = {
                "accept": "application/json, text/plain, */*",
                "sec-ch-ua": '"Chromium";v="96", "Opera GX";v="82", ";Not A Brand";v="99"',
                "origin": "https://servers.fivem.net",
                "referer": "https://servers.fivem.net/",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/82.0.4227.25"
            }
            data = rq.get(f"https://servers-frontend.fivem.net/api/servers/single/{id}", headers=h).json()
            if withSave():
                outputFile.write(str(data)+"\n")
                outputFile.close()
            break


def getIPfromCFX(cfxID):
    h = {
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="96", "Opera GX";v="82", ";Not A Brand";v="99"',
        "origin": "https://servers.fivem.net",
        "referer": "https://servers.fivem.net/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/82.0.4227.25"
    }
    data = rq.get(f"https://servers-frontend.fivem.net/api/servers/single/{cfxID}", headers=h).json()
    return str(data["Data"]["connectEndPoints"][0])


def setIP():
    global ips
    while True:
        inp = input("Enter FiveM server IP ( ex: 127.0.0.1,123.456.789 ) >> ")
        if inp != "":
            if "," in inp:
                if "cfx.re/join/" in inp:
                    ids = inp.split(",")
                    for id in ids:
                        id = id.replace("cfx.re/join/", "")
                        data = getIPfromCFX(id).split(":")
                        ips.append(data[0])
                else:
                    ips = inp.split(',')
            else:
                if "cfx.re/join/" in inp:
                    id = inp.replace("cfx.re/join/", "")
                    data = getIPfromCFX(id).split(":")
                    ips = [data[0]]
                else:
                    ips = [inp]
            break


def setPort():
    global ports
    while True:
        inp = input("Enter FiveM ports ( ex: 30120,30121 OR 30120-30121 ) >> ")
        if inp != "":
            if "," in inp:
                ports = list(map(int, inp.split(",")))
            elif "-" in inp:
                allPorts = inp.split("-")
                for port in range(int(allPorts[0]), int(allPorts[1]) + 1):
                    ports.append(port)
            else:
                ports = [int(inp)]
            break


def setPasswords():
    global file
    inp = input("Enable RCON? Enter the wordlist file else press enter >> ")
    if inp != "":
        file = open(inp, "rt")


def setOutput():
    global outputFile
    inp = input("Enter the output file where all the info will be stored. Press ENTER to continue without it >> ")
    if inp != "":
        outputFile = open(inp, "a")

def setTimeout():
    global t
    while True:
        inp = input("Enter the RCON timeout >> ")
        if inp != "":
            try:
                t = int(inp)
            except Exception:
                print("Only numbers!")
                continue
            else:
                break

def Menu():
    while True:
        ip = str(ips).replace("[", "").replace("]", "")
        port = str(ports).replace("[", "").replace("]", "")
        if file is None:
            name = None
        else:
            name = file.name
        if outputFile is None:
            outname = None
        else:
            outname = outputFile.name
        menu = f"""
            IP: {ip}
             PORT: {port}
              WordList: {name}
               Output FIle: {outname}
                Timeout: {t}

            1. Start RCON and FiveM scan
             2. Start RCON scan
              3. Start FiveM scan
               4. Change IP
                5. Change PORT
                10. Change Timeout
               6. Change WordList
              7. Change Output File
             8. Help menu ( this )
            9. Exit
            0. Get IP from CFX.re

            """
        print(menu)
        choice = input("Your choice? >> ")
        if choice != "":
            if choice == '10':
                setTimeout()
            elif choice == '0':
                setCFXforIP()
            elif choice == '1':
                scanAll()
            elif choice == '2':
                rconScan()
            elif choice == '3':
                fivemScan()
            elif choice == '4':
                setIP()
            elif choice == '5':
                setPort()
            elif choice == '6':
                setPasswords()
            elif choice == '7':
                setOutput()
            elif choice == '8' or choice.lower() == "h" or choice.lower() == 'help':
                print(menu)
            elif choice == '9' or choice.lower() == 'q' or choice.lower() == 'exit':
                print("Bye :)")
                exit()


# server = fivempy.Server("IP:PORT") -> json
# rcon = SrcClient("IP", PORT, passwd="PASSWORD") -> run commands -> resp = rcon.run("COMMAND", "WITH", "ARGS")

def withPassword():
    withPassword = True
    if file is None:
        withPassword = False
    return withPassword


def withSave():
    withOutfile = True
    if outputFile is None:
        withOutfile = False
    return withOutfile


def rconScan():
    ValidPass = {}
    for ip in ips:
        for port in ports:
            if withPassword():
                for line in file:
                    if "\n" in line:
                        line = line.replace("\n", "")
                    rcon = SrcClient(host=ip, port=port, passwd=line, timeout=50)
                    rcon2 = BEClient(host=ip, port=port, passwd=line, timeout=50)
                    try:
                        rcon.connect()
                        rcon.login(passwd=line)
                    except Exception as b:
                        print(f"Error: Source > password: {line} ", b)
                        try:
                            rcon2.connect()
                            rcon2.login(passwd=line)
                        except Exception as e:
                            print(f"Error: BattleEye > passoword: {line} ", e)
                        else:
                            ValidPass[ip+":"+str(port)+" BattleEye"] = line
                            print(f"Found RCON BattleEye > IP: {ip} PORT: {port} PASSWORD: {line}")
                    else:
                        ValidPass[ip + ":" + str(port) + " Source"] = line
                        try:
                            rcon2.connect()
                            rcon2.login(passwd=line)
                        except Exception as e:
                            print(f"Error: BattleEye > passoword: {line} ", e)
                        else:
                            ValidPass[ip + ":" + str(port) + " BattleEye"] = line
                            print(f"Found RCON BattleEye > IP: {ip} PORT: {port} PASSWORD: {line}")
                        print(f"Found RCON Source > IP: {ip} PORT: {port} PASSWORD: {line}")
            else:
                rcon = SrcClient(host=ip, port=port, timeout=50)
                rcon2 = BEClient(host=ip, port=port, timeout=50)
                try:
                    rcon.connect()
                except Exception as b:
                    print("Error: Source: No password ", b)
                    try:
                        rcon2.connect()
                    except Exception as e:
                        print('Error: BattleEye: No password ', e)
                    else:
                        ValidPass[ip + ":" + str(port) + " BattleEye"] = None
                        print(f"Found RCON BattleEye > IP: {ip} PORT: {port}")
                else:
                    ValidPass[ip + ":" + str(port) + " BattleEye"] = None
                    try:
                        rcon2.connect()
                    except Exception as e:
                        print('Error: BattleEye: No password ', e)
                    else:
                        ValidPass[ip + ":" + str(port) + " BattleEye"] = None
                        print(f"Found RCON BattleEye > IP: {ip} PORT: {port}")
                    print(f"Found RCON Source > IP: {ip} PORT: {port}")
    if withSave():
        outputFile.write(str(ValidPass)+"\n")
        outputFile.clsoe()

def rconSingle(ip, port):
    ValidPass = {}
    if withPassword():
                for line in file:
                    if "\n" in line:
                        line = line.replace("\n", "")
                    rcon = SrcClient(host=ip, port=port, passwd=line, timeout=50)
                    rcon2 = BEClient(host=ip, port=port, passwd=line, timeout=50)
                    try:
                        rcon.connect()
                        rcon.login(passwd=line)
                    except Exception as b:
                        print(f"Error: Source > password: {line} ", b)
                        try:
                            rcon2.connect()
                            rcon2.login(passwd=line)
                        except Exception as e:
                            print(f"Error: BattleEye > passoword: {line} ", e)
                        else:
                            ValidPass[ip + ":" + str(port) + " BattleEye"] = line
                            print(f"Found RCON BattleEye > IP: {ip} PORT: {port} PASSWORD: {line}")
                    else:
                        ValidPass[ip + ":" + str(port) + " Source"] = line
                        try:
                            rcon2.connect()
                            rcon2.login(passwd=line)
                        except Exception as e:
                            print(f"Error: BattleEye > passoword: {line} ", e)
                        else:
                            ValidPass[ip + ":" + str(port) + " BattleEye"] = line
                            print(f"Found RCON BattleEye > IP: {ip} PORT: {port} PASSWORD: {line}")
                        print(f"Found RCON Source > IP: {ip} PORT: {port} PASSWORD: {line}")
    else:
                rcon = SrcClient(host=ip, port=port, timeout=50)
                rcon2 = BEClient(host=ip, port=port, timeout=50)
                try:
                    rcon.connect()
                except Exception as b:
                    print("Error: Source: No password ", b)
                    try:
                        rcon2.connect()
                    except Exception as e:
                        print('Error: BattleEye: No password ', e)
                    else:
                        ValidPass[ip + ":" + str(port) + " BattleEye"] = None
                        print(f"Found RCON BattleEye > IP: {ip} PORT: {port}")
                else:
                    ValidPass[ip + ":" + str(port) + " BattleEye"] = None
                    try:
                        rcon2.connect()
                    except Exception as e:
                        print('Error: BattleEye: No password ', e)
                    else:
                        ValidPass[ip + ":" + str(port) + " BattleEye"] = None
                        print(f"Found RCON BattleEye > IP: {ip} PORT: {port}")
                    print(f"Found RCON Source > IP: {ip} PORT: {port}")
    if withSave():
        outputFile.write(str(ValidPass)+"\n")
        outputFile.clsoe()

def fivemScan():
    for ip in ips:
        for port in ports:
            print('Port '+str(port))
            server = fivempy.Server(ip + ":" + str(port))
            try:
                qu = mctools.QUERYClient(host=ip, port=port, timeout=100).get_full_stats()
            except Exception as e:
                print(e)
                if server.get_info() != "Server is offline or incorrect IP":
                    serv = {
                        'info': server.get_info(),
                        'hostname': server.get_hostname(),
                        'players': server.get_players(),
                        'player_list': server.get_player_list(),
                        'max_players': server.get_max_player(),
                        'player_count': server.get_player_count(),
                        'resource_list': server.get_ressource_list(),
                        'dynamic': server.get_dynamic()
                    }
                    print(serv)
                    if withSave():
                        outputFile.write(str(serv) + "\n")
                        outputFile.close()
                    continue
            else:
                m = f"""
                  QUERY!
                  MOTD: {qu['motd']}
                  Game Type: {qu['gametype']}
                  Game ID: {qu['game_id']}
                  Version: {qu['version']}
                  Plugins: {qu['plugins']}
                  Map: {qu['map']}
                  Players: {qu['numplayers']}
                  Max PLayers: {qu['maxplayers']}
                  Host port: {qu['hostport']}
                  Host IP: {qu['hostip']}
                  Player List: {qu['players']}
                  """
                print(m)
                print()
                if withSave():
                    outputFile.write(m + "\n")
                    outputFile.close()
            if server.get_info() != "Server is offline or incorrect IP":
                serv = {
                    'info': server.get_info(),
                    'hostname': server.get_hostname(),
                    'players': server.get_players(),
                    'player_list': server.get_player_list(),
                    'max_players': server.get_max_player(),
                    'player_count': server.get_player_count(),
                    'resource_list': server.get_ressource_list(),
                    'dynamic': server.get_dynamic()
                }
                print(serv)
                if withSave():
                    outputFile.write(str(serv) + "\n")
                    outputFile.close()


def scanAll():
    for ip in ips:
        for port in ports:
            server = fivempy.Server(ip + ":" + str(port))
            rconSingle(ip=ip, port=port)
            if server.get_info() != "Server is offline or incorrect IP":
                serv = {
                    'info': server.get_info(),
                    'hostname': server.get_hostname(),
                    'players': server.get_players(),
                    'player_list': server.get_player_list(),
                    'max_players': server.get_max_player(),
                    'player_count': server.get_player_count(),
                    'resource_list': server.get_ressource_list(),
                    'dynamic': server.get_dynamic()
                }
                print(serv)
                if withSave():
                    outputFile.write(str(serv) + "\n")
                    outputFile.close()


if __name__ == "__main__":
    setIP()
    setPort()
    setPasswords()
    setTimeout()
    setOutput()
    Menu()
