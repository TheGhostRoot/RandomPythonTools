import discord
from discord.ext import commands
import json
import time
import os
import requests
import datetime

bot = commands.Bot(command_prefix="!!!", bot=True, self_bot=False, intents=discord.Intents.all())

server_data = {}


# create the backup
async def add_roles(guild: discord.Guild):
    global server_data
    server_data["roles"] = {}
    for role in guild.roles:
        perms = role.permissions
        server_data["roles"][role.id] = {
            "display_icon_url": str(role.display_icon.url) if role.display_icon is not None and type(
                role.display_icon) is not str else None,
            "name": role.name,
            "id": role.id,
            "created_at": str(role.created_at),
            "position": role.position,
            "colour": str(role.colour),
            "color": str(role.color),
            "is_default": role.is_default(),
            "is_bot_managed": role.is_bot_managed(),
            "is_premium_subscriber": role.is_premium_subscriber(),
            "is_assignable": role.is_assignable(),
            "is_integration": role.is_integration(),
            "hoist": role.hoist,
            "mentionable": role.mentionable,
            "permissions": {
                "mention_everyone": perms.mention_everyone,
                "stream": perms.stream,
                "add_reactions": perms.add_reactions,
                "administrator": perms.administrator,
                "attach_files": perms.attach_files,
                "change_nickname": perms.change_nickname,
                "ban_members": perms.ban_members,
                "connect": perms.connect,
                "create_instant_invite": perms.create_instant_invite,
                "create_private_threads": perms.create_private_threads,
                "create_public_threads": perms.create_public_threads,
                "deafen_members": perms.deafen_members,
                "embed_links": perms.embed_links,
                "external_emojis": perms.external_emojis,
                "external_stickers": perms.external_stickers,
                "kick_members": perms.kick_members,
                "manage_channels": perms.manage_channels,
                "manage_emojis": perms.manage_emojis,
                "manage_emojis_and_stickers": perms.manage_emojis_and_stickers,
                "manage_events": perms.manage_events,
                "manage_guild": perms.manage_guild,
                "manage_messages": perms.manage_messages,
                "manage_nicknames": perms.manage_nicknames,
                "manage_permissions": perms.manage_permissions,
                "manage_roles": perms.manage_roles,
                "manage_threads": perms.manage_threads,
                "manage_webhooks": perms.manage_webhooks,
                "moderate_members": perms.moderate_members,
                "move_members": perms.move_members,
                "mute_members": perms.mute_members,
                "priority_speaker": perms.priority_speaker,
                "read_message_history": perms.read_message_history,
                "read_messages": perms.read_messages,
                "request_to_speak": perms.request_to_speak,
                "send_messages": perms.send_messages,
                "send_messages_in_threads": perms.send_messages_in_threads,
                "send_tts_messages": perms.send_tts_messages,
                "speak": perms.speak,
                "use_application_commands": perms.use_application_commands,
                "use_embedded_activities": perms.use_embedded_activities,
                "use_external_emojis": perms.use_external_emojis,
                "use_external_stickers": perms.use_external_stickers,
                "use_voice_activation": perms.use_voice_activation,
                "view_audit_log": perms.view_audit_log,
                "view_channel": perms.view_channel,
                "view_guild_insights": perms.view_guild_insights
            }
        }


