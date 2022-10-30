import os

try:
    import minestat
except ImportError:
    if os.name != "nt":
        if os.name.startswith("win"):
            os.system("python -m pip install minestat")
        else:
            os.system("python3 -m pip install minestat")
        try:
            import minestat
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
            p = input("Port range (ex for single port: 25565) or (ex for multi-port: 25565,25665) or (ex for range: 25565-25565) : ")
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
                            print(port+" won't be checked")
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
                        break
                else:
                    break
    except KeyboardInterrupt:
        print("Exiting..")
        exit()

n = 0
servers = {}

if len(rangePorts) != 0:
    for add in hosts:
        for p in range(rangePorts[0], rangePorts[1] + 1):
            print(p)
            if timeout == "":
                try:
                    minecraft = minestat.MineStat(address=add, port=p)
                except TimeoutError:
                    while True:
                        print("Timeout...")
                        ag = input("Try again? Y/N: ")
                        ag = ag.lower()
                        if ag == 'y':
                            try:
                                minecraft = minestat.MineStat(address=add, port=p)
                            except TimeoutError:
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
                        servers[n] = menu
                        n += 1
                        print(menu)
            else:
                try:
                    minecraft = minestat.MineStat(address=add, port=p, timeout=to)
                except TimeoutError:
                    while True:
                        print("Timeout...")
                        ag = input("Try again? Y/N: ")
                        ag = ag.lower()
                        if ag == 'y':
                            try:
                                minecraft = minestat.MineStat(address=add, port=p, timeout=to)
                            except TimeoutError:
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
                        servers[n] = menu
                        n += 1
                        print(menu)
else:
    for add in hosts:
        for p in allPorts:
            if timeout == "":
                try:
                    minecraft = minestat.MineStat(address=add, port=p)
                except TimeoutError:
                    while True:
                        print("Timeout...")
                        ag = input("Try again? Y/N: ")
                        ag = ag.lower()
                        if ag == 'y':
                            try:
                                minecraft = minestat.MineStat(address=add, port=p)
                            except TimeoutError:
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
                        servers[n] = menu
                        n += 1
                        print(menu)
            else:
                try:
                    minecraft = minestat.MineStat(address=add, port=p, timeout=to)
                except TimeoutError:
                    while True:
                        print("Timeout...")
                        ag = input("Try again? Y/N: ")
                        ag = ag.lower()
                        if ag == 'y':
                            try:
                                minecraft = minestat.MineStat(address=add, port=p)
                            except TimeoutError:
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
                        servers[n] = menu
                        n += 1
                        print(menu)

while True:
    try:
        save = input("File name (ex: file.txt) [press Enter for none]: ")
        if save != "":
            file = open(save, 'a')
            for k in servers.keys():
                data = servers[k]
                file.write(data+"\n")
            file.close()
            print("Saved!")
            break
        else:
            break
    except KeyboardInterrupt:
        break

print("Done...")
