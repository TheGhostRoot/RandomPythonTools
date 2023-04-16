import os
import random

try:
    import discord
    from discord.ext import commands
except ImportError:
    os.system("pip install discord.py")
    try:
        import discord
        from discord.ext import commands
    except ImportError:
        print("You need python 3.7.9")
        exit()

turnSP = ""
playerAI = ""
winBot = False
winPlayer = False
isPlayerInSP = False
markBot = ":negative_squared_cross_mark:"
markPlayer = ":o2:"
countSP = 0

player1 = ""
player2 = ""
turn = ""
gameOver = True
gameOver1 = False

board = []
boardSP = []

bot = commands.Bot(command_prefix=".", self_bot=False, bot=True, intents=discord.Intents.all())

# random AI for singe player

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

token = "token here"


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@bot.event
async def on_ready():
    print(" The Bot is online!")
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name=".helpMe for the help menu"))


@bot.command()
async def helpMe(ctx):
    embed1 = discord.Embed(colour=discord.Colour.blue())
    embed1.set_author(name="Commands:")
    embed1.add_field(name=" .play @username", value="to start a game", inline=False)
    embed1.add_field(name=" .stop", value="stops the game", inline=False)
    embed1.add_field(name=" .place <number>", value="to place your marker", inline=False)
    await ctx.send(embed=embed1)


@bot.command()
async def stop(ctx):
    global gameOver
    global gameOver1
    global player1
    global player2
    global board
    global turn
    if gameOver:
        await ctx.send("**[!]** The game is already stopped.")
        return
    board.clear()
    board = [":one:", ":two:", ":three:",
             ":four:", ":five:", ":six:",
             ":seven:", ":eight:", ":nine:"]
    gameOver = True
    turn = ""
    gameOver1 = False
    player1 = ""
    player2 = ""
    await ctx.send("The game is stopped")


@bot.command()
async def play(ctx, p2: discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count
    global gameOver1
    global board

    if gameOver or gameOver1:

        if p2 == "":
            await ctx.send("**[!]** Sorry, but you have to give second player.")
            return
        if ctx.author == p2:
            await ctx.send("**[!]** Sorry, but you cant play vs yourself.")
            return
        line = ""
        turn = ""
        board = [":one:", ":two:", ":three:",
                 ":four:", ":five:", ":six:",
                 ":seven:", ":eight:", ":nine:"]
        gameOver = False
        gameOver1 = False
        count = 0

        player1 = ctx.author
        player2 = p2
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send(" It is <@" + str(player1.id) + ">'s turn.")
        if num == 2:
            turn = player2
            await ctx.send(" It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("**[!]** Finish the game before starting another one.")


@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver1
    global gameOver
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":negative_squared_cross_mark:"
            elif turn == player2:
                mark = ":o2:"

            if 0 < pos < 10:
                if board[pos - 1] == ":one:" or board[pos - 1] == ":two:" or board[pos - 1] == ":three:" or board[
                    pos - 1] == ":four:" or board[pos - 1] == ":five:" or board[pos - 1] == ":six:" or board[
                    pos - 1] == ":seven:" or board[pos - 1] == ":eight:" or board[pos - 1] == ":nine:":
                    board[pos - 1] = mark
                    count += 1

                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    if turn == player1:
                        turn = player2
                        if gameOver:
                            await ctx.send(mark + " wins!")
                            gameOver1 = True
                        elif count >= 9:
                            await ctx.send(" tie! :thumbsup:")
                            gameOver1 = True
                        else:
                            await ctx.send(" It is <@" + str(player2.id) + ">'s turn.")
                    elif turn == player2:
                        turn = player1
                        if gameOver:
                            await ctx.send(mark + " wins!")
                            gameOver1 = True
                        elif count >= 9:
                            await ctx.send(" tie! :thumbsup:")
                            gameOver1 = True
                        else:
                            await ctx.send(" It is <@" + str(player1.id) + ">'s turn.")
                else:
                    await ctx.send("**[!]** This position is already taken.")
            else:
                await ctx.send("**[!]** You have to choose an number between 1 and 9.")
        else:
            await ctx.send("**[!]** Wait for your turn.")
    else:
        await ctx.send("**[!]** You can start a game with command .play @username")


bot.run(token)
