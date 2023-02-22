import discord
from discord import app_commands
from discord.app_commands.checks import has_permissions
from discord.ext import commands, tasks
import time
import random

bot = commands.Bot(command_prefix="??", self_bot=False, bot=True, intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())

bot.remove_command('help')

# Warn user
user = {}
warn_user_stats = {}

# Anti Raid
last_member_join = {}
last_member_leave = {}

dm_leave = {}
dm_join = {}

max_members_to_leave_per_second = {}
max_members_to_join_per_second = {}

raid_stats = {}

# Anti Retard
quarantine_role_id = {}
quarantine_stats = {}

# Anti Nuke
channel_creation = {}
channel_deletion = {}
role_creation = {}
role_deletion = {}
emoji_creation = {}
emoji_deletion = {}

max_channels_per_second_deletion = {}
max_channels_per_second_creation = {}
max_roles_per_second_deletion = {}
max_roles_per_second_creation = {}
max_emojis_per_second_deletion = {}
max_emojis_per_second_creation = {}

dm_nuke = {}
nuke_stats = {}

# Anti Spam
message_times = {}
warnings = {}
MAX_MESSAGES_PER_SECOND = {}
spam_stats = {}


async def revoke_member(server: discord.Guild, member: discord.Member):
    server_id = server.id
    role_id = quarantine_role_id[server_id]
    if quarantine_stats[server_id] and role_id:
        quarantine_role = discord.utils.get(server.roles, id=role_id)
        if quarantine_role and quarantine_role not in member.roles:
            try:
                await member.edit(roles=[quarantine_role])
            except Exception:
                usr = user[server.id]
                if warn_user_stats[server.id] and usr:
                    await usr.send(
                        f"{usr.mention} **[ *Anti-Nuke* **] Couldn't remove roles from {member.mention}")
        for channel in server.channels:
            if not all(permission is False for permission in channel.permissions_for(member)):
                await channel.set_permissions(member, overwrite=discord.Permissions.none())
        for category in server.categories:
            if not all(permission is False for permission in category.permissions_for(member)):
                await category.set_permissions(member, overwrite=discord.Permissions.none())


# on bot ready

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    change_status.start()
    print("Online!")


# help menu

@bot.tree.command(name='helpme')
async def helpme(interaction: discord.Interaction):
    emb = discord.Embed(colour=discord.Colour.random())
    emb.set_author(name="Help Menu")
    emb.add_field(name="/anti_nuke <on/off>",
                  value='```Enable / Disable nuke protection '
                        '| The protection contains of channel, role and emoji protection```')
    emb.add_field(name="/anti_spam <on/off> <messages per second>", value='```Enable / Disable spam protection```')
    emb.add_field(name="/anti_raid <on/off> <members leave per second> <members join per second>",
                  value='```Enable / Disable raid protection```')
    emb.add_field(name="/quarantine <on/off> <role id>", value='```Enable / Disable Quarantine```')
    emb.add_field(name="/warn_user <on/off> <user id>",
                  value='```Enable / Disable warning the member about the server```')
    await interaction.response.send_message(embed=emb)


# setters

@bot.tree.command(name='warn_user')
@has_permissions(administrator=True)
@app_commands.describe(mode='on/off', user_id="User ID to send DMs about server")
async def warn_user(interaction: discord.Interaction, mode: str, user_id: str):
    if user_id.isdigit():
        global warn_user_stats
        global user
        warn_user_stats[interaction.guild.id] = True if mode.lower() == "on" else False
        user[interaction.guild.id] = discord.utils.get(interaction.guild.members, id=int(user_id))
        if user[interaction.guild.id] :
            if warn_user_stats[interaction.guild.id]:
                emb = discord.Embed(colour=discord.Color.green())
                emb.add_field(name="Status", value='Enabled')
            else:
                emb = discord.Embed(colour=discord.Color.red())
                emb.add_field(name="Status", value='Disabled')
            emb.set_author(name="DM warnings")
            emb.add_field(name="User", value=user[interaction.guild.id].mention)
            await interaction.response.send_message(embed=emb)


