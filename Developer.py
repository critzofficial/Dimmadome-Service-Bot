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

    #Ultimate Test Command
    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        dict1 = {"apples": 2, "pears": 10}
        dict1.setdefault("pineapples", 5)
        await say(ctx, str(dict1["pineapples"]))
        await say(ctx, str(dict1))

    #Flexible Rules Command
    @commands.command()
    @commands.is_owner()
    async def rules(self, ctx):
        embed_rules = discord.Embed(title="Los Santos Gaming Discord Rules", description="These are the rules for the Discord server of LsG, break them at your own risk.", color=random.randint(0, 16777215))
        embed_rules.add_field(name="#1 - General Respect", value="We expect all users to respect each other, especially to respect the staff team. If you have a problem with any user, don't pour oil into the flames - call an admin to solve the problem! However, if you see an admin abusing his powers, contact one of the Upper Administrators or <@351077471241764876> .")
        embed_rules.add_field(name="#2 - No advertising", value="Advertising any kind of servers is strictly prohibited! If you want to show off your work, you have to ask an admin for permission to post it (in case of it's a link).")
        embed_rules.add_field(name="#3 - No excessive cursing", value="We understand that people have to vent every now and then or that they can simply have a bad day, but consequent cursing will lead to punishments. Watch your tongue!")
        embed_rules.add_field(name="#4 - No racism", value="Racism is not tolerated at all, even as a joke. Any racist acts will be dealt with instant bans and any spottings should be reported to the staff team immediately.")
        embed_rules.add_field(name="#5 - Be gone spam!", value="Spamming is not tolerated inside of this server. If you want to say something that is longer, write in larger segments. Don't make every word one message!")
        embed_rules.add_field(name="#6 - Keep channels in the topic field", value="Don't try to go off-topic inside of the wrong channel, keep everything where it belongs!")
        embed_rules.set_footer(text="Embed coded and called by CritZ")
        await esay(ctx, embed_rules)
        embed_grules = discord.Embed(title="Log Santos Gaming In-game Rules", description="These are the rules for the GTA San Andreas server of LsG, break them at your own risk.", color=random.randint(0, 16777215))
        embed_grules.add_field(name="#1 - No mods/hacks", value="Usage of any kind of mods that alter other players' gaming experience is strictly prohibited, unless approved by one of the higher staff members.")
        embed_grules.add_field(name="#2 - No deathmatching", value="Deathmatching (randomly killing) other players or ramming, car parking, AFK killing etc. is prohibited.")
        embed_grules.add_field(name="#3 - 5 minute cooldown after death", value="If you die in Roleplay, you have to wait approximately 5 minutes before you can return to the person that killed you.")
        embed_grules.add_field(name="#4 - No command abusement", value="Any kind of command abusement (especially in RP situations) is strictly prohibited and frowned upon!")
        embed_grules.add_field(name="#5 - No insulting", value="Insulting any other players is against the rules, even as a joke!")
        embed_grules.add_field(name="#6 - More 'be gone spam'!", value="Spamming in-game or calling out the same player is against the rules.")
        embed_grules.add_field(name="#7 - **EARN** your adminship", value="If you want to become an admin, don't keep annoying other staff members - apply instead!")
        embed_grules.set_footer(text="Embed coded and called by CritZ")
        await esay(ctx, embed_grules)


def setup(bot):
    bot.add_cog(Developer(bot))
