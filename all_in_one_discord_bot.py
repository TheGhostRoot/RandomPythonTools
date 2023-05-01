import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import random
import datetime
import numpy
import wavelink
from youtube_dl import YoutubeDL
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
import minestat

load_dotenv()

bot = commands.Bot(command_prefix="??", intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())

bot.remove_command('help')


@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    change_status.start()
    await wavelink.NodePool.create_node(bot=bot,
                                        host='127.0.0.1',
                                        port=2333,
                                        password='youshallnotpass')
    await bot.change_presence(status=discord.Status.online)
    print('♦═════════════════════SERVERS LIST═════════════════════♦')
    for guild in bot.guilds:
        print("> " + str(guild) + "  |  ID: " + str(guild.id))
    print(f"\nServers: {len(bot.guilds)}")
    print('♦════════════════════════INFO══════════════════════════♦')
    print('            •         The bot is Online!      •')
    print('            •  Made by Ivaka & Rooty & Koki4a •')
    print('♦══════════════════════════════════════════════════════♦')


activities = ["o", "i", "d"]
status = ["Yoo!",
          "Minecraft Time",
          "Discord Time",
          "Brawlhalla Time",
          "Movie Time",
          "Coding Time",
          "Dying Time",
          "??helpmepls - help menu",
          "XD",
          ":)",
          "BABI",
          "Smile",
          "усмивка",
          "Sad",
          "Exited",
          "Made by Ivaka,Rooty & Koki4a"
          ]


@tasks.loop(seconds=5)
async def change_status():
    botStats = random.randint(0, len(status) - 1)
    acStats = random.randint(0, len(activities) - 1)
    if activities[acStats] == "o":
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=status[botStats]))
    elif activities[acStats] == "i":
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=status[botStats]))
    else:
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name=status[botStats]))


@bot.event
async def on_member_join(member):
    pfp = member.avatar
    channel = bot.get_channel(1052624869264724078)  # replace id with the welcome channel's id
    embed = discord.Embed(colour=discord.Colour.dark_green())
    embed.set_author(name=f'PredatorNetwork Welcome Service')
    embed.add_field(name="**Welcome!**", value=f'**```{member} has joined```**')
    embed.set_thumbnail(url=pfp)
    embed.set_footer(text="PredatorNewtork Teams & Service")
    await channel.send(embed=embed)
    if log_channel is not None:
        embed = discord.Embed(
            title=member.name+" | Just joined",
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Roles", value=str([r.name for r in member.roles]))
        embed.add_field(name="Color", value=member.color)
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Top Role", value=member.top_role)
        embed.add_field(name="Activity", value=member.activity)
        embed.add_field(name="Voice", value=member.voice)
        await log_channel.send(embed=embed)


@bot.tree.command(name='play')
@app_commands.describe(url='YouTube link')
async def play(interaction: discord.Interaction, url: str):
    if 'http' not in url:
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name=f'{url} is not a link')
        await interaction.channel.send(embed=emb)
    elif interaction.user.voice:
        voice = interaction.guild.voice_client
        if voice is None:
            await interaction.user.voice.channel.connect()
        elif voice.is_playing():
            emb = discord.Embed(colour=discord.Colour.red())
            emb.set_author(name="Already playing")
            await interaction.channel.send(embed=emb)
            return
        voice = interaction.guild.voice_client
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']

        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        if voice.is_playing():
            emb = discord.Embed(colour=discord.Colour.purple())
            emb.set_author(name="Now playing " + info['title'])
            await interaction.channel.send(embed=emb)
    else:
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name=f"{interaction.user.name} have to join a voice channel")
        await interaction.channel.send(embed=emb)


