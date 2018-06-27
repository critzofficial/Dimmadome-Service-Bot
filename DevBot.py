from discord.ext import commands
import discord
import asyncio
import sys, traceback
import fs

description = """Welcome to the help section of Dimmadome Service Bot!

All I can really say here is that you should check each command category/usage before using anything. There are some twists that I can't change, unfortunately.

Also, note that this bot can be mentioned too to execute commands, however the bot is not allowed to have any nickname. Both the prefix and the mention work."""

bot = commands.Bot(command_prefix=["DD!", "<@269533424916627457> "], description=description)

initial_extensions = ["Utility", "Owner", "Admin", "Welcome"]


@bot.command(hidden=True)
@commands.is_owner()
async def restartbot(ctx):
    try:
        for extension in initial_extensions:
            bot.unload_extension(extension)
            bot.load_extension(extension)
        await ctx.send("Bot successfully restarted the extensions.")
    except Exception as e:
        print(f'Failed to load extension {extension}.', file=sys.stderr)
        traceback.print_exc()


@bot.command(hidden=True)
@commands.is_owner()
async def loadext(ctx, extension):
    if fs.exists(extension + ".py"):
        try:
            bot.load_extension(extension)
            await ctx.send(f"Extension {extension} successfully loaded.")
        except Exception as e:
            await ctx.send(f"Extension {extension} failed to load. Reason: ``{e.__class__.__name__}: {e}``")
    else:
        await ctx.send(f"Extension {extension} invalid.")


@bot.command(hidden=True)
@commands.is_owner()
async def unloadext(ctx, extension):
    if fs.exists(extension + ".py"):
        try:
            bot.unload_extension(extension)
            await ctx.send(f"Extension {extension} successfully unloaded.")
        except Exception as e:
            await ctx.send(f"Extension {extension} failed to unload. Reason: ``{e.__class__.__name__}: {e}``")
    else:
        await ctx.send(f"Extension {extension} invalid.")


@bot.command(hidden=True)
@commands.is_owner()
async def reloadext(ctx, extension):
    if fs.exists(extension + ".py"):
        try:
            bot.unload_extension(extension)
            bot.load_extension(extension)
            await ctx.send(f"Extension {extension} successfully reloaded.")
        except Exception as e:
            await ctx.send(f"Extension {extension} failed to reload. Reason: ``{e.__class__.__name__}: {e}``")
    else:
        await ctx.send(f"Extension {extension} invalid.")


@bot.event
@asyncio.coroutine
async def on_ready():
    print("Ready to go!")
    await bot.change_presence(activity=discord.Game(name="| DD!help |"))


@bot.event
@asyncio.coroutine
async def on_command_error(ctx, error):
    await ctx.send(
        f":interrobang: Something went wrong with the command you used. An error has been raised!\nThe error is: {error}")


for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}.', file=sys.stderr)
        traceback.print_exc()

with open("TOKEN.txt", "r") as auth:
    bot.run(auth.read())