@bot.tree.command(name='anti_raid')
@has_permissions(administrator=True)
@app_commands.describe(mode='on/off', members_leave_per_second="Amount of members to leave per second",
                       members_join_per_second="Amount of members to join per second")
async def anti_raid(interaction: discord.Interaction, mode: str, members_leave_per_second: str,
                    members_join_per_second: str):
    if members_leave_per_second.isdigit() and members_join_per_second.isdigit():
        global raid_stats
        global max_members_to_join_per_second
        global max_members_to_leave_per_second
        raid_stats[interaction.guild.id] = True if mode.lower() == "on" else False
        max_members_to_leave_per_second[interaction.guild.id] = int(members_leave_per_second)
        max_members_to_join_per_second[interaction.guild.id] = int(members_join_per_second)
        if raid_stats[interaction.guild.id]:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name="Status", value='Enabled')
        else:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name="Status", value='Disabled')
        emb.set_author(name="Anti Raid")
        emb.add_field(name="Member to leave per second", value=max_members_to_leave_per_second[interaction.guild.id])
        emb.add_field(name="Member to join per second", value=max_members_to_join_per_second[interaction.guild.id])
        await interaction.response.send_message(embed=emb)


@bot.tree.command(name='anti_spam')
@has_permissions(administrator=True)
@app_commands.describe(mode='on/off', sec="Messages per second")
async def anti_spam(interaction: discord.Interaction, mode: str, sec: str):
    if sec.isdigit():
        global MAX_MESSAGES_PER_SECOND
        MAX_MESSAGES_PER_SECOND[interaction.guild.id] = int(sec)

    global spam_stats
    spam_stats[interaction.guild.id] = True if mode.lower() == "on" else False
    if spam_stats[interaction.guild.id]:
        emb = discord.Embed(colour=discord.Colour.green())
        emb.add_field(name="Status", value='Enabled')
    else:
        emb = discord.Embed(colour=discord.Colour.red())
        emb.add_field(name="Status", value='Disabled')
    emb.set_author(name="Spam protection")
    await interaction.response.send_message(embed=emb)


@bot.tree.command(name='quarantine')
@has_permissions(administrator=True)
@app_commands.describe(mode='on/off', role_id="Quarantine role id")
async def quarantine(interaction: discord.Interaction, mode: str, role_id: str):
    global quarantine_role_id
    global quarantine_stats

    quarantine_stats[interaction.guild.id] = True if mode.lower() == "on" else False

    if quarantine_stats[interaction.guild.id]:
        emb = discord.Embed(color=discord.Color.green())
        emb.set_author(name="Enabled Retard Protection")
    else:
        emb = discord.Embed(color=discord.Color.red())
        emb.set_author(name="Disabled Retard Protection")

    if role_id.isdigit():
        quarantine_role = discord.utils.get(interaction.guild.roles, id=int(role_id))
        if quarantine_role:
            quarantine_role_id[interaction.guild.id] = int(role_id)
            emb.add_field(name="Quarantine Role", value=quarantine_role.mention)

    await interaction.response.send_message(embed=emb)


@bot.tree.command(name='anti_nuke')
@has_permissions(administrator=True)
@app_commands.describe(mode='on/off', creating_channels="Channels per second",
                       deleting_channels="Channels per second",
                       creating_roles="Roles per second",
                       deleting_roles="Roles per second",
                       creating_emojis="Emojis per second",
                       deleting_emojis="Emojis per second")