async def add_categories(guild: discord.Guild):
    global server_data
    server_data["categories"] = {}
    for category in guild.categories:
        permissions = {}
        for role in guild.roles:
            perms = category.permissions_for(role)
            permissions[role.id] = {
                "name": role.name,
                "mention_everyone": perms.mention_everyone,
                "stream": perms.stream,
                "add_reactions": perms.add_reactions,
                "administrator": perms.administrator,
                "attach_files": perms.attach_files,
                "change_nickname": perms.change_nickname,
                "ban_members": perms.ban_members,
                "connect": perms.connect,
                "create_instant_invite": perms.create_instant_invite,
                "create_private_threads": perms.create_private_threads,
                "create_public_threads": perms.create_public_threads,
                "deafen_members": perms.deafen_members,
                "embed_links": perms.embed_links,
                "external_emojis": perms.external_emojis,
                "external_stickers": perms.external_stickers,
                "kick_members": perms.kick_members,
                "manage_channels": perms.manage_channels,
                "manage_emojis": perms.manage_emojis,
                "manage_emojis_and_stickers": perms.manage_emojis_and_stickers,
                "manage_events": perms.manage_events,
                "manage_guild": perms.manage_guild,
                "manage_messages": perms.manage_messages,
                "manage_nicknames": perms.manage_nicknames,
                "manage_permissions": perms.manage_permissions,
                "manage_roles": perms.manage_roles,
                "manage_threads": perms.manage_threads,
                "manage_webhooks": perms.manage_webhooks,
                "moderate_members": perms.moderate_members,
                "move_members": perms.move_members,
                "mute_members": perms.mute_members,
                "priority_speaker": perms.priority_speaker,
                "read_message_history": perms.read_message_history,
                "read_messages": perms.read_messages,
                "request_to_speak": perms.request_to_speak,
                "send_messages": perms.send_messages,
                "send_messages_in_threads": perms.send_messages_in_threads,
                "send_tts_messages": perms.send_tts_messages,
                "speak": perms.speak,
                "use_application_commands": perms.use_application_commands,
                "use_embedded_activities": perms.use_embedded_activities,
                "use_external_emojis": perms.use_external_emojis,
                "use_external_stickers": perms.use_external_stickers,
                "use_voice_activation": perms.use_voice_activation,
                "view_audit_log": perms.view_audit_log,
                "view_channel": perms.view_channel,
                "view_guild_insights": perms.view_guild_insights
            }

        category_info = {
            "name": category.name,
            "id": category.id,
            "position": category.position,
            "created_at": str(category.created_at),
            "is_nsfw": category.is_nsfw(),
            "type_name": str(category.type.name),
            "type_value": category.type.value,
            "permissions": permissions,
            "channels": {}
        }

        for channel in category.channels:
            category_info["channels"][channel.id] = {
                "name": channel.name,
                "id": channel.id,
                "position": channel.position,
                "type_name": str(channel.type.name),
                "type_value": channel.type.value,
                "created_at": str(channel.created_at),
                "permissions": {}
            }

            if type(channel) is not discord.VoiceChannel:
                webhook = await channel.webhooks()
                if type(channel) is discord.ForumChannel:
                    category_info["channels"][channel.id] = {
                        "name": channel.name,
                        "id": channel.id,
                        "position": channel.position,
                        "type_name": str(channel.type.name),
                        "type_value": channel.type.value,
                        "created_at": str(channel.created_at),
                        "webhooks": {},
                        "is_nsfw": channel.is_nsfw(),
                        "topic": str(channel.topic) if channel.topic is not None else None,
                        "permissions": {}
                    }
                else:
                    category_info["channels"][channel.id] = {
                        "name": channel.name,
                        "id": channel.id,
                        "position": channel.position,
                        "type_name": str(channel.type.name),
                        "type_value": channel.type.value,
                        "created_at": str(channel.created_at),
                        "webhooks": {},
                        "is_news": channel.is_news(),
                        "is_nsfw": channel.is_nsfw(),
                        "topic": str(channel.topic) if channel.topic is not None else None,
                        "permissions": {}
                    }
                if type(channel) is not discord.ForumChannel:
                    category_info["channels"][channel.id]["slowmode_delay"] = int(channel.slowmode_delay)
                for web in webhook:
                    category_info["channels"][channel.id]["webhooks"][web.id] = {
                        "name": web.name,
                        "url": str(web.url),
                        "created_at": str(web.created_at),
                        "channel_id": web.channel_id,
                        "avatar_url": str(web.avatar.url) if web.avatar is not None else None,
                        "token": str(web.token) if web.token is not None else None,
                        "auth_token": str(web.auth_token) if web.auth_token is not None else None,
                        "is_authenticated": web.is_authenticated(),
                        "is_partial": web.is_partial(),
                        "proxy": str(web.proxy) if web.proxy is not None else None,
                        "proxy_auth": str(web.proxy_auth) if web.proxy_auth is not None else None
                    }
            else:
                category_info["channels"][channel.id]["bitrate"] = int(channel.bitrate)
                category_info["channels"][channel.id]["user_limit"] = int(channel.user_limit)
                category_info["channels"][channel.id]["video_quality_mode"] = str(channel.video_quality_mode)

            for r in guild.roles:
                perms = channel.permissions_for(r)
                category_info["channels"][channel.id]["permissions"][r.id] = {
                    "name": r.name,
                    "mention_everyone": perms.mention_everyone,
                    "stream": perms.stream,
                    "add_reactions": perms.add_reactions,
                    "administrator": perms.administrator,
                    "attach_files": perms.attach_files,
                    "change_nickname": perms.change_nickname,
                    "ban_members": perms.ban_members,
                    "connect": perms.connect,
                    "create_instant_invite": perms.create_instant_invite,
                    "create_private_threads": perms.create_private_threads,
                    "create_public_threads": perms.create_public_threads,
                    "deafen_members": perms.deafen_members,
                    "embed_links": perms.embed_links,
                    "external_emojis": perms.external_emojis,
                    "external_stickers": perms.external_stickers,
                    "kick_members": perms.kick_members,
                    "manage_channels": perms.manage_channels,
                    "manage_emojis": perms.manage_emojis,
                    "manage_emojis_and_stickers": perms.manage_emojis_and_stickers,
                    "manage_events": perms.manage_events,
                    "manage_guild": perms.manage_guild,
                    "manage_messages": perms.manage_messages,
                    "manage_nicknames": perms.manage_nicknames,
                    "manage_permissions": perms.manage_permissions,
                    "manage_roles": perms.manage_roles,
                    "manage_threads": perms.manage_threads,
                    "manage_webhooks": perms.manage_webhooks,
                    "moderate_members": perms.moderate_members,
                    "move_members": perms.move_members,
                    "mute_members": perms.mute_members,
                    "priority_speaker": perms.priority_speaker,
                    "read_message_history": perms.read_message_history,
                    "read_messages": perms.read_messages,
                    "request_to_speak": perms.request_to_speak,
                    "send_messages": perms.send_messages,
                    "send_messages_in_threads": perms.send_messages_in_threads,
                    "send_tts_messages": perms.send_tts_messages,
                    "speak": perms.speak,
                    "use_application_commands": perms.use_application_commands,
                    "use_embedded_activities": perms.use_embedded_activities,
                    "use_external_emojis": perms.use_external_emojis,
                    "use_external_stickers": perms.use_external_stickers,
                    "use_voice_activation": perms.use_voice_activation,
                    "view_audit_log": perms.view_audit_log,
                    "view_channel": perms.view_channel,
                    "view_guild_insights": perms.view_guild_insights
                }

        server_data["categories"][category.id] = category_info


