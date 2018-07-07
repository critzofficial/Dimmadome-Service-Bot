from discord.ext import commands
import discord
import asyncio
import sys
import traceback
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
        for ext in initial_extensions:
            bot.unload_extension(ext)
            bot.load_extension(ext)
        await ctx.send("Bot successfully restarted the extensions.")
    except Exception as err:
        print(f'Failed to load extension {ext}. Reason: ``{err.__class__.__name__}: {err}``', file=sys.stderr)
        traceback.print_exc()


@bot.command(hidden=True)
@commands.is_owner()
async def loadext(ctx, ext):
    if fs.exists(ext + ".py"):
        try:
            bot.load_extension(ext)
            await ctx.send(f"Extension {ext} successfully loaded.")
        except Exception as err:
            await ctx.send(f"Extension {ext} failed to load. Reason: ``{err.__class__.__name__}: {err}``")
    else:
        await ctx.send(f"Extension {ext} invalid.")


@bot.command(hidden=True)
@commands.is_owner()
async def unloadext(ctx, ext):
    if fs.exists(ext + ".py"):
        try:
            bot.unload_extension(ext)
            await ctx.send(f"Extension {ext} successfully unloaded.")
        except Exception as err:
            await ctx.send(f"Extension {ext} failed to unload. Reason: ``{err.__class__.__name__}: {err}``")
    else:
        await ctx.send(f"Extension {ext} invalid.")


@bot.command(hidden=True)
@commands.is_owner()
async def reloadext(ctx, ext):
    if fs.exists(ext + ".py"):
        try:
            bot.unload_extension(ext)
            bot.load_extension(ext)
            await ctx.send(f"Extension {ext} successfully reloaded.")
        except Exception as err:
            await ctx.send(f"Extension {ext} failed to reload. Reason: ``{err.__class__.__name__}: {err}``")
    else:
        await ctx.send(f"Extension {ext} invalid.")


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