async def anti_nuke(interaction: discord.Interaction, mode: str,
                    creating_channels: str,
                    deleting_channels: str,
                    creating_roles: str,
                    deleting_roles: str,
                    creating_emojis: str,
                    deleting_emojis: str):
    global nuke_stats
    global max_channels_per_second_creation
    global max_channels_per_second_deletion
    global max_roles_per_second_deletion
    global max_roles_per_second_creation
    global max_emojis_per_second_creation
    global max_emojis_per_second_deletion
    nuke_stats[interaction.guild.id] = True if mode.lower() == "on" else False
    if nuke_stats[interaction.guild.id]:
        emb = discord.Embed(colour=discord.Colour.green())
        emb.add_field(name="Status", value='Enabled')
    else:
        emb = discord.Embed(colour=discord.Colour.red())
        emb.add_field(name="Status", value='Disabled')
    emb.set_author(name="Nuke protection")
    if creating_channels.isdigit():
        max_channels_per_second_creation[interaction.guild.id] = int(creating_channels)
        emb.add_field(name="Creating Channels per Second",
                      value=max_channels_per_second_creation[interaction.guild.id])

    if deleting_channels.isdigit():
        max_channels_per_second_deletion[interaction.guild.id] = int(creating_channels)
        emb.add_field(name="Deleting Channels per Second",
                      value=max_channels_per_second_deletion[interaction.guild.id])

    if creating_roles.isdigit():
        max_roles_per_second_creation[interaction.guild.id] = int(creating_roles)
        emb.add_field(name="Creating Roles per Second", value=max_roles_per_second_creation[interaction.guild.id])

    if deleting_roles.isdigit():
        max_roles_per_second_deletion[interaction.guild.id] = int(deleting_roles)
        emb.add_field(name="Deleting Roles per Second", value=max_roles_per_second_deletion[interaction.guild.id])

    if creating_emojis.isdigit():
        max_emojis_per_second_creation[interaction.guild.id] = int(creating_emojis)
        emb.add_field(name="Creating Emojis per Second", value=max_emojis_per_second_creation[interaction.guild.id])

    if deleting_emojis.isdigit():
        max_emojis_per_second_deletion[interaction.guild.id] = int(deleting_emojis)
        emb.add_field(name="Creating Roles per Second", value=max_emojis_per_second_deletion[interaction.guild.id])

    await interaction.response.send_message(embed=emb)


# activities

@bot.event
async def on_guild_channel_create(channel):
    if nuke_stats:
        global channel_creation
        global dm_nuke
        guild_server = channel.guild
        server = guild_server.id
        usr = user[server]
        warn = warn_user_stats[server]
        quarantine_role = quarantine_role_id[server]
        quarantine_stats_status = quarantine_stats[server]
        current_time = time.monotonic()
        if server not in channel_creation.keys():
            channel_creation[server] = current_time
            return
        if current_time - channel_creation[server] <= 1000 / max_channels_per_second_creation[server]:
            if server in dm_nuke.keys():
                if (current_time - dm_nuke[server]) >= 10 and warn and usr:
                    # send another warning message
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass channel creation")
                    dm_nuke[server] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role = discord.utils.get(guild_server.roles, id=quarantine_role)
                        if role:
                            async for entry in guild_server.audit_logs(limit=10,
                                                                action=discord.AuditLogAction.channel_create):
                                if entry.target.id == channel.id:
                                    mem = discord.utils.get(guild_server.members, id=entry.user.id)
                                    if mem and role not in mem.roles:
                                        await revoke_member(guild_server, mem)
                                        if warn and usr:
                                            await usr.send(
                                                f"{usr.mention} **[ *Anti-Nuke* **] "
                                                f"{mem.mention} was given the ```{role.name}``` role and took care of it.")
                                        break
            else:
                # send the initial warning message and record the time
                if warn and usr:
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass channel creation")
                dm_nuke[server] = current_time
                if quarantine_stats_status and quarantine_role:
                    role = discord.utils.get(guild_server.roles, id=quarantine_role)
                    if role:
                        async for entry in guild_server.audit_logs(limit=10,
                                                             action=discord.AuditLogAction.channel_create):
                            if entry.target.id == channel.id:
                                mem = discord.utils.get(guild_server.members, id=entry.user.id)
                                if mem and role not in mem.roles:
                                    await revoke_member(guild_server, mem)
                                    if warn and usr:
                                        await usr.send(
                                            f"{usr.mention} **[ *Anti-Nuke* **] "
                                            f"{mem.mention} was given the ```{role.name}``` role and took care of it.")
                                    break
        channel_creation[server] = current_time


