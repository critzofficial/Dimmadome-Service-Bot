from discord.ext import commands
import discord
import fs
import os

denied = ":interrobang: - You are not permissioned to use this command!"

ownerID = 255802794244571136


class Admin:
	"""This category is all about admin commands. Permissions are enlisted in the further description of each command."""

	def __init__(self, bot):
		self.bot = bot

	#---PURGE---#
	@commands.command(aliases=["prune", "bulkdel"])
	@commands.has_permissions(manage_messages=True)
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
		await ctx.send(f":white_check_mark: - Deleted {len(numDel)} messages!")

	#---SETLOG---#
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def setlog(self, ctx, channel: discord.TextChannel=None):
		"""Sets the log channel.
		
		Parameters:
			channel - The channel used for the logs. The channel has to be mentioned normally and the bot needs to be able to read and send to it.
			
		Permissions:
			Administrator"""
		if channel != None:
			fs.write(f"../DSB_Files/log_of_{ctx.guild.id}.txt", str(channel.id))
			await ctx.send(":white_check_mark: - Log Channel set!")
		else:
			if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
				os.remove(f"../DSB_Files/log_of_{ctx.guild.id}.txt")
				await ctx.send(":white_check_mark: - Log channel deleted out of memory!")
			else:
				await ctx.send(":interrobang: - Please mention a channel!")

	#---KICK---#
	@commands.command(aliases=["k"])
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, *, reason: str=None):
		"""Kicks a mentioned user from the current guild.
		
		Parameters:
			member - The user to kick. The user must be mentioned.
			reason - (Optional) The reason for the kick. You can leave this empty. The reason will be shown inside of the audit log.
			
		Permissions:
			Kick members"""
		if member != None:
			await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
			await ctx.send(embed=discord.Embed(title=f"Kicked member {member}", description=f"Member {member} has been successfully kicked from this guild!", color=0xFF0000))
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
			await ctx.send(":interrobang: - Please mention a member to kick!")

	#---BAN---#
	@commands.command(aliases=["b"])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member, *, reason: str=None):
		"""Bans a mentioned user from the current guild.
		
		Parameters:
			member - The user to ban. The user must be mentioned.
			reason - (Optional) The reason for the ban. You can leave this empty. The reason will be shown inside of the audit log.
			
		Permissions:
			Ban/Unban members"""
		await member.ban(reason=f"Banned by {ctx.author}: {reason}")
		await ctx.send(embed=discord.Embed(title=f"Banned member {member}", description=f"Member {member} has been successfully banned from this guild!", color=0xFF0000))
		embed_kick = discord.Embed(title="Admin log: Member ban", description="A ban has been issued inside of this server.", color=0xFF0000)
		embed_kick.add_field(name="Admin", value=ctx.author)
		embed_kick.add_field(name="Banned member", value=member)
		embed_kick.add_field(name="Reason", value=reason, inline=False)
		if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
			with open(f"../DSB_Files/log_of_{ctx.guild.id}.txt", "r") as file:
				chID = file.read()
			logch = self.bot.get_channel(int(chID))
		else:
			logch = ctx
		await logch.send(embed=embed_kick)

	#---UNBAN---#
	@commands.command(aliases=["unban", "ub"])
	@commands.has_permissions(ban_members=True)
	async def pardon(self, ctx, memID: int, *, reason: str=None):
		"""Unbans a banned user from the current guild.
		
		Parameters:
			memID - The ID of the member to be unbanned. You can either find it yourself or use *DD!banlist* to get it.
			reason - (Optional) The reason for the unban. You can leave this empty. The reason will be shown inside of the audit log.
			
		Permissions:
			Ban/Unban members"""
		memObj = self.bot.get_user_info(user_id=int(memID))
		await memObj.unban(reason=f"Unbanned by {ctx.author}: {reason}")
		await ctx.send(embed=discord.Embed(title=f"Unbanned member {memObj.name}", description=f"Member {memObj.name} has been successfully unbanned from this guild!", color=0x00FF00))
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

	#---BANLIST---#
	@commands.command(aliases=["bans", "blist"])
	@commands.has_permissions(ban_members=True)
	async def banlist(self, ctx):
		"""Get all the ban entires for this server.
		
		Requirements:
			Ban/Unban members"""
		if len(await ctx.guild.bans()) != 0:
			await ctx.send("\n".join([":hammer: Name: {.user.name} ID: {.user.id} Reason: {.reason}".format(entry, entry, entry) for entry in await ctx.guild.bans()]))
		else:
			await ctx.send("No bans are found inside of this server!")


def setup(bot):
	bot.add_cog(Admin(bot))
