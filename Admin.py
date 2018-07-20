from discord.ext import commands
import discord
import fs
import os


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)

ownerID = 255802794244571136


class Admin:
    """This category is all about admin commands. Permissions are enlisted in the further description of each command."""

    def __init__(self, bot):
        self.bot = bot

    # ---PURGE---#
    @commands.command(aliases=["prune", "bulkdel"])
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
        """Kicks a mentioned user from the current guild.

        Parameters:
            member - The user to kick. The user must be mentioned.
            reason - (Optional) The reason for the kick. You can leave this empty. The reason will be shown inside of the audit log.

        Permissions:
            Kick members"""
        if member != None:
            await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
            await esay(ctx, discord.Embed(title=f"Kicked member {member}", description=f"Member {member} has been successfully kicked from this guild!", color=0xFF0000))
            embed_kick = discord.Embed(title="Admin log: Member kick", description="A kick has been issued inside of this server.", color=0xFF0000)
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
        """Bans a mentioned user from the current guild.

        Parameters:
            member - The user to ban. The user must be mentioned.
            reason - (Optional) The reason for the ban. You can leave this empty. The reason will be shown inside of the audit log.

        Permissions:
            Ban/Unban members"""
        await member.ban(reason=f"Banned by {ctx.author}: {reason}")
        await esay(ctx, discord.Embed(title=f"Banned member {member}", description=f"Member {member} has been successfully banned from this guild!", color=0xFF0000))
        embed_ban = discord.Embed(title="Admin log: Member ban", description="A ban has been issued inside of this server.", color=0xFF0000)
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
        """Bans a user by ID from the current guild. (Credit goes to DakotaBot by KazWolfe for the command name, this is to not get copyrighted :3)

        This ban is special, as it can ban users that aren't inside of the guild at all. However, their ID is required for this.

        Parameters:
            userID - The ID of the user to ban. Only integers (numeric characters) are accepted.
            reason - (Optional) The reason for the ban. You can leave this empty. The reason will be shown inside of the audit log.

        Permissions:
            Ban/Unban members"""
        user = await self.bot.get_user_info(user_id=userID)
        await ctx.guild.ban(user, delete_message_days=0, reason=f"[HACKBAN] Banned by {ctx.author}: {reason}")
        await esay(ctx, discord.Embed(title=f"Banned member {user}", description=f"Member {user} has been successfully banned from this guild!", color=0xFF0000))
        embed_hban = discord.Embed(title="Admin log: Hackban", description="A hackban has been issued inside of this server.", color=0xFF0000)
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
        await esay(ctx, discord.Embed(title=f"Unbanned member {memObj.name}", description=f"Member {memObj.name} has been successfully unbanned from this guild!", color=0x00FF00))
        embed_unban = discord.Embed(title="Admin log: Member unban", description="An unban has been issued inside of this server.", color=0x00FF00)
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
    @commands.group()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def channel(self, ctx):
        """This is the parent command of the 'channel' commands. Each command will serve a different purpose and will require different parameters. Check each command before using them!

        Permissions:
            Manage channels"""

    # ---ADD---#
    @channel.command(brief="Create a channel.")
    async def add(self, ctx, name="new-channel", nsfw=False, *, topic=None):
        """Creates a channel inside of the current guild."""
        crch = await ctx.guild.create_text_channel(name=name, reason=f"Created by {ctx.author} - {ctx.author.id}")
        if nsfw:
            await crch.edit(nsfw=True, reason=f"Created by {ctx.author} - {ctx.author.id} with NSFW.")
        if topic:
            await crch.edit(reason=f"Created by {ctx.author} - {ctx.author.id} with a topic.", topic=topic)
        await say(ctx, f":white_check_mark: - Channel {crch.name} - {crch.id} - <#{crch.id}> created!")

    # ---EDIT---#
    @channel.command(brief="Edit a channel.")
    async def edit(self, ctx, target: discord.TextChannel, nsfw=False, name=None):
        """Edits a channel inside of the current guild. Channels can get edited using their name, ID or mention."""
        if not name:
            await target.edit(reason=f"Edited by {ctx.author} - {ctx.author.id}", nsfw=nsfw)
        else:
            await target.edit(reason=f"Edited by {ctx.author} - {ctx.author.id}", nsfw=nsfw, name=name)
        await say(ctx, f":white_check_mark: - Channel edited!")

    # ---DELETE---#
    @channel.command(brief="Delete a channel.")
    async def delete(self, ctx, target: discord.TextChannel, *, reason: str="No reason provided."):
        """Deletes a channel from the current guild. Channels can get edited using their name, ID or mention."""
        await target.delete(reason=f"Deleted by {ctx.author} - {ctx.author.id} -- " + reason)
        await say(ctx, f":white_check_mark: - Channel deleted!")


def setup(bot):
    bot.add_cog(Admin(bot))