@bot.event
async def on_guild_channel_delete(channel):
    if nuke_stats:
        global channel_deletion
        global dm_nuke

        guild_server = channel.guild
        server = guild_server.id
        usr = user[server]
        warn = warn_user_stats[server]
        quarantine_role = quarantine_role_id[server]
        quarantine_stats_status = quarantine_stats[server]
        current_time = time.monotonic()
        if server not in channel_deletion.keys():
            channel_deletion[server] = current_time
            return
        if current_time - channel_deletion[server] <= 1000 / max_channels_per_second_deletion[server]:
            if server in dm_nuke.keys():
                if (current_time - dm_nuke[server]) >= 10 and warn and usr:
                    # send another warning message
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass channel deletion")
                    dm_nuke[server] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role = discord.utils.get(guild_server.roles, id=quarantine_role_id)
                        if role:
                            async for entry in guild_server.audit_logs(limit=10,
                                                                 action=discord.AuditLogAction.channel_delete):
                                if entry.target.id == channel.id:
                                    mem = discord.utils.get(guild_server.members, id=entry.user.id)
                                    if mem and role not in mem.roles:
                                        await revoke_member(guild_server, mem)
                                        if warn and usr:
                                            await usr.send(
                                                f"{usr.mention} **[ *Anti-Nuke* **] "
                                                f"{mem.mention} was given the ```{role.name}``` role and took care of it.")
                                        break
            else:
                # send the initial warning message and record the time
                if warn and usr:
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass channel deletion")
                dm_nuke[server] = current_time
                if quarantine_stats_status and quarantine_role:
                    role = discord.utils.get(guild_server.roles, id=quarantine_role_id)
                    if role:
                        async for entry in guild_server.audit_logs(limit=10,
                                                             action=discord.AuditLogAction.channel_delete):
                            if entry.target.id == channel.id:
                                mem = discord.utils.get(guild_server.members, id=entry.user.id)
                                if mem and role not in mem.roles:
                                    await revoke_member(guild_server, mem)
                                    if warn and usr:
                                        await usr.send(
                                            f"{usr.mention} **[ *Anti-Nuke* **] "
                                            f"{mem.mention} was given the ```{role.name}``` role and took care of it.")
                                    break
        channel_deletion[server] = current_time


@bot.event
async def on_guild_role_create(role):
    if nuke_stats:
        global role_creation
        global dm_nuke

        server = role.guild
        server_id = server.id
        current_time = time.monotonic()
        if server_id not in role_creation.keys():
            role_creation[server_id] = current_time
            return

        usr = user[server_id]
        warn = warn_user_stats[server_id]
        quarantine_role = quarantine_role_id[server_id]
        quarantine_stats_status = quarantine_stats[server_id]
        if current_time - role_creation[server_id] <= 1000 / max_roles_per_second_creation[server_id]:
            if server_id in dm_nuke.keys():
                if (current_time - dm_nuke[server_id]) >= 10 and warn and usr:
                    # send another warning message
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass role creation")
                    dm_nuke[server_id] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role1 = discord.utils.get(server.roles, id=quarantine_role)
                        if role1:
                            async for entry in server.audit_logs(limit=10,
                                                                 action=discord.AuditLogAction.role_create):
                                if entry.target.id == role1.id:
                                    mem = discord.utils.get(server.members, id=entry.user.id)
                                    if mem and role1 not in mem.roles:
                                        await revoke_member(server, mem)
                                        if warn and usr:
                                            await usr.send(
                                                f"{usr.mention} **[ *Anti-Nuke* **] "
                                                f"{mem.mention} was given the ```{role1.name}``` role and took care of it.")
                                        break
            else:
                # send the initial warning message and record the time
                if warn and usr:
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass role creation")
                dm_nuke[server_id] = current_time
                if quarantine_stats_status and quarantine_role:
                    role1 = discord.utils.get(server.roles, id=quarantine_role)
                    if role1:
                        async for entry in server.audit_logs(limit=10,
                                                             action=discord.AuditLogAction.role_create):
                            if entry.target.id == role1.id:
                                mem = discord.utils.get(server.members, id=entry.user.id)
                                if mem and role1 not in mem.roles:
                                    await revoke_member(server, mem)
                                    if warn and usr:
                                        await usr.send(
                                            f"{usr.mention} **[ *Anti-Nuke* **] "
                                            f"{mem.mention} was given the ```{role1.name}``` role and took care of it.")
                                    break
        role_creation[server_id] = current_time