async def create_backup(guild: discord.Guild):
    global server_data
    server_data["backup_time"] = str(datetime.datetime.now())
    server_data["name"] = guild.name
    server_data["banner_url"] = guild.banner.url if guild.banner is not None else None
    server_data["description"] = guild.description if guild.description is not None else None
    server_data["splash_url"] = guild.splash.url if guild.splash is not None else None
    server_data["discovery_splash_url"] = guild.discovery_splash.url if guild.discovery_splash is not None else None
    server_data["id"] = guild.id
    server_data[
        "premium_progress_bar_enabled"] = guild.premium_progress_bar_enabled if guild.premium_progress_bar_enabled is not None else None
    server_data["public_updates_channel"] = str(
        guild.public_updates_channel) if guild.public_updates_channel is not None else None
    server_data["rules_channel"] = str(guild.rules_channel) if guild.rules_channel is not None else None
    server_data["preferred_locale"] = str(guild.preferred_locale) if guild.preferred_locale is not None else None
    server_data["system_channel_flags"] = str(
        guild.system_channel_flags) if guild.system_channel_flags is not None else None
    server_data["vanity_url_code"] = str(guild.vanity_url_code) if guild.vanity_url_code is not None else None
    server_data["explicit_content_filter"] = str(
        guild.explicit_content_filter) if guild.explicit_content_filter is not None else None
    server_data["verification_level"] = str(guild.verification_level) if guild.verification_level is not None else None
    server_data["default_notifications"] = str(
        guild.default_notifications) if guild.default_notifications is not None else None
    server_data["large"] = guild.large
    server_data["owner_name"] = guild.owner.name
    server_data["owner_id"] = guild.owner.id
    server_data["created_at"] = str(guild.created_at)
    server_data["system_channel"] = str(guild.system_channel) if guild.system_channel is not None else None
    server_data["system_channel_id"] = guild.system_channel.id if guild.system_channel is not None else None
    server_data[
        "system_channel_category_name"] = guild.system_channel.category.name if guild.system_channel is not None else None
    server_data[
        "system_channel_category_id"] = guild.system_channel.category.id if guild.system_channel is not None else None
    server_data["icon_url"] = guild.icon.url if guild.icon is not None else None
    server_data["afk_timeout"] = guild.afk_timeout if guild.afk_timeout is not None else None
    server_data["mfa_level"] = str(guild.mfa_level) if guild.mfa_level is not None else None
    server_data["banner_key"] = guild.banner.key if guild.banner is not None else None
    server_data["afk_channel"] = str(guild.afk_channel) if guild.afk_channel is not None else None
    server_data["afk_channel_id"] = guild.afk_channel.id if guild.afk_channel is not None else None
    server_data[
        "afk_channel_category_name"] = guild.afk_channel.category.name if guild.afk_channel is not None else None
    server_data["afk_channel_category_id"] = guild.afk_channel.category.id if guild.afk_channel is not None else None
    server_data["emojis"] = {}
    for e in guild.emojis:
        server_data["emojis"][e.id] = {
            "name": e.name,
            "id": e.id,
            "url": str(e.url),
            "created_at": str(e.created_at),
            "user": str(e.user),
            "animated": e.animated,
            "require_colons": e.require_colons
        }
    await add_roles(guild=guild)
    await add_categories(guild=guild)


