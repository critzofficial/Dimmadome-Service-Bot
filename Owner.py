from discord.ext import commands
import discord
import textwrap


async def say(ctx, cont: str):
    return await ctx.send(cont)

ownerID = 255802794244571136


class Owner:
    """This category is all about the commands made specially for the owner of the bot, Dr. Heinz Doofenshmirtz. You can have a look, but you can also simply ignore them."""

    def __init__(self, bot):
        self.bot = bot

    #---EVAL---#
    @commands.command(aliases=["run", "exec"])
    @commands.is_owner()
    async def eval(self, ctx, *, body):
        """Run any quick command.

        Parameters:
            body - The code to execute.

        Requirements:
            Bot ownership"""
        to_exec = textwrap.indent(body, "  ")
        exec(f"async def func(ctx):\n\t{to_exec}", globals())
        await func(ctx)

    #---QUIT---#
    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        """Logs out of discord.

        Requirements:
            Bot ownership"""
        await say(ctx, "Shutting down...")
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))
