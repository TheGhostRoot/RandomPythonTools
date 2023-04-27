import discord
from discord.ext import commands, tasks
from discord.ui import View
import asyncio
import random

bot = commands.Bot(command_prefix='drunkme.', intents=discord.Intents.all())

# user_id : {"drinks": ['vodka', 'bira', ..], "drunk_time": 120}
user_data = dict()

# user_id : [Channel_id1, channel_id2]
unseen_channels = dict()

SERVER_ID = 1097933447546294483

# "beer": 1, "vodka": 3, "vine": 5, "viski": 4, "rakiq": 2, "djin": 6, "tekila": 2, "uzo": 1, "rum": 7, "likior": 4, "martini": 3, "ciganche": 10, "baileys": 4
# "limits": {server_id: 150, server_id: 200, ...}
drinks = {"beer": 2, "vodka": 3, "vine": 5, "viski": 4, "rakiq": 4, "djin": 6, "tekila": 2, "uzo": 1, "rum": 7,
          "likior": 4, "martini": 3, "ciganche": 10, "baileys": 4, "limits": {}}


# 🍹  🧉  🥤  🍷  🍸  🍺  🧃  🥂  🍾  🍻


@tasks.loop(seconds=2)
async def make_them_drunk():
    global user_data
    global unseen_channels
    channels_to_unsee = []
    for user_id, user_info in user_data.items():
        unseen_channels[user_id] = []
        server = discord.utils.get(bot.guilds, id=SERVER_ID)
        if server:
            user = discord.utils.get(server.members, id=user_id)
            if user:
                if user_data[user_id]["drunk_time"] == 0:
                    user_data[user_id]['drinks'].clear()
                    for c in server.channels:
                        await c.set_permissions(target=user, overwrite=discord.PermissionOverwrite(view_channel=True))
                elif user_info["drunk_time"] > 39 or user_info["drunk_time"] < 39:
                    print(user.name, 'is now drunk')
                    channels_in = [1]
                    while len(channels_in) > 0:
                        channels_to_unsee = random.choices(server.channels, k=int(len(server.channels) * (1 / 3)))
                        channels_in = [c for c in channels_to_unsee if c in unseen_channels[user.id]]
                    for channel1 in channels_to_unsee:
                        try:
                            await channel1.set_permissions(target=user,
                                                           overwrite=discord.PermissionOverwrite(view_channel=False))
                        except Exception:
                            continue
                        else:
                            unseen_channels[user.id].append(channel1.id)
                            await asyncio.sleep(1)
                    if len(unseen_channels[user.id]) > 0:
                        channels_to_see = random.choices(unseen_channels[user.id],
                                                         k=int(len(server.channels) * (1 / 2)))
                        for c1 in channels_to_see:
                            chann = discord.utils.get(server.channels, id=c1)
                            if chann:
                                try:
                                    await chann.set_permissions(target=user, overwrite=discord.PermissionOverwrite(
                                        view_channel=True))
                                except Exception:
                                    continue
                                if c1 in unseen_channels[user.id]:
                                    unseen_channels[user.id].remove(c1)
                                await asyncio.sleep(1)

                user_data[user_id]["drunk_time"] = user_data[user_id]["drunk_time"] - 1
                print(user_data[user_id]["drunk_time"])


def update_drink(user_id):
    global user_data
    user_data[user_id]["drunk_time"] = sum([drinks[drink] for drink in user_data[user_id]['drinks']])


class ChooseDrink(View):
    global user_data

    def __init__(self):
        super().__init__(timeout=None)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = False

    # button: discord.Button, interaction
    # interaction, button: discord.Button
    @discord.ui.button(label='Beer', style=discord.ButtonStyle.primary)
    async def beer_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Beer")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("beer")
        update_drink(member_id)

    @discord.ui.button(label='Vodka', style=discord.ButtonStyle.primary)
    async def vodka_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Vodka")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("vodka")
        update_drink(member_id)

    @discord.ui.button(label='Vine', style=discord.ButtonStyle.primary)
    async def vine_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Vine")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("vine")
        update_drink(member_id)

    @discord.ui.button(label='Viski', style=discord.ButtonStyle.primary)
    async def viski_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Viski")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("viski")
        update_drink(member_id)

    @discord.ui.button(label='Rakiq', style=discord.ButtonStyle.primary)
    async def rakiq_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Rakiq")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("rakiq")
        update_drink(member_id)

    @discord.ui.button(label='Djin', style=discord.ButtonStyle.primary)
    async def djin_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Djin")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("djin")
        update_drink(member_id)

    @discord.ui.button(label='Tekila', style=discord.ButtonStyle.primary)
    async def tekila_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Tekila")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("tekila")
        update_drink(member_id)

    @discord.ui.button(label='Uzo', style=discord.ButtonStyle.primary)
    async def uzo_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Uzo")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("uzo")
        update_drink(member_id)

    @discord.ui.button(label='Rum', style=discord.ButtonStyle.primary)
    async def rum_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Rum")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("rum")
        update_drink(member_id)

    @discord.ui.button(label='Likior', style=discord.ButtonStyle.primary)
    async def likior_button(self, interaction, button: discord.Button):
        await interaction.channel.send("Likior drink")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("likior")
        update_drink(member_id)

    @discord.ui.button(label='Martini', style=discord.ButtonStyle.primary)
    async def martini_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Martini")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("martini")
        update_drink(member_id)

    @discord.ui.button(label='Ciganche', style=discord.ButtonStyle.primary)
    async def ciganche_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Ciganche")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("ciganche")
        update_drink(member_id)

    @discord.ui.button(label='Baileys', style=discord.ButtonStyle.primary)
    async def vodka_button(self, interaction, button: discord.Button):
        await interaction.channel.send(f"{interaction.user.mention} drank Baileys")
        member_id = interaction.user.id
        if member_id not in user_data.keys():
            user_data[member_id] = {'drinks': [], "drunk_time": 0}
        user_data[member_id]['drinks'].append("baileys")
        update_drink(member_id)

    @discord.ui.button(label='Secret', style=discord.ButtonStyle.primary)
    async def secret_button(self, interaction, button: discord.Button):
        # 823947753917906945 - ti
        # 951513329107619850 - ivak
        if interaction.user.id == 951513329107619850:
            await interaction.user.send(
                "Te amo, mi osito <3 https://tenor.com/view/hugs-sending-virtual-hugs-loading-gif-8158818")


@bot.command()
async def menu(ctx):
    DrinksMenu = discord.Embed(colour=discord.Colour.red())
    DrinksMenu.set_author(name="🍷 Drinks on me!")
    for drink_name, num in drinks.items():
        if drink_name != 'limits':
            DrinksMenu.add_field(name="🍹 | " + drink_name, value=str(num))
    DrinksMenu.set_footer(text="By rooty and Adi")
    await ctx.reply(embed=DrinksMenu, view=ChooseDrink())


@bot.event
async def on_ready():
    global drinks
    server = discord.utils.get(bot.guilds, id=SERVER_ID)
    if server:
        for c in server.channels:
            for u in server.members:
                await c.set_permissions(target=u, overwrite=discord.PermissionOverwrite(view_channel=True))
    make_them_drunk.start()
    print('Bot online', bot.user.name)


if __name__ == "__main__":
    bot.run("OTYzMTA5ODM0NjE2NjE0OTEy.GMpPFY.CLDTUXfeSdi0dRrVWXkwITobWw6U8Nl-0WwOTk")

