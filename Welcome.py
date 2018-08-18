from discord.ext import commands
import discord
import json


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)


class Welcome:
    """This category is all about the welcome/leave commands designed for the bot. All commands can only get executed by the administrators.

    This category also supports special 'decorators' to make your messages even fancier!

    They are:
    {USERNAME} - The plain display name of the user.
    {USERID} - The user's unique ID.
    {MENTION} - Mentions the user. This is only available in the welcome variant!
    {SRVNAME} - The name of the server.
    {SRVID} - The server's unique ID.
    {SRVCOUNT} - The amount of members in the server."""

    def __init__(self, bot):
        self.bot = bot

    ##----EVENT ON MEMBER JOIN----##
    async def on_member_join(self, member):
        with open("../DSB_Files/welcome.json") as file:
            weldict = json.load(file)
        if str(member.guild.id) in weldict:
            if member.guild.id == 475902932190101504:
                role = discord.utils.get(member.guild.roles, id=475931350491332618)
                await member.add_roles(role, reason="Member joined us!")
            channelID = int(weldict[str(member.guild.id)]["chID"])
            channel = self.bot.get_channel(channelID)
            msg = weldict[str(member.guild.id)]["msg"]
            if "{USERNAME}" in msg:
                msg = msg.replace("{USERNAME}", member.display_name)
            if "{USERID}" in msg:
                msg = msg.replace("{USERID}", str(member.id))
            if "{MENTION}" in msg:
                msg = msg.replace("{MENTION}", f"<@{member.id}>")
            if "{SRVNAME}" in msg:
                msg = msg.replace("{SRVNAME}", member.guild.name)
            if "{SRVID}" in msg:
                msg = msg.replace("{SRVID}", str(member.guild.id))
            if "{SRVCOUNT}" in msg:
                msg = msg.replace("{SRVCOUNT}", str(len(member.guild.members)))
            embed_welcome = discord.Embed(title=f"Welcome to {member.guild.name}!", description=msg, color=0x00FF00)
            embed_welcome.set_image(url=member.avatar_url)
            embed_welcome.set_footer(text=f"You are our member #{len(member.guild.members)} !")
            await channel.send(embed=embed_welcome)

    ##----EVENT ON MEMBER LEAVE----##
    async def on_member_remove(self, member):
        with open("../DSB_Files/leave.json") as file:
            leavedict = json.load(file)
        if str(member.guild.id) in leavedict:
            channelID = int(leavedict[str(member.guild.id)]["chID"])
            channel = self.bot.get_channel(channelID)
            msg = leavedict[str(member.guild.id)]["msg"]
            if "{USERNAME}" in msg:
                msg = msg.replace("{USERNAME}", member.display_name)
            if "{USERID}" in msg:
                msg = msg.replace("{USERID}", str(member.id))
            if "{SRVNAME}" in msg:
                msg = msg.replace("{SRVNAME}", member.guild.name)
            if "{SRVID}" in msg:
                msg = msg.replace("{SRVID}", str(member.guild.id))
            if "{SRVCOUNT}" in msg:
                msg = msg.replace("{SRVCOUNT}", str(len(member.guild.members)))
            embed_leave = discord.Embed(title=f"{member.name} just left us...", description=msg, color=0xFF8800)
            embed_leave.set_image(url=member.avatar_url)
            embed_leave.set_footer(text=f"We are left with {len(member.guild.members)} members.")
            await channel.send(embed=embed_leave)

    #---~WELCOME~---#
    @commands.group()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        """This is the parent command of the welcome commands. Channel and text are only required for setting.

        Permissions:
          Administrator"""
        pass

    #--SETW--#
    @welcome.command()
    async def setw(self, ctx, channel: discord.TextChannel, *, message: str):
        """Sets the welcome channel and message!

        Whenever a new user joins, bot or not, a message will be sent, when this is defined.

        Parameters:
          channel - The channel to use. The channel can be mentioned, named or ID'd.
          message - The message to use. Please avoid using emojis, as they don't get saved properly!"""
        with open("../DSB_Files/welcome.json", "r") as filetoread:
            srvdict = json.load(filetoread)
        srvdict[str(ctx.guild.id)] = {"chID": str(channel.id), "msg": str(message)}
        with open("../DSB_Files/welcome.json", "w") as filetowrite:
            json.dump(srvdict, filetowrite)
        await say(ctx, ":white_check_mark: - Welcome message and channel set!")

    #--TESTW--#
    @welcome.command()
    async def testw(self, ctx):
        """Tests the welcome channel and message!

        The bot must have access to send in the specific channel at *all* times."""
        with open("../DSB_Files/welcome.json", "r") as filetoread:
            srvdict = json.load(filetoread)
        if not str(ctx.guild.id) in srvdict:
            await say(ctx, ":interrobang: - Your server has no welcome settings defined!")
        else:
            channelID = int(srvdict[str(ctx.guild.id)]["chID"])
            channel = self.bot.get_channel(channelID)
            msg = srvdict[str(ctx.guild.id)]["msg"]
            if "{USERNAME}" in msg:
                msg = msg.replace("{USERNAME}", ctx.author.display_name)
            if "{USERID}" in msg:
                msg = msg.replace("{USERID}", str(ctx.author.id))
            if "{MENTION}" in msg:
                msg = msg.replace("{MENTION}", f"<@{ctx.author.id}>")
            if "{SRVNAME}" in msg:
                msg = msg.replace("{SRVNAME}", ctx.guild.name)
            if "{SRVID}" in msg:
                msg = msg.replace("{SRVID}", str(ctx.guild.id))
            if "{SRVCOUNT}" in msg:
                msg = msg.replace("{SRVCOUNT}", str(len(ctx.guild.members)))
            embed_welcome = discord.Embed(title=f"Welcome to {ctx.guild.name}!", description=msg, color=0x00FF00)
            embed_welcome.set_image(url=ctx.author.avatar_url)
            embed_welcome.set_footer(text=f"You are our member #{len(ctx.guild.members)} !")
            await channel.send(embed=embed_welcome)

    #--DELETEW--#
    @welcome.command()
    async def deletew(self, ctx):
        """Deletes the welcome settings for this guild.

        Both channel and message will get deleted."""
        with open("../DSB_Files/welcome.json", "r") as filetoread:
            srvdict = json.load(filetoread)
        if not str(ctx.guild.id) in srvdict:
            await say(ctx, ":interrobang: - Your server has no welcome settings defined!")
        else:
            del srvdict[str(ctx.guild.id)]
            with open("../DSB_Files/welcome.json", "w") as filetowrite:
                json.dump(srvdict, filetowrite)
            await say(ctx, ":white_check_mark: - Welcome settings deleted!")

    #---~LEAVE~---#
    @commands.group()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        """This is the parent command of the leave commands. Channel and text are only required for setting.

        Permissions:
          Administrator"""

    #--SETL--#
    @leave.command()
    async def setl(self, ctx, channel: discord.TextChannel, *, message: str):
        """Sets the leave channel and message!

        Whenever an user leaves, bot or not, a message will be sent, when this is defined.

        Parameters:
          channel - The channel to use. The channel can be mentioned, named or ID'd.
          message - The message to use. Please avoid using emojis, as they don't get saved properly!"""
        with open("../DSB_Files/leave.json", "r") as filetoread:
            srvdict = json.load(filetoread)
        srvdict[str(ctx.guild.id)] = {"chID": str(channel.id), "msg": str(message)}
        with open("../DSB_Files/leave.json", "w") as filetowrite:
            json.dump(srvdict, filetowrite)
        await say(ctx, ":white_check_mark: - Leave message and channel set!")

    #--TESTL--#
    @leave.command()
    async def testl(self, ctx):
        """Tests the leave channel and message!

        The bot must have access to send in the specific channel at *all* times."""
        with open("../DSB_Files/leave.json", "r") as filetoread:
            srvdict = json.load(filetoread)
        if not str(ctx.guild.id) in srvdict:
            await say(ctx, ":interrobang: - Your server has no leave settings defined!")
        else:
            channelID = int(srvdict[str(ctx.guild.id)]["chID"])
            channel = self.bot.get_channel(channelID)
            msg = srvdict[str(ctx.guild.id)]["msg"]
            if "{USERNAME}" in msg:
                msg = msg.replace("{USERNAME}", ctx.author.display_name)
            if "{USERID}" in msg:
                msg = msg.replace("{USERID}", str(ctx.author.id))
            if "{SRVNAME}" in msg:
                msg = msg.replace("{SRVNAME}", ctx.guild.name)
            if "{SRVID}" in msg:
                msg = msg.replace("{SRVID}", str(ctx.guild.id))
            if "{SRVCOUNT}" in msg:
                msg = msg.replace("{SRVCOUNT}", str(len(ctx.guild.members)))
            embed_leave = discord.Embed(title=f"{ctx.author.name} just left us...", description=msg, color=0xFF8800)
            embed_leave.set_image(url=ctx.author.avatar_url)
            embed_leave.set_footer(text=f"We are left with {len(ctx.guild.members)} members.")
            await channel.send(embed=embed_leave)

    #--DELETEL--#
    @leave.command()
    async def deletel(self, ctx):
        """Deletes the leave settings for this guild.

        Both channel and message will get deleted."""
        with open("../DSB_Files/leave.json", "r") as filetoread:
            srvdict = json.load(filetoread)
        if not str(ctx.guild.id) in srvdict:
            await say(ctx, ":interrobang: - Your server has no welcome settings defined!")
        else:
            del srvdict[str(ctx.guild.id)]
            with open("../DSB_Files/leave.json", "w") as filetowrite:
                json.dump(srvdict, filetowrite)
            await say(ctx, ":white_check_mark: - Leave settings deleted!")


def setup(bot):
    bot.add_cog(Welcome(bot))
