import os

try:
    import discord
    from discord.ext import commands
except ImportError:
    os.system("pip install discord.py")
    try:
        import discord
        from discord.ext import commands
    except:
        print("You need python 3.7.9")
        exit()


bot = commands.Bot(command_prefix="b.", self_bot=False, bot=True)
token = "token here


@bot.event
async def on_ready():
    print("The Bot is online.")
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="b.helpMe for the help menu"))


@bot.command()
async def helpMe(ctx):
    embed1 = discord.Embed(colour=discord.Colour.blue())
    embed1.set_author(name="Commands:")
    embed1.add_field(name=" b.play <word>", value="starts a game", inline=False)
    embed1.add_field(name=" b.stop", value="stops the game", inline=False)
    embed1.add_field(name=" b.guessWord <word>", value="to guess a word", inline=False)
    embed1.add_field(name=" b.guess <letter>", value="to guess a letter", inline=False)
    embed1.add_field(name="[!]", value="Warning", inline=False)
    embed1.add_field(name="Developer: ", value="🔥𝕣𝕠𝕠𝕥𝕪🔥#8465", inline=False)
    await ctx.send(embed=embed1)


"""
7 lives
"""

players = []
host = ""

word = ""
guessWord1 = ""
lives = []
alive = ":hearts:"


@bot.command()
async def play(ctx, Gword: str):
    global host
    global lives
    global players
    global word
    global guessWord1
    Gword = Gword.lower()
    if host == "":
        if Gword is not None and Gword != "":
            await ctx.message.delete()
            host = ctx.author
            word = Gword
            JustStr = ""
            i = 0
            while i < len(word):
                JustStr += "-"
                i += 1
            guessWord1 = JustStr
            lives = [":hearts:", ":hearts:", ":hearts:", ":hearts:", ":hearts:", ":hearts:",
                     ":hearts:"]
            await ctx.author.send(guessWord1)
            l = ""
            for live in lives:
                l += " " + live
            await ctx.send(l)
            await ctx.send("**Host** >> " + str(host))
        else:
            await ctx.send("**[!]**You have to give a word and the message will be deleted.")
    else:
        await ctx.send("**[!]**Finish this game.")


@bot.command()
async def stop(ctx):
    global host
    global lives
    global players
    global word
    global guessWord1
    if ctx.author == host:
        host = ""
        lives.clear()
        players.clear()
        word = ""
        guessWord1 = ""
        await ctx.send("The game just stopped.")
    else:
        await ctx.send("**[!]**You need to be the host of the game.")


@bot.command()
async def guess(ctx, letter: str):
    global host
    global players
    global lives
    global word
    global guessWord1
    letter = letter.lower()
    if ctx.author == host:
        await ctx.send("**[!]**You cant be a guesser!")
    else:
        if word == "":
            await ctx.send("**[!]**There is no game started.")
        else:
            if letter is None or letter == "":
                await ctx.send("**[!]**You have to give a letter you think it could be in the word.")
            else:
                if ctx.author not in players:
                    players.append(ctx.author)
                if letter in guessWord1:
                    await ctx.send("**[!]** **" + letter + "** is already guessed.")
                else:
                    if letter in word:
                        # New letter found

                        # pypi
                        # p-p-
                        # -i--
                        # ---y

                        numOfLetters = 0
                        for char in word:
                            if char == letter:
                                numOfLetters += 1

                        if numOfLetters > 0:
                            # -------
                            # p
                            # p------
                            # t
                            # p--t---
                            newGuessWord = ""
                            if numOfLetters == 1:
                                index = word.index(letter)
                                indexNow = 0
                                for char in guessWord1:
                                    if indexNow == index:
                                        newGuessWord += letter
                                    else:
                                        newGuessWord += char
                                    indexNow += 1
                            if numOfLetters > 1:
                                lotIndex = []
                                index2 = -1
                                for letters in word:
                                    if letters == letter:
                                        index2 += 1
                                        lotIndex.append(index2)
                                indexNow = -1
                                for char in guessWord1:
                                    if indexNow in lotIndex:
                                        newGuessWord += letter
                                    else:
                                        newGuessWord += char
                                    indexNow += 1
                            guessWord1 = newGuessWord
                            l = ""
                            for live in lives:
                                l += " " + live
                            await ctx.send(guessWord1)
                            if guessWord1 == word:
                                await ctx.send("<@"+str(ctx.author.id)+"> **IS** the **WINNER**")
                                await ctx.send("**Host** >> " + str(host))
                                for player in players:
                                    await ctx.send("**Guesser** >> " + str(player))
                                host = ""
                                lives.clear()
                                players.clear()
                                word = ""
                                guessWord1 = ""
                            else:
                                await ctx.send(l)
                                await ctx.send("There IS **" + letter + "** in the word.")
                                await ctx.send("**Host** >> " + str(host))
                                for player in players:
                                    await ctx.send("**Guesser** >> " + str(player))
                    else:
                        # This letter is not in the word
                        # remove one live
                        if len(lives) == 1 or len(lives) == 0:
                            await ctx.send(host+" **IS** the **WINNER**")
                            for player in players:
                                await ctx.send("**Guesser** >> " + str(player))
                            host = ""
                            lives.clear()
                            players.clear()
                            word = ""
                            guessWord1 = ""
                        else:
                            lives.pop(0)
                            l = ""
                            for live in lives:
                                l += " " + live
                            await ctx.send(guessWord1)
                            await ctx.send(l)
                            await ctx.send("There is NO **" + letter + "** in the word.")
                            await ctx.send("**Host** >> " + str(host))
                            for player in players:
                                await ctx.send("**Guesser** >> " + str(player))


@bot.command()
async def guessWord(ctx, wordG: str):
    global word
    global guessWord1
    global players
    global lives
    global alive
    global host
    wordG = wordG.lower()
    if ctx.author == host:
        await ctx.send("**[!]**You cant be a guesser!")
    else:
        if word is None:
            await ctx.send("**[!]**There is no game started.")
        else:
            if wordG is None or word == "":
                await ctx.send("**[!]**You have to give a word you think it is.")
            else:
                if ctx.author not in players:
                    players.append(ctx.author)
                if word == wordG:
                    # the guesser wins
                    host = None
                    lives.clear()
                    players.clear()
                    word = None
                    guessWord1 = None
                    await ctx.send("That is **CORRECT**!")
                    await ctx.send(str(ctx.author) + " is the winner!")
                    await ctx.author.send(str(ctx.author) + " just guessed the word!")
                else:
                    livesLeft = 0
                    for live in lives:
                        if live == alive:
                            livesLeft += 1
                    if livesLeft == 1 or livesLeft == 0:
                        # the guessers lose
                        host = None
                        lives.clear()
                        players.clear()
                        word = None
                        guessWord1 = None
                        await ctx.send("You ran out of lives! Your game just finished.")
                        await ctx.send("The **HOST** is the **WINNER** > " + str(host))
                        await ctx.author.send("You just won the game!")
                        await ctx.author.send("**Word** > " + str(word))
                    else:
                        await ctx.send("Nine try, but that is **INCORRECT**! Sorry.")
                        lives.pop(0)
                        l = ""
                        for live in lives:
                            l += " " + live
                        await ctx.send(l)
                        await ctx.send("**Host** >> " + str(host))
                        for player in players:
                            await ctx.send("**Guesser** >> " + str(player))


try:
    bot.run(token)
except:
    print("The bot can't staty or the token is invalid")