@bot.event
async def on_member_remove(member):
    pfp = member.avatar
    channel = bot.get_channel(1052624869264724078)
    embed = discord.Embed(colour=discord.Colour.red())
    embed.set_author(name='PredatorNetwork Bye Service')
    embed.add_field(name="**Good Bye!**", value=f'**```{member} has left```**')
    embed.set_thumbnail(url=pfp)
    embed.set_footer(text="PredatorNewtork Teams & Service")
    await channel.send(embed=embed)
    if log_channel is not None:
        embed = discord.Embed(
            title=member.name + " | Just left",
            colour=discord.Colour.red()
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Roles", value=str([r.name for r in member.roles]))
        embed.add_field(name="Color", value=member.color)
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Top Role", value=member.top_role)
        embed.add_field(name="Activity", value=member.activity)
        embed.add_field(name="Voice", value=member.voice)
        await log_channel.send(embed=embed)


@bot.tree.command(name='kick')
@has_permissions(manage_roles=True, ban_members=True)
@app_commands.describe(member='@tag the member', reason="Your reason")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.message.delete()
    await member.kick(reason=reason)
    emb = discord.Embed(colour=discord.Colour.red())
    emb.set_author(name=f"{member} was kicked")
    emb.add_field(name="**Reason:**", value=f'**```{reason}```**')
    await interaction.channel.send(embed=emb)


@bot.tree.command(name='ban')
@app_commands.describe(member='@tag the member', reason="Your reason")
@has_permissions(manage_roles=True, ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    await member.ban(reason=reason)
    emb = discord.Embed(colour=discord.Colour.red())
    emb.set_author(name=f"{member} was Banned")
    emb.add_field(name="**Reason:**", value=f'**```{reason}```**')
    await interaction.channel.send(embed=emb)


@bot.tree.command(name='warn')
@commands.has_permissions(manage_messages=True)
@app_commands.describe(user="User")
async def warn(interaction: discord.Interaction, user: discord.Member):
    await interaction.message.delete()
    warn1 = discord.utils.get(user.guild.roles, id=1048958846607048779)
    warn2 = discord.utils.get(user.guild.roles, id=1048958846607048780)
    warn3 = discord.utils.get(user.guild.roles, id=1048958846607048781)
    haveWarn1 = warn1 in user.roles
    haveWarn2 = warn2 in user.roles
    haveWarn3 = warn3 in user.roles
    if haveWarn1 and haveWarn2 and haveWarn3:
        await interaction.channel.send(f"{user} can't be warned anymore.")
    elif haveWarn1 and haveWarn2:
        await user.add_roles(warn3)
        await interaction.channel.send(f"{user} was warned 3 times!")
    elif haveWarn1:
        await user.add_roles(warn2)
        await interaction.channel.send(f"{user} was warned 2 times!")
    else:
        await user.add_roles(warn1)
        await interaction.channel.send(f"{user} was warned 1 time!")


@bot.tree.command(name='unwarn')
@commands.has_permissions(manage_messages=True)
@app_commands.describe(user="User")
async def unwarn(interaction: discord.Interaction, user: discord.Member):
    await interaction.message.delete()
    warn1 = discord.utils.get(user.guild.roles, id=1048958846607048779)
    warn2 = discord.utils.get(user.guild.roles, id=1048958846607048780)
    warn3 = discord.utils.get(user.guild.roles, id=1048958846607048781)
    haveWarn1 = warn1 in user.roles
    haveWarn2 = warn2 in user.roles
    haveWarn3 = warn3 in user.roles
    if haveWarn1 and haveWarn2 and haveWarn3:
        await user.remove_roles(warn3)
        await interaction.channel.send(f"{user} now have 2 warns.")
    elif haveWarn1 and haveWarn2:
        await user.remove_roles(warn2)
        await interaction.channel.send(f"{user} now have 1 warn.")
    elif haveWarn1:
        await user.remove_roles(warn1)
        await interaction.channel.send(f"{user} now is not warned.")
    else:
        await interaction.channel.send(f"{user} was never warned.")


class CreateTicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = False

    @discord.ui.button(label='Create Ticket', style=discord.ButtonStyle.blurple)
    async def menu1(self, interaction, button: discord.Button):
        cat = discord.utils.get(interaction.guild.categories, id=1048958852831395921)
        ch = discord.utils.get(cat.text_channels, name=f"ticket-{str(interaction.user).replace('#', '').lower()}")
        if ch:
            await interaction.user.send("You already have a open ticket!")
            return
        d = await interaction.guild.create_text_channel(f"ticket {interaction.user}", category=cat)
        channel = bot.get_channel(d.id)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        emb = discord.Embed(colour=discord.Colour.green())
        emb.set_author(name=interaction.user)
        emb.add_field(name="Please describe your problem in detail.", value='Predator Team is here to help!')
        buttons = TicketButtons()
        await channel.send(embed=emb, view=buttons)


class StaffStatusButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = False

    @discord.ui.button(label="Online", style=discord.ButtonStyle.green)
    async def on(self, interaction, button: discord.Button):
        usr = discord.utils.get(interaction.guild.members, id=bot.user.id)
        await usr.edit(nick='Staff is online!')

    @discord.ui.button(label="Offline", style=discord.ButtonStyle.red)
    async def off(self, interaction, button: discord.Button):
        usr = discord.utils.get(interaction.guild.members, id=bot.user.id)
        await usr.edit(nick='Staff is offline!')


@bot.tree.command(name='staffstatus')
@has_permissions(administrator=True)
async def staffstatus(interaction: discord.Interaction):
    embed = discord.Embed(title="Staff Status")
    embed.add_field(name="Важна информация!",
                    value="До всички стафове ако някой е цъкнал online а няма екип online ще има наказания!")
    buttons = StaffStatusButtons()
    await interaction.channel.send(embed=embed, view=buttons)


class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = False

    @discord.ui.button(label='Close', style=discord.ButtonStyle.red)
    async def menu1(self, interaction, button: discord.Button):
        role = discord.utils.get(interaction.guild.roles, id=1048958846636396547)
        if role not in interaction.user.roles:
            await interaction.channel.send("You are not staff. You can't close the ticket!")
            return
        await interaction.response.send_message("This ticket is closed!")
        await interaction.channel.delete()
        self.stop()

    @discord.ui.button(label='Save', style=discord.ButtonStyle.green)
    async def menu2(self, interaction, button: discord.Button):
        role = discord.utils.get(interaction.guild.roles, id=1048958846636396547)
        if role not in interaction.user.roles:
            await interaction.channel.send("You are not staff. You can't save the ticket!")
            return
        emb = discord.Embed(colour=discord.Colour.random())
        emb.set_author(name=f"Date: {datetime.datetime.now()}")
        emb.add_field(name=interaction.channel.name, value=f'Saved by {interaction.user}')
        transcript_channel_id = 1057059092197277838  # Replace with the actual channel ID
        transcript_channel = bot.get_channel(transcript_channel_id)
        discord.TextChannel.webhooks()

        # Build the transcript message
        messages = []
        async for m in interaction.channel.history():
            messages.append(f'{m.author}: {m.content}\n')
        messages = numpy.flip(messages)
        allMessages = ''
        for msg in messages:
            allMessages += msg
        emb.add_field(name='Messages:', value=allMessages)
        emb.set_footer(text="PredatorNewtork Ticket Save")
        # Send the transcript to the transcript channel
        await transcript_channel.send(embed=emb)
        await interaction.response.send_message("This ticket is saved!")


@bot.tree.command(name='join')
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        await interaction.message.delete()
        channel = interaction.user.voice.channel
        voice = interaction.message.guild.voice_client
        if voice is not None and voice.is_connected():
            await interaction.channel.send("I am already connected!")
        else:
            await channel.connect()
    else:
        await interaction.channel.send("You are not in a VC, you must be in VC to run this command!")


"""
@bot.tree.command(name='msg')
@app_commands.describe(messageTuple1="Your message")
@has_permissions(manage_messages=True)
async def msg(interaction: discord.Interaction, messageTuple1: str):
    if type(messageTuple1) == str:
        messageTuple1 = tuple(messageTuple1.split())
    message = ''.join(c+' ' for c in messageTuple1).replace('\\n', '\n')
    channel = bot.get_channel(1048958847844368489)
    embed = discord.Embed(colour=discord.Colour.dark_blue())
    embed.set_author(name=f'Predator Network')
    embed.add_field(name=f"**Announcement:**", value=f'```{message}```')
    embed.set_footer(text="PredatorNewtork Teams & Service")
    await channel.send(embed=embed)
"""


@bot.tree.command(name='clear')
@commands.has_permissions(manage_messages=True)
@app_commands.describe(amount="Amount")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)


@bot.tree.command(name='app')
async def app(interaction: discord.Interaction):
    # Ask the first custom question
    await interaction.message.author.send("What is your name?")

    # Wait for the user's response
    response = await bot.wait_for('message', check=lambda message: message.author == interaction.message.author)
    name = response.content

    # Ask the second custom question
    await interaction.message.author.send("What is your email address?")

    # Wait for the user's response
    response = await bot.wait_for('message', check=lambda message: message.author == interaction.message.author)
    email = response.content

    # Create an embedded message with the responses
    embed = discord.Embed(title="Application Results", description=f"Name: {name}\nEmail: {email}")

    # Send the embedded message to the current channel and to the user
    await interaction.channel.send(f"{interaction.message.author.mention} check your DM", embed=embed)
    await interaction.message.author.send(embed=embed)


@bot.tree.command(name='leave')
async def leave(interaction: discord.Interaction):
    voice_client = interaction.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        emb = discord.Embed(colour=discord.Colour.random())
        emb.set_author(name="I am NOT connected to a voice channel")
        await interaction.channel.send(embed=emb)


@bot.tree.command(name='staffhelp')
@commands.has_permissions(manage_messages=True)
async def staffhelp(interaction: discord.Interaction):
    embed = discord.Embed(colour=discord.Colour.dark_blue())
    embed.set_author(name=f'HelpCommands')
    embed.add_field(name="**Staff\nBasic\nCommands:**",
                    value='**```!warn\n!unwarn\n!mute\n!unmute\n!kick\n!ban\n!unban```**')
    embed.add_field(name="**Default**", value='**commands**')
    embed.set_footer(text="PredatorNewtork Teams & Service")
    await interaction.channel.send(embed=embed)


def getAllRules():
    allRules = {}

    common_rules = ['Без обидни прякори.', 'Без прякори със сексуален характер.',
                    'Без снимки на профила с явен сексуален характер.',
                    'Без обидни профилни снимки.', 'Модераторите си запазват правото да променят псевдоними.',
                    'Без бъгове, експлойти, хакове, грешки и т.н.',
                    'Модераторите си запазват правото да използват собствената си преценка, независимо от правилата.']

    chat_rules = ['Без разпит на стафовете.', 'Без искане за предоставяне на роли/роли на стаф.',
                  'Без @споменаване на спам.',
                  'Няма сексуално открито съдържание.', 'Няма съдържание на NSFW.', 'Без порнографско съдържание.',
                  'Без незаконно съдържание.',
                  'Без публикуване на лична информация (включително истински имена, адреси, имейли, пароли, информация за банкови сметки и кредитни карти и др.).',
                  'Без пиратство.', 'Без тормоз.', 'Без сексизъм.', 'Без обиден език/псуване.', 'Без тролене.',
                  'Без спам.',
                  'Без CAPS LOCK.', 'Без рекламиране!']

    common_message = ''
    ind = 1
    for rule in common_rules:
        common_message += str(ind) + "." + rule + "\n"
        ind += 1

    chat_message = ''
    ind = 1
    for rule in chat_rules:
        chat_message += str(ind) + "." + rule + "\n"
        ind += 1

    allRules['common'] = common_message
    allRules['chat'] = chat_message
    return allRules


@bot.tree.command(name='apply')
async def apply(interaction: discord.Interaction):
    # Ask the first custom question
    await interaction.message.author.send("What is your name?")

    # Wait for the user's response
    response = await bot.wait_for('message', check=lambda
        message: message.author == interaction.message.author and message.channel == interaction.message.channel)
    name = response.content

    # Ask the second custom question
    await interaction.channel.send("What is your email address?")

    # Wait for the user's response
    response = await bot.wait_for('message', check=lambda
        message: message.author == interaction.message.author and message.channel == interaction.message.channel)
    email = response.content

    # Print the user's responses
    print(f"Name: {name} Email: {email}")


@bot.tree.command(name='правила')
@commands.has_permissions(administrator=True)
async def правила(interaction: discord.Interaction):
    await interaction.message.delete()
    await interaction.channel.send("♦══════════════════@everyone══════════════════♦")
    rules = getAllRules()
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='PredatorNetwork')
    embed.add_field(name='Общи правила:', value="```\n" + rules['common'] + '\n```')
    embed.add_field(name='Чат правила:', value="```\n" + rules['chat'] + '\n```')
    embed.set_footer(text="PredatorNewtork Teams & Service")
    await interaction.channel.send(embed=embed)
    await interaction.channel.send("♦═══════════════════════════════════════════♦")