@bot.event
async def on_guild_role_delete(role):
    if nuke_stats:
        global role_deletion
        global dm_nuke

        server = role.guild
        server_id = server.id
        current_time = time.monotonic()
        if server not in role_deletion.keys():
            role_deletion[server_id] = current_time
            return
        usr = user[server_id]
        warn = warn_user_stats[server_id]
        quarantine_role = quarantine_role_id[server_id]
        quarantine_stats_status = quarantine_stats[server_id]
        if current_time - role_deletion[server_id] <= 1000 / max_roles_per_second_deletion[server_id]:
            if server_id in dm_nuke.keys():
                if (current_time - dm_nuke[server_id]) >= 10 and warn and usr:
                    # send another warning message
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass role deletion")
                    dm_nuke[server_id] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role1 = discord.utils.get(server.roles, id=quarantine_role)
                        if role1:
                            async for entry in server.audit_logs(limit=10,
                                                                 action=discord.AuditLogAction.role_delete):
                                if entry.target.id == role1.id:
                                    mem = discord.utils.get(server.members, id=entry.user.id)
                                    if mem and role1 not in mem.roles:
                                        await revoke_member(server, mem)
                                        if warn and usr:
                                            await usr.send(
                                                f"{usr.mention} **[ *Anti-Nuke* **] "
                                                f"{mem.mention} was given the ```{role1.name}``` role and took care of it.")
                                        break
            else:
                # send the initial warning message and record the time
                if warn and usr:
                    await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Mass role deletion")
                dm_nuke[server_id] = current_time
                if quarantine_stats_status and quarantine_role:
                    role1 = discord.utils.get(server.roles, id=quarantine_role)
                    if role1:
                        async for entry in server.audit_logs(limit=10,
                                                             action=discord.AuditLogAction.role_delete):
                            if entry.target.id == role1.id:
                                mem = discord.utils.get(server.members, id=entry.user.id)
                                if mem and role1 not in mem.roles:
                                    await revoke_member(server, mem)
                                    if warn and usr:
                                        await usr.send(
                                            f"{usr.mention} **[ *Anti-Nuke* **] "
                                            f"{mem.mention} was given the ```{role1.name}``` role and took care of it.")
                                    break
        role_deletion[server_id] = current_time


@bot.event
async def on_member_join(member):
    if raid_stats:
        global last_member_join
        global dm_join

        server = member.guild
        server_id = server.id
        current_time = time.monotonic()
        if server_id not in last_member_join.keys():
            last_member_join[server_id] = current_time
            return

        usr = user[server_id]
        warn = warn_user_stats[server_id]
        quarantine_role = quarantine_role_id[server_id]
        quarantine_stats_status = quarantine_stats[server_id]
        if current_time - last_member_join[server_id] <= 1000 / max_members_to_join_per_second[server_id]:
            if server_id in dm_join.keys():
                if (current_time - dm_join[server_id]) >= 10 and warn and usr:
                    # send another warning message
                    await usr.send(f"{usr.mention} **[ *Anti-Raid* **] Many members just joined")
                    dm_join[server_id] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role = discord.utils.get(server.roles, id=quarantine_role)
                        if role and role not in member.roles:
                            await member.add_roles(role)
                            if warn and usr:
                                await usr.send(f"{usr.mention} **[ *Anti-Raid* **] "
                                                f"{member.mention} was given the ```{role.name}``` role")

            else:
                # send the initial warning message and record the time
                if warn and usr:
                    await usr.send(f"{usr.mention} **[ *Anti-Raid* **] Many members just joined")
                dm_join[server_id] = current_time
                if quarantine_stats_status and quarantine_role:
                    role = discord.utils.get(server.roles, id=quarantine_role)
                    if role and role not in member.roles:
                        await member.add_roles(role)
                        if warn and usr:
                            await usr.send(f"{usr.mention} **[ *Anti-Raid* **] "
                                            f"{member.mention} was given the ```{role.name}``` role")
        last_member_join[server_id] = current_time


