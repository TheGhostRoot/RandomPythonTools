import os

try:
    import minestat
    import mcrcon
    import mctools
except ImportError:
    if os.name != "nt":
        if os.name.startswith("win"):
            os.system("python -m pip install minestat mctools mcrcon")
        else:
            os.system("python3 -m pip install minestat mctools mcrcon")
        try:
            import minestat
            import mcrcon
            import mctools
        except ImportError:
            print("You need python3")
            exit()
    else:
        exit()


while True:
    try:
        add = input("Host / IP (ex for single host: 127.0.0.1) (ex for multi-host: 127.0.0.1,1.1.1.1) : ")
        if add != "":
            hosts = []
            if "," in add:
                host = add.split(",")
                for h in host:
                    hosts.append(h)
            else:
                hosts.append(add)
            p = input(
                "Port range (ex for single port: 25565) or (ex for multi-port: 25565,25665) or (ex for range: 25565-25565) : ")
            if p != "":
                allPorts = []
                rangePorts = []
                if "-" in p:
                    # range of ports
                    ports = p.split("-")
                    startPort = ports[0]
                    finalPort = ports[1]
                    ra = [startPort, finalPort]
                    for port in ra:
                        try:
                            port = int(port)
                        except Exception:
                            print(port + " is not an number")
                            continue
                        else:
                            rangePorts.append(port)
                elif "," in p:
                    # few ports
                    ports = p.split(",")
                    for port in ports:
                        try:
                            port = int(port)
                        except Exception:
                            print(port + " won't be checked")
                            continue
                        else:
                            allPorts.append(port)
                else:
                    # single port
                    try:
                        p = int(p)
                    except Exception:
                        print("Only numbers!")
                        continue
                    else:
                        allPorts.append(p)
                timeout = input("Timeout in seconds (for default press Enter): ")
                if timeout != "":
                    try:
                        to = int(timeout)
                    except Exception:
                        print("Only numbers!")
                        continue
                    else:
                        rc = input("RCON Y/N : ")
                        if rc != "":
                            rc = rc.lower()
                            if rc == "y":
                                wl = input("World list (ex: /usr/bin/passwords.txt) : ")
                                if wl != "":
                                    try:
                                        file = open(wl, "rt")
                                    except Exception as e:
                                        print(e)
                                        continue
                                    else:
                                        worldlist = []
                                        for line in file:
                                            if "\n" in line:
                                                line = line.replace("\n", "")
                                            worldlist.append(line)
                            qu = input("QUERY Y/N : ")
                            if qu != "":
                                qu = qu.lower()
                                break
                else:
                    rc = input("RCON Y/N : ")
                    if rc != "":
                        rc = rc.lower()
                        if rc == "y":
                            wl = input("World list (ex: /usr/bin/passwords.txt) : ")
                            if wl != "":
                                try:
                                    file = open(wl, "rt")
                                except Exception as e:
                                    print(e)
                                    continue
                                else:
                                    worldlist = []
                                    for line in file:
                                        if "\n" in line:
                                            line = line.replace("\n", "")
                                        worldlist.append(line)
                        qu = input("QUERY Y/N : ")
                        if qu != "":
                            qu = qu.lower()
                            break

    except KeyboardInterrupt:
        print("Exiting..")
        exit()

n = 0
servers = {}