@bot.tree.command(name='online')
async def online(interaction: discord.Interaction):
    usr = discord.utils.get(interaction.message.guild.members, id=bot.user.id)
    await usr.edit(nick='Staff Working!')


@bot.tree.command(name='ticket')
async def ticket(interaction: discord.Interaction):
    emb = discord.Embed(colour=discord.Colour.green())
    emb.set_author(name="PredatorNetwork Ticket System")
    emb.add_field(name="Click on the button to create new ticket", value='Disrespect to staff members is unacceptable')
    emb.set_footer(text="PredatorNewtork Ticket System")
    buttons = CreateTicketButtons()
    await interaction.channel.send(embed=emb, view=buttons)


@bot.tree.command(name='verify')
async def verify(interaction: discord.Interaction):
    # Create the embed message
    embed = discord.Embed(title='Verification', description='Are you sure you want to be verified?', color=0x00ff00)
    embed.set_footer(text='Click the buttons below to confirm or cancel your verification.')
    # Add the "Confirm" and "Cancel" buttons to the embed
    embed.add_field(name='\u200b', value='[Confirm](buttonurl:confirm)  [Cancel](buttonurl:cancel)', inline=False)
    # Send the embed message
    message = await interaction.channel.send(embed=embed)
    # Add the "Confirm" and "Cancel" reactions to the message
    await message.add_reaction('✅')
    await message.add_reaction('❌')