@bot.event
async def on_member_remove(member):
    if raid_stats:
        global last_member_leave
        global dm_leave

        server = member.guild
        server_id = server.id
        current_time = time.monotonic()
        if server_id not in last_member_leave.keys():
            last_member_leave[server_id] = current_time
            return
        usr = user[server_id]
        warn = warn_user_stats[server_id]
        quarantine_role = quarantine_role_id[server_id]
        quarantine_stats_status = quarantine_stats[server_id]
        if current_time - last_member_leave[server_id] <= 1000 / max_members_to_leave_per_second[server_id]:
            if server_id in dm_leave.keys():
                if (current_time - dm_leave[server_id]) >= 10 and warn and usr:
                    # send another warning message
                    await usr.send(f"{usr.mention} **[ *Anti-Raid* **] Many members just left")
                    dm_leave[server_id] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role = discord.utils.get(server.roles, id=quarantine_role)
                        if role and role not in member.roles:
                            await member.add_roles(role)
                            if warn and usr:
                                await usr.send(f"{usr.mention} **[ *Anti-Raid* **] "
                                                f"{member.mention} was given the ```{role.name}``` role")
            else:
                # send the initial warning message and record the time
                if warn and usr:
                    await usr.send(f"{usr.mention} **[ *Anti-Raid* **] Many members just left")
                dm_leave[server_id] = current_time
                if quarantine_stats_status and quarantine_role:
                    role = discord.utils.get(server.roles, id=quarantine_role)
                    if role and role not in member.roles:
                        await member.add_roles(role)
                        if warn and usr:
                            await usr.send(f"{usr.mention} **[ *Anti-Raid* **] "
                                            f"{member.mention} was given the ```{role.name}``` role")
        last_member_leave[server_id] = current_time