def checkMC(add, p):
    global minecraft, menu, ag, n, servers
    if timeout == "":
        try:
            minecraft = minestat.MineStat(address=add, port=p)
        except Exception:
            while True:
                print("Error...")
                ag = input("Try again? Y/N: ")
                ag = ag.lower()
                if ag == 'y':
                    try:
                        minecraft = minestat.MineStat(address=add, port=p)
                    except Exception:
                        continue
                    else:
                        break
                else:
                    break
        else:
            if minecraft.max_players is not None:
                menu = f"""
  Port: {minecraft.port}
  Host: {minecraft.address}
  MOTD: {minecraft.motd}
  Online: {minecraft.online}
  Players: {minecraft.current_players}
  Max Players: {minecraft.max_players}
  Gamemode: {minecraft.gamemode}
  Latency: {minecraft.latency}
  Tool version: {minecraft.VERSION}
  Server version: {minecraft.version}
  SPL protocol: {minecraft.slp_protocol}
  Stripped MOTD: {minecraft.stripped_motd}
  """
                n += 1
                servers[n] = menu
                print(menu)
    else:
        try:
            minecraft = minestat.MineStat(address=add, port=p, timeout=to)
        except Exception:
            while True:
                print("Error...")
                ag = input("Try again? Y/N: ")
                ag = ag.lower()
                if ag == 'y':
                    try:
                        minecraft = minestat.MineStat(address=add, port=p, timeout=to)
                    except Exception:
                        continue
                    else:
                        break
                else:
                    break
        else:
            if minecraft.max_players is not None:
                menu = f"""
  Port: {minecraft.port}
  Host: {minecraft.address}
  MOTD: {minecraft.motd}
  Online: {minecraft.online}
  Players: {minecraft.current_players}
  Max Players: {minecraft.max_players}
  Gamemode: {minecraft.gamemode}
  Latency: {minecraft.latency}
  Tool version: {minecraft.VERSION}
  Server version: {minecraft.version}
  SPL protocol: {minecraft.slp_protocol}
  Stripped MOTD: {minecraft.stripped_motd}
  """
                n += 1
                servers[n] = menu
                print(menu)


def checkRCON(add, p):
    global n, servers
    if timeout == "":
        # no timeout to
        for password in worldlist:
            rcon = mcrcon.MCRcon(host=add, password=password, port=p)
            try:
                rcon.connect()
            except Exception as e:
                rcon.disconnect()
                print(e)
                continue
            else:
                rcon.disconnect()
                m = f"""
  RCON Found!
  Port: {p}
  Host: {add}
  Password: {password}
  """
                n += 1
                servers[n] = m
                print(m)
    else:
        # have timeout
        for password in worldlist:
            rcon = mcrcon.MCRcon(host=add, password=password, port=p, timeout=to)
            try:
                rcon.connect()
            except Exception as e:
                rcon.disconnect()
                print(e)
                continue
            else:
                rcon.disconnect()
                m = f"""
  RCON Found!
  Port: {p}
  Host: {add}
  Password: {password}
  """
                n += 1
                servers[n] = m
                print(m)


def checkQUERY(add, p):
    global n, servers
    if timeout == "":
        query = mctools.QUERYClient(host=add, port=p)
    else:
        query = mctools.QUERYClient(host=add, port=p, timeout=to)

    try:
        stats = query.get_full_stats()
    except Exception:
        return
    else:
        players = []
        pp = list(map(str, stats['players']))
        for player in pp:
            if "\x1b[0m" in player:
                player = player.replace("\x1b[0m", "")
            players.append(player)
        m = f"""
  QUERY!
  MOTD: {stats['motd']}
  Game Type: {stats['gametype']}
  Game ID: {stats['game_id']}
  Version: {stats['version']}
  Plugins: {stats['plugins']}
  Map: {stats['map']}
  Players: {stats['numplayers']}
  Max PLayers: {stats['maxplayers']}
  Host port: {stats['hostport']}
  Host IP: {stats['hostip']}
  Player List: {players}
  """
        n += 1
        servers[n] = m
        print(m)


def attack(add, p):
    print(f"Port {p}")
    checkMC(add=add, p=p)
    if rc == 'y':
        checkRCON(add=add, p=p)
    if qu == 'y':
        checkQUERY(add=add, p=p)


if len(rangePorts) != 0:
    for add in hosts:
        for p in range(rangePorts[0], rangePorts[1] + 1):
            attack(add=add, p=p)
else:
    for add in hosts:
        for p in allPorts:
            attack(add=add, p=p)

while True:
    try:
        save = input("File name (ex: file.txt) [press Enter for none]: ")
        if save != "":
            file = open(save, 'a')
            for k in servers.keys():
                data = servers[k]
                file.write(data + "\n")
            file.close()
            print("Saved!")
            break
        else:
            break
    except KeyboardInterrupt:
        break

print("Done...")
