from discord.ext import commands
import discord
import textwrap
import traceback

ownerID = 255802794244571136

class Owner:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, body):
        to_exec = textwrap.indent(body, "  ")
        try:
            exec(f"async def func(ctx):\n\t{to_exec}", globals())
            await func(ctx)
        except Exception as e:
            await ctx.send(f"```{e.__class__.__name__}: {e}```")
            traceback.print_exc()

    #---QUIT---#
    @commands.command(description="Logs the bot out of discord.\nRequired permissions: Bot ownership")
    @commands.is_owner()
    async def quit(self, ctx):
        """Logs out of discord."""
        await ctx.send("Shutting down...")
        await self.bot.logout()

    #---OSAY---#
    @commands.command(description="Repeats word after word.\nRequired permissions: Bot ownership")
    @commands.is_owner()
    async def osay(self, ctx, *, msg):
        """Say something."""
        await ctx.send(msg)

    #---OPM---#
    @commands.command()
    @commands.is_owner()
    async def opm(self, ctx, mention: discord.Member=None, *, msg):
        """Make the bot PM someone."""
        if mention == None:
            await ctx.send("You didn't mention anyone!")
        else:
            await mention.send(msg)

def setup(bot):
    bot.add_cog(Owner(bot))