# load the backup
async def load_roles(guild: discord.Guild, server_backup: dict):
    for role_id, role_data in server_backup['roles'].items():
        settings = server_backup["roles"][role_id]
        time.sleep(2)
        if settings["name"] == "@everyone":
            r = discord.utils.get(guild.roles, name="@everyone")
            perms = settings["permissions"]
            await r.edit(permissions=discord.Permissions(
                mention_everyone=bool(perms['mention_everyone']),
                stream=bool(perms['stream']),
                add_reactions=bool(perms['add_reactions']),
                administrator=bool(perms['administrator']),
                attach_files=bool(perms['attach_files']),
                change_nickname=bool(perms['change_nickname']),
                ban_members=bool(perms['ban_members']),
                connect=bool(perms['connect']),
                create_instant_invite=bool(perms['create_instant_invite']),
                create_private_threads=bool(perms['create_private_threads']),
                create_public_threads=bool(perms['create_public_threads']),
                deafen_members=bool(perms['deafen_members']),
                embed_links=bool(perms['embed_links']),
                external_emojis=bool(perms['external_emojis']),
                external_stickers=bool(perms['external_stickers']),
                kick_members=bool(perms['kick_members']),
                manage_channels=bool(perms['manage_channels']),
                manage_emojis=bool(perms['manage_emojis']),
                manage_emojis_and_stickers=bool(perms['manage_emojis_and_stickers']),
                manage_events=bool(perms['manage_events']),
                manage_guild=bool(perms['manage_guild']),
                manage_messages=bool(perms['manage_messages']),
                manage_nicknames=bool(perms['manage_nicknames']),
                manage_permissions=bool(perms['manage_permissions']),
                manage_roles=bool(perms['manage_roles']),
                manage_threads=bool(perms['manage_threads']),
                manage_webhooks=bool(perms['manage_webhooks']),
                moderate_members=bool(perms['moderate_members']),
                move_members=bool(perms['move_members']),
                mute_members=bool(perms['mute_members']),
                priority_speaker=bool(perms['priority_speaker']),
                read_message_history=bool(perms['read_message_history']),
                read_messages=bool(perms['read_messages']),
                request_to_speak=bool(perms['request_to_speak']),
                send_messages=bool(perms['send_messages']),
                send_messages_in_threads=bool(perms['send_messages_in_threads']),
                send_tts_messages=bool(perms['send_tts_messages']),
                speak=bool(perms['speak']),
                use_application_commands=bool(perms['use_application_commands']),
                use_embedded_activities=bool(perms['use_embedded_activities']),
                use_external_emojis=bool(perms['use_external_emojis']),
                use_external_stickers=bool(perms['use_external_stickers']),
                use_voice_activation=bool(perms['use_voice_activation']),
                view_audit_log=bool(perms['view_audit_log']),
                view_channel=bool(perms['view_channel']),
                view_guild_insights=bool(perms['view_guild_insights'])
            )
            )
        else:
            icon = None
            if settings["display_icon_url"] is not None:
                icon_resp = requests.get(settings["display_icon_url"])
                icon = icon_resp.content
            perms = settings["permissions"]
            try:
                role = await guild.create_role(
                    name=settings["name"] if settings["name"] is not None else None,
                    color=discord.Color(int(settings["color"][1:], 16)) if settings["color"] is not None else None,
                    display_icon=icon if settings["display_icon_url"] is not None else None,
                    hoist=settings["hoist"] if settings["hoist"] is not None else None,
                    mentionable=settings["mentionable"] if settings["mentionable"] is not None else None,
                    permissions=discord.Permissions(
                        mention_everyone=bool(perms['mention_everyone']),
                        stream=bool(perms['stream']),
                        add_reactions=bool(perms['add_reactions']),
                        administrator=bool(perms['administrator']),
                        attach_files=bool(perms['attach_files']),
                        change_nickname=bool(perms['change_nickname']),
                        ban_members=bool(perms['ban_members']),
                        connect=bool(perms['connect']),
                        create_instant_invite=bool(perms['create_instant_invite']),
                        create_private_threads=bool(perms['create_private_threads']),
                        create_public_threads=bool(perms['create_public_threads']),
                        deafen_members=bool(perms['deafen_members']),
                        embed_links=bool(perms['embed_links']),
                        external_emojis=bool(perms['external_emojis']),
                        external_stickers=bool(perms['external_stickers']),
                        kick_members=bool(perms['kick_members']),
                        manage_channels=bool(perms['manage_channels']),
                        manage_emojis=bool(perms['manage_emojis']),
                        manage_emojis_and_stickers=bool(perms['manage_emojis_and_stickers']),
                        manage_events=bool(perms['manage_events']),
                        manage_guild=bool(perms['manage_guild']),
                        manage_messages=bool(perms['manage_messages']),
                        manage_nicknames=bool(perms['manage_nicknames']),
                        manage_permissions=bool(perms['manage_permissions']),
                        manage_roles=bool(perms['manage_roles']),
                        manage_threads=bool(perms['manage_threads']),
                        manage_webhooks=bool(perms['manage_webhooks']),
                        moderate_members=bool(perms['moderate_members']),
                        move_members=bool(perms['move_members']),
                        mute_members=bool(perms['mute_members']),
                        priority_speaker=bool(perms['priority_speaker']),
                        read_message_history=bool(perms['read_message_history']),
                        read_messages=bool(perms['read_messages']),
                        request_to_speak=bool(perms['request_to_speak']),
                        send_messages=bool(perms['send_messages']),
                        send_messages_in_threads=bool(perms['send_messages_in_threads']),
                        send_tts_messages=bool(perms['send_tts_messages']),
                        speak=bool(perms['speak']),
                        use_application_commands=bool(perms['use_application_commands']),
                        use_embedded_activities=bool(perms['use_embedded_activities']),
                        use_external_emojis=bool(perms['use_external_emojis']),
                        use_external_stickers=bool(perms['use_external_stickers']),
                        use_voice_activation=bool(perms['use_voice_activation']),
                        view_audit_log=bool(perms['view_audit_log']),
                        view_channel=bool(perms['view_channel']),
                        view_guild_insights=bool(perms['view_guild_insights'])
                    )
                )
                await role.edit(position=settings["position"])
            except Exception:
                continue


