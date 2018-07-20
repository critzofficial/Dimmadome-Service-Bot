from discord.ext import commands
import discord
import random


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)

ownerID = 255802794244571136


class Developer:
    """This module is about commands getting tested. Please don't use these, as the bot will be unstable with them until they work the way the bot owner wants them to."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, *, cont: str):
        await say(ctx, cont)

    @commands.command()
    @commands.is_owner()
    async def rules(self, ctx):
        embed_rules = discord.Embed(title="Lua Teaching Rules", description="These are the rules for Lua Teaching, break them at your own risk.", color=random.randint(0, 16777215))
        embed_rules.add_field(name="#1 - General Respect", value="We expect all users to respect each other, especially to respect the staff team. If you have a problem with any user, don't pour oil into the flames - call an admin to solve the problem! However, if you see an admin abusing his powers, contact one of the Owners.")
        embed_rules.add_field(name="#2 - No excessive cursing", value="We understand that people have to vent every now and then or that they can simply have a bad day, but consequent cursing will lead to punishments. Watch your tongue!")
        embed_rules.add_field(name="#3 - No racism", value="Racism is not tolerated at all, even as a joke. Any racist acts will be dealt with instant bans and any spottings should be reported to the staff team immediately.")
        embed_rules.add_field(name="#4 - No NSFW outside the NSFW channels", value="Remember that there are users under 18 using Discord, so keep any NSFW content (even memes) inside of the NSFW channel. Viewing the channel's content goes at your risk and we will not act for that. However, bestiality or animals mating are never allowed.")
        embed_rules.add_field(name="#5 - Keep channels in the topic field", value="Don't try to go off-topic inside of the wrong channel, keep everything where it belongs! This includes memes, too.")
        await esay(ctx, embed_rules)


def setup(bot):
    bot.add_cog(Developer(bot))