@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is from the correct message and user
    if str(reaction.emoji) == '✅':
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name="Hello Nigga")
        emb.add_field(name="Verification:", value="To verify yourself, you need to click this emoji:✅")
        await user.send(embed=emb)
    elif str(reaction.emoji) == '❌':
        pass
        # await reaction.message.author.remove_roles(role)


minecraft_ip = "130.61.140.104"
minecraft_port = 25565


@tasks.loop(minutes=1)
async def check_mc_stats():
    minecraft = minestat.MineStat(address=minecraft_ip, port=minecraft_port)
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
    channel = bot.get_channel(1068696904436809808)
    stats = "╏lobby-🟢" if minecraft.online else "lobby-🔴"
    if channel and channel.name != stats:
        await channel.edit(name=stats)


# log bot

log_channel = None

@bot.event
async def on_message(message):
    global log_channel
    if message.author == bot.user:
        return
    role = discord.utils.get(message.guild.roles, id=1065567010190270464)
    if message.content.startswith("setlog") and role in message.author.roles:
        channel_mentions = message.channel_mentions
        if channel_mentions:
            log_channel = channel_mentions[0]
            embed = discord.Embed(title="Logs channel set to:",
                                  description=f"Channel info: {log_channel.id}\n\n Channel name: {log_channel.name}",
                                  colour=discord.Colour.green())
            await message.channel.send(embed=embed)
        else:
            embed1 = discord.Embed(title="~~==============~~| Command Error |~~==============~~",
                                   description=f"~~==================================================~~\n**You need to specify a channel to set as the log channel.**\n\n~~==================================================~~\n\n Example: {prefix}#(channel) or {prefix}<#(channel ID)>\n\n~~==================================================~~",
                                   colour=discord.Colour.red())
            await message.channel.send(embed=embed1)