async def load_emojis(guild: discord.Guild, server_backup: dict):
    if len(server_backup["emojis"]) == 0:
        return

    for emoji_id in server_backup["emojis"].keys():
        settings = server_backup["emojis"][emoji_id]

        img = None
        if settings["url"] is not None:
            img_resp = requests.get(settings["url"])
            img = img_resp.content

        await guild.create_custom_emoji(
            name=settings["name"],
            image=img if settings["url"] is not None else None
        )


async def load_categories(guild: discord.Guild, server_backup: dict):
    # load webhooks like list()
    # they are string
    if len(server_backup["categories"]) == 0:
        return

    categories = server_backup['categories']

    for category_id, category_data in categories.items():
        permission_overwrites = {}
        for role_id, permissions in category_data["permissions"].items():
            role = discord.utils.get(guild.roles, name=permissions['name'])
            if role is None:
                continue
            permission_overwrites[role] = discord.PermissionOverwrite(
                mention_everyone=permissions['mention_everyone'],
                stream=permissions['stream'],
                add_reactions=permissions['add_reactions'],
                administrator=permissions['administrator'],
                attach_files=permissions['attach_files'],
                change_nickname=permissions['change_nickname'],
                ban_members=permissions['ban_members'],
                connect=permissions['connect'],
                create_instant_invite=permissions['create_instant_invite'],
                create_private_threads=permissions['create_private_threads'],
                create_public_threads=permissions['create_public_threads'],
                deafen_members=permissions['deafen_members'],
                embed_links=permissions['embed_links'],
                external_emojis=permissions['external_emojis'],
                external_stickers=permissions['external_stickers'],
                kick_members=permissions['kick_members'],
                manage_channels=permissions['manage_channels'],
                manage_emojis=permissions['manage_emojis'],
                manage_emojis_and_stickers=permissions['manage_emojis_and_stickers'],
                manage_events=permissions['manage_events'],
                manage_guild=permissions['manage_guild'],
                manage_messages=permissions['manage_messages'],
                manage_nicknames=permissions['manage_nicknames'],
                manage_permissions=permissions['manage_permissions'],
                manage_roles=permissions['manage_roles'],
                manage_threads=permissions['manage_threads'],
                manage_webhooks=permissions['manage_webhooks'],
                moderate_members=permissions['moderate_members'],
                move_members=permissions['move_members'],
                mute_members=permissions['mute_members'],
                priority_speaker=permissions['priority_speaker'],
                read_message_history=permissions['read_message_history'],
                read_messages=permissions['read_messages'],
                request_to_speak=permissions['request_to_speak'],
                send_messages=permissions['send_messages'],
                send_messages_in_threads=permissions['send_messages_in_threads'],
                send_tts_messages=permissions['send_tts_messages'],
                speak=permissions['speak'],
                use_application_commands=permissions['use_application_commands'],
                use_embedded_activities=permissions['use_embedded_activities'],
                use_external_emojis=permissions['use_external_emojis'],
                use_external_stickers=permissions['use_external_stickers'],
                use_voice_activation=permissions['use_voice_activation'],
                view_audit_log=permissions['view_audit_log'],
                view_channel=permissions['view_channel'],
                view_guild_insights=permissions['view_guild_insights']
            )
        if len(permission_overwrites) < 99:
            category = await guild.create_category(
                name=category_data['name'],
                position=category_data['position'],
                overwrites=permission_overwrites
            )
        else:
            perm_chunks = []
            total_over = {}
            for role, perms in permission_overwrites.items():
                total_over[role] = perms
                if len(total_over) >= 99:
                    perm_chunks.append(total_over)
                    total_over = {}

            category = await guild.create_category(
                name=category_data['name'],
                position=category_data['position'],
                overwrites=perm_chunks[0]
            )

            for over in perm_chunks[1:]:
                await category.set_permissions(overwrite=over)
                time.sleep(1)
        # time.sleep(1)

        for channel_id, channel_data in category_data["channels"].items():
            channel_type = channel_data['type_name']

            try:
                channel_nsfw = bool(channel_data['is_nsfw'])
            except Exception:
                channel_nsfw = None
            try:
                channel_topic = channel_data['topic'] if channel_data['topic'] is not None else None
            except Exception:
                channel_topic = None
            channel_position = int(channel_data['position'])
            channel_name = channel_data['name']
            # time.sleep(2)
            overwrites2 = {}
            for role_id, permissions in channel_data["permissions"].items():
                role = discord.utils.get(guild.roles, name=permissions['name'])
                if role is None:
                    continue
                overwrites2[role] = discord.PermissionOverwrite(
                    mention_everyone=permissions['mention_everyone'],
                    stream=permissions['stream'],
                    add_reactions=permissions['add_reactions'],
                    administrator=permissions['administrator'],
                    attach_files=permissions['attach_files'],
                    change_nickname=permissions['change_nickname'],
                    ban_members=permissions['ban_members'],
                    connect=permissions['connect'],
                    create_instant_invite=permissions['create_instant_invite'],
                    create_private_threads=permissions['create_private_threads'],
                    create_public_threads=permissions['create_public_threads'],
                    deafen_members=permissions['deafen_members'],
                    embed_links=permissions['embed_links'],
                    external_emojis=permissions['external_emojis'],
                    external_stickers=permissions['external_stickers'],
                    kick_members=permissions['kick_members'],
                    manage_channels=permissions['manage_channels'],
                    manage_emojis=permissions['manage_emojis'],
                    manage_emojis_and_stickers=permissions['manage_emojis_and_stickers'],
                    manage_events=permissions['manage_events'],
                    manage_guild=permissions['manage_guild'],
                    manage_messages=permissions['manage_messages'],
                    manage_nicknames=permissions['manage_nicknames'],
                    manage_permissions=permissions['manage_permissions'],
                    manage_roles=permissions['manage_roles'],
                    manage_threads=permissions['manage_threads'],
                    manage_webhooks=permissions['manage_webhooks'],
                    moderate_members=permissions['moderate_members'],
                    move_members=permissions['move_members'],
                    mute_members=permissions['mute_members'],
                    priority_speaker=permissions['priority_speaker'],
                    read_message_history=permissions['read_message_history'],
                    read_messages=permissions['read_messages'],
                    request_to_speak=permissions['request_to_speak'],
                    send_messages=permissions['send_messages'],
                    send_messages_in_threads=permissions['send_messages_in_threads'],
                    send_tts_messages=permissions['send_tts_messages'],
                    speak=permissions['speak'],
                    use_application_commands=permissions['use_application_commands'],
                    use_embedded_activities=permissions['use_embedded_activities'],
                    use_external_emojis=permissions['use_external_emojis'],
                    use_external_stickers=permissions['use_external_stickers'],
                    use_voice_activation=permissions['use_voice_activation'],
                    view_audit_log=permissions['view_audit_log'],
                    view_channel=permissions['view_channel'],
                    view_guild_insights=permissions['view_guild_insights']
                )

            perm_chunks2 = []
            total_over2 = {}
            for role, perms in overwrites2.items():
                total_over2[role] = perms
                if len(total_over2) >= 99:
                    perm_chunks2.append(total_over2)
                    total_over2 = {}

            if (channel_type == 'voice') or ('stage' in channel_type):
                try:
                    vq = discord.VideoQualityMode(channel_data['video_quality_mode'])
                except Exception:
                    vq = discord.VideoQualityMode.full
                if len(overwrites2) < 99:
                    channel_voice = await guild.create_voice_channel(
                        name=channel_name,
                        category=category,
                        position=channel_position,
                        video_quality_mode=vq,
                        overwrites=overwrites2
                    )
                else:
                    channel_voice = await guild.create_voice_channel(
                        name=channel_name,
                        category=category,
                        position=channel_position,
                        video_quality_mode=vq,
                        overwrites=perm_chunks2[0]
                    )
                    for over in perm_chunks2[1:]:
                        for r, p in over.items():
                            await channel_voice.set_permissions(target=r, overwrite=p)
                            time.sleep(1)
            else:
                webhooks = dict(channel_data["webhooks"])
                if len(overwrites2) < 99:
                    channel_text = await guild.create_text_channel(
                        name=channel_name,
                        category=category,
                        position=channel_position,
                        #news=channel_news,
                        nsfw=channel_nsfw,
                        topic=channel_topic,
                        overwrites=overwrites2
                    )
                else:
                    channel_text = await guild.create_text_channel(
                        name=channel_name,
                        category=category,
                        position=channel_position,
                        #news=channel_news,
                        nsfw=channel_nsfw,
                        topic=channel_topic,
                        overwrites=perm_chunks2[0]
                    )
                    for over in perm_chunks2[1:]:
                        for r, p in over.items():
                            await channel_text.set_permissions(target=r, overwrite=p)
                            time.sleep(1)
                for web_id, web_settings in webhooks.items():
                        #iconr = requests.get(web_settings["avatar_url"])
                        #icon = iconr.content
                        #, avatar=web_settings["avatar_url"]
                        await channel_text.create_webhook(name=web_settings["name"])
                        time.sleep(1)