@bot.event
async def on_guild_emojis_update(before, after):
    if nuke_stats:
        server = before[0].guild
        added = [e for e in after if e not in before]
        removed = [e for e in before if e not in after]
        global dm_nuke

        server_id = server.id
        if added:
            #print(f"Emojis added to {guild.name}: {', '.join(str(e) for e in added)}")
            global emoji_creation
            server_id = server_id
            usr = user[server_id]
            warn = warn_user_stats[server_id]
            quarantine_role = quarantine_role_id[server_id]
            quarantine_stats_status = quarantine_stats[server_id]
            current_time = time.monotonic()
            if server_id not in emoji_creation.keys():
                emoji_creation[server_id] = current_time
                return

            if current_time - emoji_creation[server_id] <= 1000 / max_emojis_per_second_creation[server_id]:
                if server_id in dm_nuke.keys():
                    if (current_time - dm_nuke[server_id]) >= 10 and warn and usr:
                        # send another warning message
                        await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Many emojis have been added")
                        dm_nuke[server_id] = current_time
                        if quarantine_stats_status and quarantine_role:
                            role = discord.utils.get(server.roles, id=quarantine_role)
                            if role:
                                async for entry in server.audit_logs(limit=10,
                                                                    action=discord.AuditLogAction.emoji_create):
                                    if entry.target.id == added[0].id:
                                        mem = discord.utils.get(server.members, id=entry.user.id)
                                        if mem and role not in mem.roles:
                                            await revoke_member(server, mem)
                                            if warn and usr:
                                                await usr.send(
                                                    f"{usr.mention} **[ *Anti-Nuke* **] "
                                                    f"{mem.mention} was given the ```{role.name}``` role and took are of it.")
                                            break
                else:
                    # send the initial warning message and record the time
                    if warn and usr:
                        await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Many emojis have been added")
                    dm_nuke[server_id] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role = discord.utils.get(server.roles, id=quarantine_role)
                        if role:
                            async for entry in server.audit_logs(limit=10,
                                                                 action=discord.AuditLogAction.emoji_create):
                                if entry.target.id == added[0].id:
                                    mem = discord.utils.get(server.members, id=entry.user.id)
                                    if mem and role not in mem.roles:
                                        await revoke_member(server, mem)
                                        if warn and usr:
                                            await usr.send(
                                                f"{usr.mention} **[ *Anti-Nuke* **] "
                                                f"{mem.mention} was given the ```{role.name}``` role and took care of it.")
                                        break
            emoji_creation[server_id] = current_time
        elif removed:
            #print(f"Emojis removed from {guild.name}: {', '.join(str(e) for e in removed)}")
            global emoji_deletion
            server_id = server_id
            usr = user[server_id]
            warn = warn_user_stats[server_id]
            quarantine_role = quarantine_role_id[server_id]
            quarantine_stats_status = quarantine_stats[server_id]
            current_time = time.monotonic()
            if server_id not in emoji_deletion.keys():
                emoji_deletion[server_id] = current_time
                return

            if current_time - emoji_deletion[server_id] <= 1000 / max_emojis_per_second_deletion[server_id]:
                if server_id in dm_nuke.keys():
                    if (current_time - dm_nuke[server_id]) >= 10 and warn and usr:
                        # send another warning message
                        await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Many emojis have been deleted")
                        dm_nuke[server_id] = current_time
                        if quarantine_stats_status and quarantine_role:
                            role = discord.utils.get(server.roles, id=quarantine_role)
                            if role:
                                for entry in await server.audit_logs(limit=100,
                                                                     action=discord.AuditLogAction.emoji_delete).flatten():
                                    if entry.target.id == added[0].id:
                                        mem = discord.utils.get(server.members, id=entry.user.id)
                                        if mem and role not in mem.roles:
                                            await revoke_member(server, mem)
                                            if warn and usr:
                                                await usr.send(
                                                    f"{usr.mention} **[ *Anti-Nuke* **] "
                                                    f"{mem.mention} was given the ```{role.name}``` role and took care of it.")
                                            break
                else:
                    # send the initial warning message and record the time
                    if warn and usr:
                        await usr.send(f"{usr.mention} **[ *Anti-Nuke* **] Many emojis have been deleted")
                    dm_nuke[server_id] = current_time
                    if quarantine_stats_status and quarantine_role:
                        role = discord.utils.get(server.roles, id=quarantine_role)
                        if role:
                            for entry in await server.audit_logs(limit=100,
                                                                 action=discord.AuditLogAction.emoji_delete).flatten():
                                if entry.target.id == added[0].id:
                                    mem = discord.utils.get(server.members, id=entry.user.id)
                                    if mem and role not in mem.roles:
                                        await revoke_member(server, mem)
                                        if warn and usr:
                                            await usr.send(
                                                f"{usr.mention} **[ *Anti-Nuke* **] "
                                                f"{mem.mention} was given the ```{role.name}``` role and took care of it.")
                                        break
            emoji_deletion[server_id] = current_time


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if spam_stats:
        global message_times
        global warnings
        author = message.author.id
        current_time = time.monotonic()
        if author not in message_times.keys():
            message_times[author] = current_time
            return
        if current_time - message_times[author] <= 1000 / MAX_MESSAGES_PER_SECOND[message.guild.id]:
            if author in warnings:
                if (current_time - warnings[author]) >= 10:
                    # send another warning message
                    await message.channel.send(f"{message.author.mention}, please don't spam messages.")
                    warnings[author] = current_time
            else:
                # send the initial warning message and record the time
                await message.channel.send(f"{message.author.mention}, please don't spam messages.")
                warnings[author] = current_time

        message_times[author] = current_time


# tasks

activities = ["o", "i", "d"]
status = ["Yoo!",
          "/helpme - help menu",
          "Anti-Nuke, Anti-Spam, Anti-Raid, Quarantine",
          "Watching over a server"
          ]


@tasks.loop(seconds=5)
async def change_status():
    botStats = random.randint(0, len(status) - 1)
    acStats = random.randint(0, len(activities) - 1)
    stats_ = activities[acStats]
    if stats_ == "o":
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=status[botStats]))
    elif stats_ == "i":
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=status[botStats]))
    else:
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(name=status[botStats]))


if __name__ == "__main__":
    bot.run("Bot token here")