@bot.event
async def on_voice_state_update(member, before, after):
    if log_channel is not None:
        embed = discord.Embed(
            title=member.name+" | Voice Update",
            colour=discord.Colour.blurple()
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Top role", value=member.top_role)
        embed.add_field(name="Roles", value=str([r.name for r in member.roles]))
        embed.add_field(name="Activity", value=member.activity)
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Mention", value=member.mention)

        embed.add_field(name="After Channel Mention", value=after.channel.mention)
        embed.add_field(name="After Channel Name", value=after.channel)
        embed.add_field(name="After Channel ID", value=after.channel.id)
        embed.add_field(name="After AFK", value=after.afk)
        embed.add_field(name="After Deaf", value=after.deaf)
        embed.add_field(name="After Mute", value=after.mute)

        embed.add_field(name="Before Channel Mention", value=before.channel.mention)
        embed.add_field(name="Before Channel Name", value=before.channel)
        embed.add_field(name="Before Channel ID", value=before.channel.id)
        embed.add_field(name="Before AFK", value=before.afk)
        embed.add_field(name="Before Deaf", value=before.deaf)
        embed.add_field(name="Before Mute", value=before.mute)
        await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    if log_channel is not None:
        embed = discord.Embed(title=channel.name + " | Channel Deleted")
        embed.add_field(name="Name", value=channel.name)
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Created At", value=channel.created_at)
        embed.add_field(name="Category", value=channel.category)
        embed.add_field(name="Type", value=channel.type)
        embed.add_field(name="Last Message", value=channel.last_message)
        embed.add_field(name="Mention", value=channel.mention)

        if type(channel) is discord.TextChannel:
            embed.add_field(name="Is NSFW", value=channel.is_nsfw())
            embed.add_field(name="Is News", value=channel.is_news())

        elif type(channel) is discord.VoiceChannel:
            embed.add_field(name="Voice States", value=channel.voice_states)

        await log_channel.send(embed=embed)


@bot.event
async def on_guild_channel_delete(channel):
    if log_channel is not None:
        embed = discord.Embed(title=channel.name+" | Channel Deleted")
        embed.add_field(name="Name", value=channel.name)
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Created At", value=channel.created_at)
        embed.add_field(name="Category", value=channel.category)
        embed.add_field(name="Type", value=channel.type)
        embed.add_field(name="Last Message", value=channel.last_message)

        if type(channel) is discord.TextChannel:
            embed.add_field(name="Is NSFW", value=channel.is_nsfw())
            embed.add_field(name="Is News", value=channel.is_news())

        elif type(channel) is discord.VoiceChannel:
            embed.add_field(name="Voice States", value=channel.voice_states)

        await log_channel.send(embed=embed)


@bot.event
async def on_guild_role_create(role):
    if log_channel is not None:
        embed = discord.Embed(title=role.name+" | Role Created", color=0x00FF00)

        perm_msg = ""
        perms = [perm for perm in role.permissions]
        for name, value in perms:
            perm_msg += "・❯❯・" + name + " -> " + str(value) + "\n"

        embed.set_thumbnail(url=role.icon)
        embed.add_field(name="Name", value=role.name)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Mention", value=role.mention)
        embed.add_field(name="Members", value=str([m.name for m in role.members]))
        embed.add_field(name="Created At", value=role.created_at)
        embed.add_field(name="Color", value=role.color)
        embed.add_field(name="Is Assignable", value=role.is_assignable())
        embed.add_field(name="Is Default", value=role.is_default())
        embed.add_field(name="Is Bot Managed", value=role.is_bot_managed())
        embed.add_field(name="Is Premium Subscriber", value=role.is_premium_subscriber())

        await log_channel.send(embed=embed)
        await log_channel.send(f"**Permissions:**\n{perm_msg}")


@bot.event
async def on_guild_role_delete(role):
    if log_channel is not None:
        embed = discord.Embed(title=role.name+" | Role Deleted", color=0x00FF00)
        embed.set_thumbnail(url=role.icon)
        embed.add_field(name="Name", value=role.name)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Members", value=str([m.name for m in role.members]))
        embed.add_field(name="Created At", value=role.created_at)
        embed.add_field(name="Color", value=role.color)
        embed.add_field(name="Is Assignable", value=role.is_assignable())
        embed.add_field(name="Is Default", value=role.is_default())
        embed.add_field(name="Is Bot Managed", value=role.is_bot_managed())
        embed.add_field(name="Is Premium Subscriber", value=role.is_premium_subscriber())
        await log_channel.send(embed=embed)



@bot.event
async def on_guild_update(before, after):
    if log_channel is not None:
        embed = discord.Embed(
            title="Server Update",
            colour=discord.Colour.purple()
        )
        embed.set_thumbnail(url=after.icon)

        embed.add_field(name="After Name", value=after.name)
        embed.add_field(name="After ID", value=after.id)
        embed.add_field(name="After Large", value=after.large)
        embed.add_field(name="After System Channel", value=after.system_channel)
        embed.add_field(name="After Created At", value=after.created_at)
        embed.add_field(name="After Member Count", value=after.member_count)
        embed.add_field(name="After Owner", value=after.owner)
        embed.add_field(name="After Owner ID", value=after.owner_id)

        embed.add_field(name="Before Name", value=before.name)
        embed.add_field(name="Before ID", value=before.id)
        embed.add_field(name="Before Large", value=before.large)
        embed.add_field(name="Before System Channel", value=before.system_channel)
        embed.add_field(name="Before Created At", value=before.created_at)
        embed.add_field(name="Before Member Count", value=before.member_count)
        embed.add_field(name="Before Owner", value=before.owner)
        embed.add_field(name="Before Owner ID", value=before.owner_id)
        await log_channel.send(embed=embed)


@bot.event
async def on_message_delete(message):
    if log_channel is not None:
        embed = discord.Embed(title="Message Deleted",
                              description=f"Author: {message.author} {message.author.id})\n"
                                          f"Content: {message.content}\n"
                                          f"Location: #{message.channel.name}\n"
                                          f"Sent at: {message.created_at}\n"
                                          f"Edited at: {message.edited_at}",
                              color=0xFF0000)
        await log_channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    if (log_channel is not None) and (before.content != "" or after.content != ""):
        embed = discord.Embed(title="Message Edited",
                              description=f"Author: {before.author} ({before.author.id})\n"
                                          f"Before: {before.content}\n"
                                          f"After: {after.content}\n"
                                          f"Location: #{before.channel.name}\n"
                                          f"Content: {before.content}",
                              color=0xFFFF00)
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_role_update(before, after):
    if log_channel is not None:
        embed = discord.Embed(
            title=before.name + ' | Role Update',
            color=discord.Color.blue()
        )

        perm_msg = ""
        perms = [perm for perm in after.permissions]
        for name, value in perms:
            perm_msg += "・❯❯・" + name + " -> " + str(value) + "\n"

        member_str = ""
        mem = [mem.name for mem in after.members]
        for m in mem:
            member_str += m + "\n"

        embed.add_field(name="Name", value=after.name)
        embed.add_field(name="ID", value=after.id)
        embed.add_field(name="Color", value=after.color)
        embed.set_thumbnail(url=after.icon)
        embed.add_field(name="Created At", value=after.created_at)
        embed.add_field(name="Mention", value=after.mention)
        embed.add_field(name="Is Assignable", value=after.is_assignable())
        embed.add_field(name="Is Default", value=after.is_default())
        embed.add_field(name="Is Bot Managed", value=after.is_bot_managed())
        embed.add_field(name="Is Premium Subscriber", value=after.is_premium_subscriber())

        await log_channel.send(embed=embed)
        await log_channel.send(f"**Permissions:** \n{perm_msg} ")
        await log_channel.send(f"**Members:** \n{member_str} ")


@bot.event
async def on_member_update(before, after):
    if log_channel is not None:
        embed = discord.Embed(
            title=before.name + ' | Member Update',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=after.avatar)
        embed.add_field(name="Name", value=after.name)
        embed.add_field(name="ID", value=after.id)
        embed.add_field(name="Roles", value=str([r.name for r in after.roles]))
        embed.add_field(name="Color", value=after.color)
        embed.add_field(name="Status", value=after.status)
        embed.add_field(name="Top Role", value=after.top_role)
        embed.add_field(name="Activity", value=after.activity)
        embed.add_field(name="Voice", value=after.voice)
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_channel_update(before, after):
    if log_channel is not None:
        embed = discord.Embed(
            title=before.name + ' | Channel Update',
            color=discord.Color.blue()
        )
        weby = []
        for web in await after.webhooks():
            weby.append(web)
        embed.add_field(name="Name", value=after.name)
        embed.add_field(name="ID", value=after.id)
        embed.add_field(name="Category", value=after.category)
        embed.add_field(name="Topic", value=after.topic)
        embed.add_field(name="Position", value=after.position)
        embed.add_field(name="Webhooks", value=str(weby) if len(weby) > 0 else "No webhooks")
        embed.add_field(name="Slowmode Delay", value=after.slowmode_delay)
        embed.add_field(name="News", value=after.is_news())
        embed.add_field(name="NSFW", value=after.is_nsfw())
        perms = {}
        for target, overwrite in after.overwrites.items():
            # target.id  -  role id
            # overwrite - permissions
            perms_role = {}
            for key in overwrite._values.keys():
                # key - permission
                # value - false/true
                perms_role[key] = overwrite._values[key]
            perms[target.id] = perms_role
        for p in perms.keys():
            server = bot.get_guild(1048958846170828825)
            role = discord.utils.get(server.roles, id=p)
            permissions = perms[p]
            embed.add_field(name=role.name, value=permissions)
        roless = [r.name for r in after.changed_roles]
        embed.add_field(name="Role Names", value=str(roless) if len(roless) > 0 else "No roles")
        await log_channel.send(embed=embed)


bot.run("Discord bot token")
