from discord.ext import commands
import discord

ownerID = 255802794244571136

class Admin:

    def __init__(self, bot):
        self.bot = bot

    #---DISMISS---#
    @commands.command(description="Makes the bot leave the server.\nRequired permissions: administrator")
    async def dismiss(self, ctx):
        """Make me leave. :["""
        if ctx.author.guild_permissions.administrator:
            await ctx.guild.leave()

def setup(bot):
    bot.add_cog(Admin(bot))