async def load_backup_and_delete(guild: discord.Guild, server_backup: dict):
    for r in guild.roles:
        if r.name != "@everyone":
            try:
                await r.delete()
            except Exception:
                continue
            time.sleep(1)

    for e in guild.emojis:
        try:
            await e.delete()
        except Exception:
            continue
        time.sleep(1)

    for cat in guild.categories:
        try:
            await cat.delete()
        except Exception:
            continue

    for cha in guild.channels:
        try:
            await cha.delete()
        except Exception:
            continue

    icon = None
    if server_backup["icon_url"] is not None:
        icon_resp = requests.get(server_backup["icon_url"])
        icon = icon_resp.content

    banner = None
    if server_backup["banner_url"] is not None:
        banner_resp = requests.get(server_backup["banner_url"])
        banner = banner_resp.content

    splash = None
    if server_backup["splash_url"] is not None:
        splash_resp = requests.get(server_backup["splash_url"])
        splash = splash_resp.content

    discovery_splash = None
    if server_backup["discovery_splash_url"] is not None:
        discovery_splash_resp = requests.get(server_backup["discovery_splash_url"])
        discovery_splash = discovery_splash_resp.content

    content_filter = None
    if server_backup["explicit_content_filter"] is not None:
        if server_backup["explicit_content_filter"] == "all_members":
            content_filter = discord.ContentFilter.all_members
        elif server_backup["explicit_content_filter"] == "no_roles":
            content_filter = discord.ContentFilter.no_role
        else:
            content_filter = discord.ContentFilter.disabled

    time.sleep(1)
    await guild.edit(
        name=server_backup["name"],
        description=server_backup["description"],
        icon=icon if server_backup["icon_url"] is not None else None,
        banner=banner if server_backup["banner_url"] is not None else None,
        splash=splash if server_backup["splash_url"] is not None else None,
        discovery_splash=discovery_splash if server_backup["discovery_splash_url"] is not None else None,
        afk_timeout=server_backup["afk_timeout"] if server_backup["afk_timeout"] is not None else None,
        default_notifications=getattr(discord.NotificationLevel,
                                      server_backup["default_notifications"].split(".")[1]) if server_backup[
                                                                                                   "default_notifications"] is not None else None,
        verification_level=discord.VerificationLevel[server_backup["verification_level"]] if server_backup[
                                                                                                 "verification_level"] is not None else None,
        explicit_content_filter=content_filter if server_backup["explicit_content_filter"] is not None else None,
        preferred_locale=server_backup["preferred_locale"] if server_backup["preferred_locale"] is not None else None,
        premium_progress_bar_enabled=server_backup["premium_progress_bar_enabled"] if server_backup[
                                                                                          "premium_progress_bar_enabled"] is not None else None,
    )
    time.sleep(1)
    await load_emojis(guild=guild, server_backup=server_backup)
    await load_roles(guild=guild, server_backup=server_backup)
    await load_categories(guild=guild, server_backup=server_backup)
    time.sleep(1)
    try:
        system_channel_flags = None
        if server_backup["system_channel_flags"] is not None:
            value = int(
                server_backup["system_channel_flags"].replace("<SystemChannelFlags value=", "").replace(">", ""))
            if value == 1:
                system_channel_flags = discord.SystemChannelFlags(1)
            elif value == 2:
                system_channel_flags = discord.SystemChannelFlags(2)
            elif value == 4:
                system_channel_flags = discord.SystemChannelFlags(4)
            elif value == 8:
                system_channel_flags = discord.SystemChannelFlags(8)
            else:
                system_channel_flags = None
        await guild.edit(
            afk_channel=discord.utils.get(guild.channels, name=server_backup["afk_channel"]) if server_backup[
                                                                                                    "afk_channel"] is not None else None,
            system_channel=discord.utils.get(guild.channels, name=server_backup["system_channel"]) if server_backup[
                                                                                                          "system_channel"] is not None else None,
            rules_channel=discord.utils.get(guild.channels, name=server_backup["rules_channel"]) if server_backup[
                                                                                                        "rules_channel"] is not None else None,
            public_updates_channel=discord.utils.get(guild.channels, name=server_backup["public_updates_channel"]) if
            server_backup["public_updates_channel"] is not None else None
        )
        if system_channel_flags is not None:
            time.sleep(1)
            await guild.edit(
                system_channel_flags=system_channel_flags
            )
    except Exception:
        pass


@bot.event
async def on_ready():
    print("Online")


@bot.command()
async def backup(ctx):
    server_save_name = "servers/" + str(ctx.guild.id) + ".json"
    if os.path.exists(server_save_name):
        embed = discord.Embed(title="Already have backup", colour=discord.Colour.red())
        await ctx.reply(embed=embed)
        return
    start_time = time.time()
    await create_backup(ctx.guild)
    end_time = time.time()
    f = open(server_save_name, "a")
    with open(server_save_name, "w") as file:
        file.write(json.dumps(server_data, indent=4))
    embed = discord.Embed(title="Backup Saved", description=f"{round(end_time - start_time, 3)} seconds took",
                          colour=discord.Colour.green())
    await ctx.reply(embed=embed)


@bot.command()
async def load_backup(ctx, guild_id):
    if guild_id != "" and str(guild_id).isdigit():
        with open("servers/" + guild_id + ".json", "r") as file:
            server_backup = json.load(file)
        await load_backup_and_delete(guild=ctx.guild, server_backup=server_backup)
        print("Done")
    else:
        await ctx.reply("ID needed")


if __name__ == "__main__":
    bot.run("Bot token here")
