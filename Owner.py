from discord.ext import commands
import discord
import textwrap
import random
import fs


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)

ownerID = 255802794244571136

verified_users = []


class Owner:
    """This category is all about the commands made specially for the owner of the bot, CritZ. You can have a look, but you can also simply ignore them."""

    def __init__(self, bot):
        self.bot = bot

    def is_verified(ctx):
        return ctx.author.id == ownerID or ctx.author.id in verified_users

    #---VERIFY---#
    @commands.command()
    async def verify(self, ctx, passcode):
        """Gain access to some of the owner-only commands!

        Parameters:
          passcode - The passcode. Every time an user is verified, a new one is generated."""
        with open("../DSB_Files/ultra_secret_passcode.txt", "r") as file:
            passkey = file.read()
        if passcode != passkey:
            await say(ctx, ":interrobang: - Passcodes do not match!")
        elif passcode == passkey:
            verified_users.append(ctx.author.id)
            list_keychars = []
            for i in range(20):
                list_choice = []
                x = random.randint(65, 90)
                list_choice.append(x)
                y = random.randint(97, 122)
                list_choice.append(y)
                z = random.randint(48, 57)
                list_choice.append(z)
                chooser = random.choice(list_choice)
                converted = chr(chooser)
                list_keychars.append(str(converted))
            passcode = "".join(list_keychars)
            print("The new password is: " + passcode)
            fs.write("../DSB_Files/ultra_secret_passcode.txt", passcode)
            await say(ctx, ":white_check_mark: - Successfully validated!")

    #---EVAL---#
    @commands.command(aliases=["run", "exec"])
    @commands.check(is_verified)
    #@commands.is_owner()
    async def eval(self, ctx, *, body):
        """Run any quick command.

        Parameters:
          body - The code to execute.

        Requirements:
          Bot ownership/Verification"""
        to_exec = textwrap.indent(body, "  ")
        exec(f"async def func(ctx):\n\t{to_exec}", globals())
        await func(ctx)

    #---QUIT---#
    @commands.command()
    @commands.check(is_verified)
    #@commands.is_owner()
    async def quit(self, ctx):
        """Logs out of discord.

        Requirements:
          Bot ownership/Verification"""
        await say(ctx, "Shutting down...")
        await self.bot.logout()

    #---QUICKUI---#
    @commands.command()
    @commands.check(is_verified)
    #@commands.is_owner()
    async def quickui(self, ctx, *, user: discord.User):
        """Shows some quick info about a special user.

        Parameters:
          user - The user to look for.

        Requirements:
          Bot ownership/Verification"""
        embed_qui = discord.Embed(title="Name", description=user.name)
        embed_qui.set_thumbnail(url=user.avatar_url)
        embed_qui.add_field(name="ID", value=user.id)
        embed_qui.add_field(name="Date of Account Creation", value=user.created_at.strftime("%A, %d. %B %Y %H:%M"))
        await esay(ctx, embed_qui)


def setup(bot):
    bot.add_cog(Owner(bot))
