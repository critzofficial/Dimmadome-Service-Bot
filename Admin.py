from discord.ext import commands
import discord
import os
import fs
import json
import emoji

filternames1 = ["InviteFilter", "EmojiFilter"]
filternames2 = ["EmojiFilter"]

def extract_emojis(string):
    return ''.join(c for c in string if c in emoji.UNICODE_EMOJI)


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)


ownerID = 255802794244571136


class Admin:
    """This category is all about admin commands. Permissions are enlisted in the further description of each command."""

    def __init__(self, bot):
        self.bot = bot

    # -0-0-EVENTS-0-0-#
    async def on_message(self, message):
        # -0-INVFILTER-0-#
        if "discord.gg" in message.content or "discordapp.com/invite" in message.content:
            with open("../DSB_Files/filters.json", "r") as file:
                invfilter = json.load(file)
            try:
                invfilter = invfilter[str(message.guild.id)]["InviteFilter"]
            except KeyError:
                invfilter = False
            if invfilter:
                if not message.author.guild_permissions.manage_messages:
                    await message.delete()
                    await message.channel.send(
                        f":exclamation: - Please do not send invite links, {message.author.mention}!")
            elif not invfilter:
                pass
        # -0-EMOJIFILTER-0-#
        # TODO: Make the filter warn users when triggered.
        for c in emoji.UNICODE_EMOJI:
            if c in message.content:
                emjlimit = 0
                with open("../DSB_Files/filters.json", "r") as file:
                    emjfilter = json.load(file)
                try:
                    emjfilter = emjfilter[str(message.guild.id)]["EmojiFilter"]
                except KeyError:
                    emjfilter = False
                if emjfilter:
                    with open("../DSB_Files/emojis.json", "r") as filetoread:
                        emjdict = json.load(filetoread)
                    try:
                        emjlimit = emjdict[str(message.guild.id)]
                    except KeyError:
                        emjlimit = 5
                    finally:
                        emjcount = len(extract_emojis(message.content))
                        if emjcount >= emjlimit:
                            await message.delete()
                            await message.channel.send(f":exclamation: - Easy on the emojis, {message.author.mention}! They have feelings too, you know.")
                elif not emjfilter:
                    pass

    # ---~FILTERSETTINGS~---#
    @commands.group(brief="Change the filter settings!", aliases=["filterset"])
    @commands.has_permissions(administrator=True)
    async def filtersettings(self, ctx):
        """This is the parent command for the filter settings. Check each command's functionality!"""
        pass

    # --TOGGLE--#
    @filtersettings.command(aliases=["t"])
    async def toggle(self, ctx, filtertochange: str):
        """Toggles a filter!

        'Toggle' means whether the filter should be active on the current server or not. If the filter is already active, it will be turned off, and vice versa.

        Parameters:
          filter - The filter to toggle."""
        if filtertochange in filternames1:
            toggledPos = "how would I fucking know"
            with open("../DSB_Files/filters.json", "r") as filetoread:
                filters = json.load(filetoread)
            try:
                x = filters[str(ctx.guild.id)][filtertochange]
                if x:
                    filters[str(ctx.guild.id)][filtertochange] = False
                    toggledPos = False
                else:
                    filters[str(ctx.guild.id)][filtertochange] = True
                    toggledPos = True
            except KeyError:
                filters[str(ctx.guild.id)] = {filtertochange: True}
                toggledPos = True
            finally:
                with open("../DSB_Files/filters.json", "w") as filetowrite:
                    json.dump(filters, filetowrite)
                if toggledPos:
                    y = "enabled"
                else:
                    y = "disabled"
                await esay(ctx, discord.Embed(title="Filter toggled!",
                                              description=f"The filter ``{filtertochange}`` has been {y}!"))
        else:
            await say(ctx, ":interrobang: - Wrong filter name! Please use one of the following:\n```" + ",\n".join(filternames1) + "```")

    # --SETFILLIMIT--#
    @filtersettings.command(aliases=["sfl", "setfilterlimit"])
    async def setfillimit(self, ctx, filtertochange: str, limittoset: int):
        """Sets the limit of characters allowed inside of filters that use a limit!

        If not defined, it will default to the following values:

        Emojis: 5

        Parameters:
          filtertochange - The filter to change.
          limittoset - The limit to set. This must be a number!"""
        if filtertochange in filternames2:
            with open("../DSB_Files/emojis.json", "r") as filetoread:
                emjdict = json.load(filetoread)
            emjdict[str(ctx.guild.id)] = limittoset
            with open("../DSB_Files/emojis.json", "w") as filetowrite:
                json.dump(emjdict, filetowrite)
            await esay(ctx, discord.Embed(title="Filter changed!", description=f"The filter limit of {filtertochange} has been set to {limittoset}!"))
        else:
            await say(ctx, ":interrobang: - Wrong filter name! Please use one of the following:\n```" + ",\n".join(filternames2) + "```")

    # ---PREFIX---#
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix: str):
        """Define a custom prefix for the bot!

        If your prefix will contain spaces, quote your prefix!
        The custom prefix will not override the 3 default prefixes given. The custom prefix will only be added as a 4th prefix.

        Parameters:
          prefix - The prefix to set.

        Permissions:
          Administrator"""
        with open("../DSB_Files/prefixes.json", "r") as filetoread:
            prefixes = json.load(filetoread)
        prefixes[str(ctx.guild.id)] = prefix
        with open("../DSB_Files/prefixes.json", "w") as filetowrite:
            json.dump(prefixes, filetowrite)
        await say(ctx, ":white_check_mark: - Prefix set to > " + prefix + " < !")

    # ---PURGE---#
    @commands.command(aliases=["prune", "bulkdel", "clear"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        """Mass delete messages!

        The message limit is at 2000 per usage.
        The command will be slow(ish) if the number is bigger than 50, so please let it work while it's running!
        The bot is also only able to purge messages effectively fast if they're newer than 2 weeks, and the rate is at 50 messages per 5 seconds. Any messages older than 2 weeks will be deleted one-by-one at a much slower rate. This rate is very slow, so avoid making the bot delete any older messages.

        Parameters:
          number - The number of messages to prune. As said, max is 2000.

        Permissions:
          Manage messages"""
        numDel = await ctx.channel.purge(limit=number, bulk=True)
        await say(ctx, f":white_check_mark: - Deleted {len(numDel)} messages!")

    # ---MUTE---#
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = "No reason given."):
        """Mutes an user inside of the guild.

        The command currently has no time settings, so mutes are always permanent until manually undone.

        Parameters:
          member - The member to mute. Can be named, mentioned or ID'd.
          reason - The reason. This is optional, but recommended."""
        muterole = discord.utils.get(ctx.guild.roles, id=447154216985690112)
        await member.add_roles(muterole, reason=reason)
        await esay(ctx, discord.Embed(title="User muted!", description=f"{member} has been successfully muted.",
                                      color=0xFF8800))
        embed_mute = discord.Embed(title="Admin Log: User muted",
                                   description="An user has been muted inside of this guild.", color=0xFF8800)
        embed_mute.add_field(name="Admin", value=ctx.author)
        embed_mute.add_field(name="Muted User", value=member)
        embed_mute.add_field(name="Reason", value=reason)
        if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
            with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                chID = file.read()
            logch = self.bot.get_channel(int(chID))
        else:
            logch = ctx
        await esay(logch, embed_mute)

    # ---UNMUTE---#
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = "No reason given."):
        """Unmutes an user inside of the guild.

        Parameters:
          member - The member to unmute. Can be named, mentioned or ID'd.
          reason - The reason. This is optional, but recommended."""
        muterole = discord.utils.get(ctx.guild.roles, id=447154216985690112)
        await member.remove_roles(muterole, reason=reason)
        await esay(ctx, discord.Embed(title="User unmuted!", description=f"{member} has been successfully unmuted.",
                                      color=0xFF8800))
        embed_unmute = discord.Embed(title="Admin Log: User unmuted",
                                     description="An user has been unmuted inside of this guild.", color=0xFF8800)
        embed_unmute.add_field(name="Admin", value=ctx.author)
        embed_unmute.add_field(name="Unmuted User", value=member)
        embed_unmute.add_field(name="Reason", value=reason)
        if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
            with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                chID = file.read()
            logch = self.bot.get_channel(int(chID))
        else:
            logch = ctx
        await esay(logch, embed_unmute)

    # ---~EMBED~---#
    @commands.group(brief="Manage and create personal embeds! (WIP)")
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx):
        """This is the parent command for the embed commands. Check each command's functionality!

        ~WARNING!~ This command might be unstable. If you find any errors, please report them!

        Permissions:
          Administrator"""

    # --CREATETEMPLATE--#
    @embed.command()
    async def createtemplate(self, ctx):
        """Create a embed template, or reset your current one!

        No parameters required. It makes a basic template with a title, description and green color."""
        with open("../DSB_Files/embeds.json", "r") as filetoread:
            embedsdict = json.load(filetoread)
        embedsdict[str(ctx.guild.id)] = {"title": "Title here!", "description": "Description here!", "color": 0x00FF00,
                                         "field_num": 0}
        with open("../DSB_Files/embeds.json", "w") as filetowrite:
            json.dump(embedsdict, filetowrite)
        await esay(ctx, discord.Embed(title="Template created!",
                                      description="The template for this server has been created, happy editing!",
                                      color=0x00FF00))

    # --POST--#
    @embed.command()
    async def post(self, ctx):
        """Post your made embed!"""
        with open("../DSB_Files/embeds.json", "r") as file:
            embedsdict = json.load(file)
        try:
            title = embedsdict[str(ctx.guild.id)]["title"]
            if title == "-":
                title = discord.Embed.Empty
            description = embedsdict[str(ctx.guild.id)]["description"]
            color = embedsdict[str(ctx.guild.id)]["color"]
            embed_custom = discord.Embed(title=title, description=description, color=color)
            embed_field_count = int(embedsdict[str(ctx.guild.id)]["field_num"])
            if embed_field_count != 0:
                for x in range(embed_field_count):
                    y = x + 1
                    exec("embed_custom.add_field(name=embedsdict[str(ctx.guild.id)][\"field_{" + str(
                        y) + "}\"][\"name\"], value=embedsdict[str(ctx.guild.id)][\"field_{" + str(
                        y) + "}\"][\"value\"])")
            else:
                pass
            await esay(ctx, embed_custom)
        except KeyError:
            await say(ctx,
                      ":interrobang: - The bot had problems loading the embed! Did you even create one? ``DD!embed create``")

    # --SETTITLE--#
    @embed.command()
    async def settitle(self, ctx, *, text: str):
        """Sets a custom title!

        The title is the first bold text inside of an embed. The title does not need to be specified, only the description is mandatory. To remove the title, simply type in '-'."""
        with open("../DSB_Files/embeds.json", "r") as filetoread:
            embedsdict = json.load(filetoread)
        try:
            embedsdict[str(ctx.guild.id)]["title"] = text
            with open("../DSB_Files/embeds.json", "w") as filetowrite:
                json.dump(embedsdict, filetowrite)
            await say(ctx,
                      ":white_check_mark: - Embed title set to -> " + embedsdict[str(ctx.guild.id)]["title"] + " <- !")
        except KeyError:
            await say(ctx,
                      ":interrobang: - The bot had problems saving the settings! Did you even create a template? ``DD!embed create``")

    # --SETDESC--#
    @embed.command()
    async def setdesc(self, ctx, *, text: str):
        """Sets a custom description!

        The title is the first field of regular text of an embed. The description is minimally required to let an embed be postable.

        A description can contain hyperlinks! Just use the following concept: [here goes your text](here goes your link)

        PLEASE NOTICE! If you want to use hyperlinks inside of your embed, the links MUST start with either 'http://' or 'https://', else the hyperlink won't work. This is an issue from Discord's side, the bot can not counter this."""
        with open("../DSB_Files/embeds.json", "r") as filetoread:
            embedsdict = json.load(filetoread)
        try:
            embedsdict[str(ctx.guild.id)]["description"] = text
            with open("../DSB_Files/embeds.json", "w") as filetowrite:
                json.dump(embedsdict, filetowrite)
            await say(ctx, ":white_check_mark: - Embed description set to -> " + embedsdict[str(ctx.guild.id)][
                "description"] + "<- !")
        except KeyError:
            await say(ctx,
                      ":interrobang: - The bot had problems saving the settings! Did you even create a template? ``DD!embed create``")

    # --SETFIELDNUM--#
    @embed.command()
    async def setfieldnum(self, ctx, num: int):
        """Sets the number of fields for the embed to use.

        PLEASE NOTICE!
        Defining a new field number will reset all fields."""
        with open("../DSB_Files/embeds.json", "r") as filetoread:
            embedsdict = json.load(filetoread)
        try:
            embedsdict[str(ctx.guild.id)]["field_num"] = num
            for x in range(num):
                y = x + 1
                exec("embedsdict[str(ctx.guild.id)][\"field_{" + str(y) + "}\"] = {\"name\": \"Field " + str(
                    y) + " Name\", \"value\": \"Field " + str(y) + " Value\"}")
            with open("../DSB_Files/embeds.json", "w") as filetowrite:
                json.dump(embedsdict, filetowrite)
            await say(ctx, f":white_check_mark: - Embed field count set to {num}!")
        except KeyError:
            await say(ctx,
                      ":interrobang: - The bot had problems saving the settings! Did you even create a template? ``DD!embed create``")

    # --SETFIELDNAME--#
    @embed.command()
    async def setfieldname(self, ctx, num: int, *, text: str):
        """Sets a field name!

        The name of a field is the bold text. It's mandatory for every field to have a name defined."""
        with open("../DSB_Files/embeds.json", "r") as filetoread:
            embedsdict = json.load(filetoread)
        try:
            embedsdict[str(ctx.guild.id)]["field_{" + str(num) + "}"]["name"] = text
            with open("../DSB_Files/embeds.json", "w") as filetowrite:
                json.dump(embedsdict, filetowrite)
            await say(ctx, f":white_check_mark: - Embed number {str(num)}'s name set to -> {text} <- !")
        except KeyError:
            await say(ctx,
                      ":interrobang: - The bot had problems saving the settings! Did you even create a template? ``DD!embed create``")

    # --SETFIELDVALUE--#
    @embed.command()
    async def setfieldvalue(self, ctx, num: int, *, text: str):
        """Sets a field value!

        The value of a field is the regular text. It's mandatory for every field to have a value defined.

        A field value can contain hyperlinks! Just use the following concept: [here goes your text](here goes your link)

        PLEASE NOTICE! If you want to use hyperlinks inside of your embed, the links MUST start with either 'http://' or 'https://', else the hyperlink won't work. This is an issue from Discord's side, the bot can not counter this."""
        with open("../DSB_Files/embeds.json", "r") as filetoread:
            embedsdict = json.load(filetoread)
        try:
            embedsdict[str(ctx.guild.id)]["field_{" + str(num) + "}"]["value"] = text
            with open("../DSB_Files/embeds.json", "w") as filetowrite:
                json.dump(embedsdict, filetowrite)
            await say(ctx, f":white_check_mark: - Embed number {str(num)}'s value set to -> {text} <- !")
        except KeyError:
            await say(ctx,
                      ":interrobang: - The bot had problems saving the settings! Did you even create a template? ``DD!embed create``")

    # ---~WARN~---#
    @commands.group(brief="Manage warns on users!")
    async def warn(self, ctx):
        """This is the parent command for the warn/unwarn commands. Check each command's functionality!

       Permissions:
         Kick members/Ban members for 'add', kick members for 'remove', administrator for 'set' and 'setlimit'."""

        pass

    # --SETLIMIT--#
    @warn.command()
    @commands.has_permissions(administrator=True)
    async def setlimit(self, ctx, number: int):
        """Set the warn limit!

        Defaults to 3."""
        with open("../DSB_Files/warns.json", "r") as filetoread:
            warnsdict = json.load(filetoread)
        warnsdict[ctx.guild.id] = {"limit": number}
        with open("../DSB_Files/warns.json", "w") as filetowrite:
            json.dump(warnsdict, filetowrite)
        await esay(ctx, discord.Embed(title="Limit set!",
                                      description=f"The warn limit for this server has been set to {number}!"))

    # --ADD--#
    @warn.command()
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def add(self, ctx, member: discord.Member, *, reason: str = "No reason specified."):
        """Warns an user!

        If the warns and limit equal, the user will be kicked. However, a warn number that exceeds the limit will cause the bot to ban the user."""
        with open("../DSB_Files/warns.json", "r") as filetoread:
            warnsdict = json.load(filetoread)
        try:
            warnlimit = warnsdict[str(ctx.guild.id)]["limit"]
        except KeyError:
            warnlimit = 3
        try:
            pastwarns = warnsdict[str(ctx.guild.id)][str(member.id)]
            warnsdict[str(ctx.guild.id)][str(member.id)] = pastwarns + 1
        except KeyError:
            warnsdict[str(ctx.guild.id)] = {str(member.id): 1}
        finally:
            if warnsdict[str(ctx.guild.id)][str(member.id)] < warnlimit:
                await esay(ctx, discord.Embed(title="User warned!",
                                              description=f"User {member.mention} has been successfully warned. He currently has {warnsdict[str(ctx.guild.id)][str(member.id)]} warns.",
                                              color=0xFFFF00))
                if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
                    with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                        chID = file.read()
                    logch = self.bot.get_channel(int(chID))
                else:
                    logch = ctx
                embed_warned = discord.Embed(title="Admin Log: User warn",
                                             description="An user has been warned inside of this guild.",
                                             color=0xFFFF00)
                embed_warned.add_field(name="Admin", value=ctx.author.mention)
                embed_warned.add_field(name="Warned user", value=member.mention)
                embed_warned.add_field(name="Reason", value=reason)
                await esay(logch, embed_warned)
            elif warnsdict[str(ctx.guild.id)][str(member.id)] == warnlimit:
                await member.kick(
                    reason=f"[WARN] - Warns have been exceeded. The warn has been executed by {ctx.author} . The reason for the warn is: {reason}")
                await esay(ctx, discord.Embed(title="User kicked!",
                                              description=f"User {member} has been kicked due to exceeded warns. The next warn will result in a ban!",
                                              color=0xFFFF00))
                if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
                    with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                        chID = file.read()
                    logch = self.bot.get_channel(int(chID))
                else:
                    logch = ctx
                embed_warnkicked = discord.Embed(title="Admin Log: User warn-kick",
                                                 description="An user has been warned and warns have been exceeded, the user has been kicked.",
                                                 color=0xFFFF00)
                embed_warnkicked.add_field(name="Admin", value=ctx.author.mention)
                embed_warnkicked.add_field(name="Kicked user", value=member)
                embed_warnkicked.add_field(name="Reason", value=reason)
                await esay(logch, embed_warnkicked)
            elif warnsdict[str(ctx.guild.id)][str(member.id)] > warnlimit:
                await member.ban(
                    reason=f"[WARN] - Warns have been exceeded. The warn has been executed by {ctx.author} . The reason for the warn is: {reason}")
                await esay(ctx, discord.Embed(title="User banned!",
                                              description=f"User {member} has been banned due to exceeded warns.",
                                              color=0xFFFF00))
                if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
                    with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                        chID = file.read()
                    logch = self.bot.get_channel(int(chID))
                else:
                    logch = ctx
                embed_warnbanned = discord.Embed(title="Admin Log: User warn-ban",
                                                 description="An user has been warned and warns have been exceeded, the user has been banned.",
                                                 color=0xFFFF00)
                embed_warnbanned.add_field(name="Admin", value=ctx.author.mention)
                embed_warnbanned.add_field(name="Banned user", value=member)
                embed_warnbanned.add_field(name="Reason", value=reason)
                await esay(logch, embed_warnbanned)
            with open("../DSB_Files/warns.json", "w") as filetowrite:
                json.dump(warnsdict, filetowrite)

    # --REMOVE--#
    @warn.command()
    @commands.has_permissions(kick_members=True)
    async def remove(self, ctx, member: discord.Member, *, reason: str = "No reason specified."):
        """Unwarns an user!

        The warns are set to 0."""
        nowarnfound = False
        with open("../DSB_Files/warns.json", "r") as filetoread:
            warnsdict = json.load(filetoread)
        try:
            warnsdict[str(ctx.guild.id)][str(member.id)] = 0
        except KeyError:
            nowarnfound = True
            await say(ctx, ":interrobang: - The mentioned user has never been warned!")
        finally:
            if not nowarnfound:
                await esay(ctx, discord.Embed(title="Warns cleaned!", description=f"User {member} is no longer warned!",
                                              color=0x00FF00))
                if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
                    with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                        chID = file.read()
                    logch = self.bot.get_channel(int(chID))
                else:
                    logch = ctx
                embed_warncleaned = discord.Embed(title="Admin Log: User unwarn",
                                                  description="An user has been unwarned inside of this guild.",
                                                  color=0xFFFF00)
                embed_warncleaned.add_field(name="Admin", value=ctx.author.mention)
                embed_warncleaned.add_field(name="Unwarned user", value=member.mention)
                embed_warncleaned.add_field(name="Reason", value=reason)
                await esay(logch, embed_warncleaned)
                with open("../DSB_Files/warns.json", "w") as filetowrite:
                    json.dump(warnsdict, filetowrite)
            else:
                pass

    # --SET--#
    @warn.command()
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, member: discord.Member, number: int):
        """'Hardcode' an user's warns!

        This command can set the warns of an user at a desired amount. Please keep in mind that this command is not capable of kicking/banning users if the limit has been hit or exceeded."""
        with open("../DSB_Files/warns.json", "r") as filetoread:
            warnsdict = json.load(filetoread)
        try:
            warnsdict[str(ctx.guild.id)][str(member.id)] = number
        except KeyError:
            warnsdict[str(ctx.guild.id)] = {member.id: number}
        finally:
            with open("../DSB_Files/warns.json", "w") as filetowrite:
                json.dump(warnsdict, filetowrite)
            await esay(ctx, discord.Embed(title="Warns have been set!",
                                          description=f"The warns of {member.mention} have been set to {number}!",
                                          color=0x00FF00))

    # --CHECK--#
    @warn.command()
    async def check(self, ctx, member: discord.Member = None):
        """Checks the limit and, if given, member's warns!"""
        warnlimit = 3
        memberwarns = 0
        nicedescription = f"The limit of the server's warns is set to {warnlimit}."
        with open("../DSB_Files/warns.json", "r") as filetoread:
            warnsdict = json.load(filetoread)
        try:
            warnlimit = warnsdict[str(ctx.guild.id)]["limit"]
        except KeyError:
            pass
        if member != None:
            try:
                memberwarns = warnsdict[str(ctx.guild.id)][str(member.id)]
            except KeyError:
                pass
            nicedescription = f"The member's warns are currently at {memberwarns} and the limit of the server's warns is set to {warnlimit}."
        await esay(ctx, discord.Embed(title="Information gathered!", description=nicedescription, color=0x00FF00))

    # ---SETLOG---#
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel = None):
        """Sets the log channel.

        Parameters:
          channel - The channel used for the logs. The channel has to be mentioned normally and the bot needs to be able to read and send to it.

        Permissions:
          Administrator"""
        if channel != None:
            fs.write(f"../DSB_Files/log_of_{ctx.guild.id}.txt", str(channel.id))
            await say(ctx, ":white_check_mark: - Log Channel set!")
        else:
            if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
                os.remove(f"../DSB_Files/log_of_{ctx.guild.id}.txt")
                await say(ctx, ":white_check_mark: - Log channel deleted out of memory!")
            else:
                await say(ctx, ":interrobang: - Please mention a channel!")

    # ---KICK---#
    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks an user from the current guild.

        Parameters:
          member - The user to kick. The user can be mentioned, named or ID'ed.
          reason - (Optional) The reason for the kick. You can leave this empty. The reason will be shown inside of the audit log.

        Permissions:
          Kick members"""
        if member != None:
            await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
            await esay(ctx, discord.Embed(title=f"Kicked member {member}",
                                          description=f"Member {member} has been successfully kicked from this guild!",
                                          color=0xFF0000))
            embed_kick = discord.Embed(title="Admin log: Member kick",
                                       description="A kick has been issued inside of this server.", color=0xFF0000)
            embed_kick.add_field(name="Admin", value=ctx.author)
            embed_kick.add_field(name="Kicked member", value=member)
            embed_kick.add_field(name="Reason", value=reason, inline=False)
            if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
                with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                    chID = file.read()
                logch = self.bot.get_channel(int(chID))
            else:
                logch = ctx
            await logch.send(embed=embed_kick)
        else:
            await say(ctx, ":interrobang: - Please mention a member to kick!")

    # ---BAN---#
    @commands.command(aliases=["b"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Bans an user from the current guild.

        Parameters:
          member - The user to ban. The user can be mentioned, named or ID'ed.
          reason - (Optional) The reason for the ban. You can leave this empty. The reason will be shown inside of the audit log.

        Permissions:
          Ban/Unban members"""
        await member.ban(reason=f"Banned by {ctx.author}: {reason}")
        await esay(ctx, discord.Embed(title=f"Banned member {member}",
                                      description=f"Member {member} has been successfully banned from this guild!",
                                      color=0xFF0000))
        embed_ban = discord.Embed(title="Admin log: Member ban",
                                  description="A ban has been issued inside of this server.", color=0xFF0000)
        embed_ban.add_field(name="Admin", value=ctx.author)
        embed_ban.add_field(name="Banned member", value=member)
        embed_ban.add_field(name="Reason", value=reason, inline=False)
        if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
            with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                chID = file.read()
            logch = self.bot.get_channel(int(chID))
        else:
            logch = ctx
        await logch.send(embed=embed_ban)

    # ---HACKBAN---#
    @commands.command(aliases=["hban", "hb"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def hackban(self, ctx, userID: int, *, reason: str = None):
        """Bans a user by ID from the current guild.

        This ban is special, as it can ban users that aren't inside of the guild at all. However, their ID is required for this.

        Parameters:
          userID - The ID of the user to ban. Only integers (numeric characters) are accepted.
          reason - (Optional) The reason for the ban. You can leave this empty. The reason will be shown inside of the audit log.

        Permissions:
          Ban/Unban members"""
        user = await self.bot.get_user_info(user_id=userID)
        await ctx.guild.ban(user, delete_message_days=0, reason=f"[HACKBAN] Banned by {ctx.author}: {reason}")
        await esay(ctx, discord.Embed(title=f"Banned member {user}",
                                      description=f"Member {user} has been successfully banned from this guild!",
                                      color=0xFF0000))
        embed_hban = discord.Embed(title="Admin log: Hackban",
                                   description="A hackban has been issued inside of this server.", color=0xFF0000)
        embed_hban.add_field(name="Admin", value=ctx.author)
        embed_hban.add_field(name="Hackbanned member", value=user)
        embed_hban.add_field(name="Reason", value=reason, inline=False)
        if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
            with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                chID = file.read()
            logch = self.bot.get_channel(int(chID))
        else:
            logch = ctx
        await logch.send(embed=embed_hban)

    # ---UNBAN---#
    @commands.command(aliases=["unban", "ub"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def pardon(self, ctx, memID: int, *, reason: str = None):
        """Unbans a banned user from the current guild.

        Parameters:
          memID - The ID of the member to be unbanned. You can either find it yourself or use *DD!banlist* to get it.
          reason - (Optional) The reason for the unban. You can leave this empty. The reason will be shown inside of the audit log.

        Permissions:
          Ban/Unban members"""
        memObj = self.bot.get_user_info(user_id=int(memID))
        await memObj.unban(reason=f"Unbanned by {ctx.author}: {reason}")
        await esay(ctx, discord.Embed(title=f"Unbanned member {memObj.name}",
                                      description=f"Member {memObj.name} has been successfully unbanned from this guild!",
                                      color=0x00FF00))
        embed_unban = discord.Embed(title="Admin log: Member unban",
                                    description="An unban has been issued inside of this server.", color=0x00FF00)
        embed_unban.add_field(name="Admin", value=ctx.author)
        embed_unban.add_field(name="Unbanned member", value=memObj)
        embed_unban.add_field(name="Reason", value=reason, inline=False)
        if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
            with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
                chID = file.read()
            logch = self.bot.get_channel(int(chID))
        else:
            logch = ctx
        logch.send(embed=embed_unban)

    # ---BANLIST---#
    @commands.command(aliases=["bans", "blist"])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def banlist(self, ctx):
        """Get all the ban entires for this server.

        Requirements:
          Ban/Unban members"""
        if len(await ctx.guild.bans()) != 0:
            await say(ctx, "\n".join(
                [":hammer: Name: {.user.name} ID: {.user.id} Reason: {.reason}".format(entry, entry, entry) for entry in
                 await ctx.guild.bans()]))
        else:
            await say(ctx, "No bans are found inside of this server!")

    # ---~CHANNEL~---#
    @commands.group(brief="Manage channels!")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def channel(self, ctx):
        """This is the parent command of the 'channel' commands. Each command will serve a different purpose and will require different parameters. Check each command before using them!

        Permissions:
          Manage channels"""

    # --CREATE--#
    @channel.command(brief="Create a channel.")
    async def create(self, ctx, name="new-channel", nsfw=False, *, topic=None):
        """Creates a channel inside of the current guild."""
        crch = await ctx.guild.create_text_channel(name=name, reason=f"Created by {ctx.author} - {ctx.author.id}")
        if nsfw:
            await crch.edit(nsfw=True, reason=f"Created by {ctx.author} - {ctx.author.id} with NSFW.")
        if topic:
            await crch.edit(reason=f"Created by {ctx.author} - {ctx.author.id} with a topic.", topic=topic)
        await say(ctx, f":white_check_mark: - Channel {crch.name} - {crch.id} - <#{crch.id}> created!")

    # --EDIT--#
    @channel.command(brief="Edit a channel.")
    async def edit(self, ctx, target: discord.TextChannel, nsfw=False, name=None):
        """Edits a channel inside of the current guild. Channels can get edited using their name, ID or mention."""
        if not name:
            await target.edit(reason=f"Edited by {ctx.author} - {ctx.author.id}", nsfw=nsfw)
        else:
            await target.edit(reason=f"Edited by {ctx.author} - {ctx.author.id}", nsfw=nsfw, name=name)
        await say(ctx, f":white_check_mark: - Channel edited!")

    # --DELETE--#
    @channel.command(brief="Delete a channel.")
    async def delete(self, ctx, target: discord.TextChannel, *, reason: str = "No reason provided."):
        """Deletes a channel from the current guild. Channels can get edited using their name, ID or mention."""
        await target.delete(reason=f"Deleted by {ctx.author} - {ctx.author.id} -- " + reason)
        await say(ctx, f":white_check_mark: - Channel deleted!")


def setup(bot):
    bot.add_cog(Admin(bot))
