from discord.ext import commands
import asyncio
import sys, traceback

bot = commands.Bot(command_prefix='DDT!')

initial_extensions = ["Utility", "Owner", "Admin"]

@bot.command(hidden=True)
@commands.is_owner()
async def loadext(ctx, extension):
    if extension in initial_extensions:
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
    if extension in initial_extensions:
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
    if extension in initial_extensions:
        try:
            bot.unload_extension(extension)
            bot.load_extension(extension)
            await ctx.send(f"Extension {extension} successfully restarted.")
        except Exception as e:
            await ctx.send(f"Extension {extension} failed to restart. Reason: ``{e.__class__.__name__}: {e}``")
    else:
        await ctx.send(f"Extension {extension} invalid.")

@bot.event
@asyncio.coroutine
async def on_ready():
    print("Ready to go!")

@bot.event
@asyncio.coroutine
async def on_command_error(ctx, error):
    await ctx.send(f":interrobang: Something went wrong with the command you used. An error has been raised!\nThe error is: {error}")

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}.', file=sys.stderr)
        traceback.print_exc()

with open("DEVTOKEN.txt", "r") as auth:
    bot.run(auth.read())