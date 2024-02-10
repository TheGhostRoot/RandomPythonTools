import os, sys

try:
    import minestat
    import discord
    from discord.ext import commands, tasks

except ImportError:
    if sys.platform.startswith("win"):
        os.system("python -m pip install discord.py minestat")

    else:
        os.system("python3 -m pip install discord.py minestat")

    try:
        import minestat
        import discord
        from discord.ext import commands, tasks

    except ImportError:
        print("Can't install stuff")
        exit()

"""
minecraft = minestat.MineStat(address=add, port=p)
                menu = f\"""
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
  \"""

"""

bot = commands.Bot(command_prefix="!!!", help=None, intents=discord.Intents.all())

channel_id = 1159216815801630743
message_stats = None

# (address:port) : name
mc_servers = dict()
mc_servers["127.0.0.1:25565"] = "MyServer"


display_players_server = "MyServer"



my_guild_id = 0

def getMCStats(address: str, port: int) -> minestat.MineStat:
    return minestat.MineStat(address=address, port=port)

async def sendStats(embed: discord.Embed):
    channel = bot.get_channel(channel_id)
    if channel is None:
        return

    global message_stats
    if message_stats is None:
        s = await channel.send(embed=embed)
        message_stats = s

    else:
        await message_stats.edit(embed=embed)


def formatMCStats(minecraft: minestat.MineStat, server_name: str) -> discord.Embed:
    data = dict()
    if minecraft is None:
        return discord.Embed(colour=discord.Colour.red())

    emb = discord.Embed()
# MOTD : {minecraft.stripped_motd}
    menu = f"""
Host : {minecraft.address}
Server Stats : { "🟢" if minecraft.online else "🔴" }
Port : {minecraft.port}
MOTD : {minecraft.stripped_motd}
Online : {minecraft.current_players} / {minecraft.max_players}
Server Version : 1.16 - 1.20
    """
    # f"```{menu}```"
    # "🟢" if minecraft.online else "🔴"

    emb.add_field(name=server_name, value=f"```{menu}```", inline=False)
    return emb


@tasks.loop(seconds=3)
async def update():
    server_embeds = []
    players = 0
    for host in mc_servers.keys():
        name = mc_servers[host]

        stats = None
        if ":" in host:
            spl = host.split(":")
            port = int(spl[1])
            address = spl[0]
            stats = getMCStats(address, port)
            server_embeds.append(formatMCStats(stats, name))

        else:
            stats = getMCStats(host, 25565)
            server_embeds.append(formatMCStats(stats, name))

        if name == display_players_server:
            players = stats.current_players

    totalEmbed = discord.Embed(colour=discord.Colour.blue(), title="Servers Status")
    for server in server_embeds:
        for f in server.fields:
            totalEmbed.add_field(name=f.name, value=f.value, inline=f.inline)

    await sendStats(totalEmbed)
    await bot.change_presence(activity=discord.Game(name=f"{display_players_server}: {players}"))


@bot.event
async def on_ready():
    update.start()
    print(bot.user.name + " is online")


if __name__ == "__main__":
    bot.run("TOKEN HERE")
