from discord.ext import commands
import discord
import json
import random


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)


ownerID = 255802794244571136


class Economy:
    """This module is about the 'economy' system of DummyBot, where you can earn virtual money, spend it and have fun with your purchased items!

    (This module is relatively new, so be gentle with the commands!)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, *, user: discord.Member = None):
        """Check the balance of someone!

        This command can only check the balance of a member on the current server. Balances accross servers are separated.

        Parameters:
          user - The user to check. This parameter is optional and defaults to the user that sends the message."""
        if user == None:
            user = ctx.author
        else:
            pass
        with open("../DSB_Files/economy.json", "r") as file:
            economydict = json.load(file)
        try:
            curbalance = economydict[str(ctx.guild.id)][str(user.id)]["balance"]
            await esay(ctx, discord.Embed(title=f"Balance of {user.name}", description=f"The current balance of {user.name} is {curbalance}$!", color=0x00FF00))
        except KeyError:
            await say(ctx, f":interrobang: - Whoops, it seems like {user.name} doesn't have a balance currently! Did they try getting any income yet?")

    @commands.command()
    async def work(self, ctx):
        """Work to earn some money!

        *PLEASE NOTICE!* The command currently has no cooldown, but will have one in the future. All balances will be reset once the economy system has been finished."""
        with open("../DSB_Files/economy.json", "r") as filetoread:
            economydict = json.load(filetoread)
        guild_balances = economydict.setdefault(str(ctx.guild.id), {})
        curuser = guild_balances.get(str(ctx.author.id), {"balance": 0})
        curbalance = curuser.get("balance")
        income = random.randrange(20000, 100000) / 100
        newbalance = round(curbalance + income, 2)
        try:
            guild_balances[str(ctx.author.id)]["balance"] = newbalance
        except KeyError:
            guild_balances[str(ctx.author.id)] = {"balance": newbalance}
        with open("../DSB_Files/economy.json", "w") as filetowrite:
            json.dump(economydict, filetowrite)
        await esay(ctx, discord.Embed(title="Work Income", description=f"You worked and worked until you earned yourself {income}$. Your new balance is {newbalance}$.", color=0x00FF00))

    @commands.command()
    async def setmoney(self, ctx, user: discord.Member, *, money: int):
        """Set the money of an user!

        Parameters:
          user - The user to set the money to. If nicknames/usernames will be used (that contain whitespaces), quote them.
          money - The amount to set. If decimal, it will be rounded down to 2 decimals."""
        with open("../DSB_Files/economy.json", "r") as filetoread:
            economydict = json.load(filetoread)
        money = round(money, 2)
        try:
            economydict[str(ctx.guild.id)][str(user.id)]["balance"] = money
        except KeyError:
            economydict[str(ctx.guild.id)] = {str(user.id): {"balance": money}}
        with open("../DSB_Files/economy.json", "w") as filetowrite:
            json.dump(economydict, filetowrite)
        await esay(ctx, discord.Embed(title="Money Set", description=f"The money for {user.name} has been set to {money}$!", color=0x00FF00))

    @commands.command()
    async def rob(self, ctx, user: discord.Member):
        """Attempt to rob someone!

        If you succeed, you will gain a random amount out of their balance, starting from 20%. If you fail, you will have to pay up to 50% of your own balance.

        If the user you're robbing has no cash, the command will not work. If the half of your balance is below 500$, you will be charged 500$ (in case of failure).

        Parameters:
          user - The user to rob."""
        user_is_robbable = True
        with open("../DSB_Files/economy.json", "r") as filetoread:
            economydict = json.load(filetoread)
        your_fate = random.randint(0, 100)
        if your_fate < 50:
            #You got caught!
            try:
                bal1 = economydict[str(ctx.guild.id)][str(ctx.author.id)]["balance"]
                bal1maxpay = bal1 / 2
                if bal1maxpay >= 500:
                    fee = random.uniform(0, bal1maxpay)
                else:
                    fee = 500
                bal2 = bal1 - fee
            except KeyError:
                economydict[str(ctx.guild.id)] = {str(ctx.author.id): {"balance": -500}}
                bal2 = economydict[str(ctx.guild.id)][str(ctx.author.id)]["balance"]
                fee = 500
            await esay(ctx, discord.Embed(title=":outbox_tray: - Whoops, that went wrong!", description=f"You got caught while attempting to rob {user.name} and have been charged a fee of {fee}$! Your current balance is {bal2}$."))
        elif your_fate >= 50:
            #You succeeded!
            try:
                userbal = economydict[str(ctx.guild.id)][str(user.id)]["balance"]
                userbalmin = userbal / 5
                if userbal > 0:
                    gain = round(random.uniform(userbalmin, userbal), 2)
                else:
                    user_is_robbable = False
            except KeyError:
                user_is_robbable = False
            if user_is_robbable:
                try:
                    authorbalbef = economydict[str(ctx.guild.id)][str(ctx.author.id)]["balance"]
                    economydict[str(ctx.guild.id)][str(ctx.author.id)]["balance"] = authorbalbef + gain
                    authorbalaft = economydict[str(ctx.guild.id)][str(ctx.author.id)]["balance"]
                except KeyError:
                    economydict[str(ctx.guild.id)][str(ctx.author.id)]["balance"]


def setup(bot):
    bot.add_cog(Economy(bot))
