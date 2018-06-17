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

	#---DISMISS---#
	@commands.command(description="Makes the bot leave the server.\nRequired permissions: administrator")
	async def dismiss(self, ctx):
		"""Make me leave. :["""
		if ctx.author.guild_permissions.administrator:
			await ctx.guild.leave()
			
	#---SETLOG---#
	@commands.command(description="Sets the log channel for the bot. These are used for various admin commands.")
	async def setlog(self, ctx, channel: discord.TextChannel=None):
		"""Sets the log channel."""
		if ctx.author.guild_permissions.administrator:
			if channel != None:
				fs.write(f"../DSB_Files/log_of_{ctx.guild.id}.txt", str(channel.id))
				await ctx.send(":white_check_mark: - Log Channel set!")
			else:
				if fs.exists(f"../DSB_Files/log_of_{ctx.guild.id}.txt"):
					os.remove(f"../DSB_Files/log_of_{ctx.guild.id}.txt")
					await ctx.send(":white_check_mark: - Log channel deleted out of memory!")
				else:
					await ctx.send(":interrobang: - Please mention a channel!")
		else:
			await ctx.send(denied)
			
	#---KICK---#
	@commands.command(description="..or there are more? Kicks a member from the guild. The member must be mentioned.", aliases=["k"])
	async def kick(self, ctx, member: discord.Member, *, reason: str=None):
		"""Kick that one bad behaving boy."""
		if ctx.author.guild_permissions.kick_members:
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
		else:
			await ctx.send(denied)
			
	#---BAN---#
	@commands.command(description="..or there are more again? Bans a member from the guild. The member must be mentioned.", aliases=["b"])
	async def ban(self, ctx, member: discord.Member, *, reason: str=None):
		"""Bans that one extra bad behaving boy."""
		if ctx.author.guild_permissions.ban_members:
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
		else:
			await ctx.send(denied)
	
	#---UNBAN---#
	@commands.command(description="Unbans a member banned inside of the current guild. The ID has to be used for the unban.", aliases=["unban", "ub"])
	async def pardon(self, ctx, memID: int, *, reason: str=None):
		"""Unbans a now good boy."""
		if ctx.author.guild_permissions.ban_members:
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
	@commands.command(description="This command writes down the name, ID and reason of each ban found inside of the server. To unban someone, always use the ID.", aliases=["bans", "blist"])
	async def banlist(self, ctx):
		"""Get all the ban entires for this server."""
		if ctx.author.guild_permissions.ban_members:
			if len(await ctx.guild.bans()) != 0:
				await ctx.send("\n".join([":hammer: Name: {.user.name} ID: {.user.id} Reason: {.reason}".format(entry, entry, entry) for entry in await ctx.guild.bans()]))
			else:
				await ctx.send("No bans are found inside of this server!")
	
	#---WARN---#
	@commands.command(description="If the warns exceed the number of 3, kicks will be handed out to the targets instead.")
	async def warn(self, ctx, member: discord.Member):
		"""Warns an user."""
		if ctx.author.guild_permissions.kick_members:
			if fs.exists(f"../DSB_Files/warns_of_{member.id}.txt"):
				with open(f"../DSB_Files/warns_of_{member.id}.txt", "r") as file:
					warns = int(file.read())
			else:
				warns = 0
			if warns < 2:
				warns += 1
				await ctx.send(embed=discord.Embed(title="Warn Command", description=f"Successfully warned {member.name}!", color=0xFF7000))
				fs.write(f"../DSB_Files/warns_of_{member.id}.txt", str(warns))
			elif warns == 2:
				await member.kick(reason=f"Warned by {ctx.author.name}: Warns have been exceeded")
				embed_warnk = discord.Embed(title="Warn kick", description="A kick for excessive warns has been issued inside of this server.", color=0xFF0000)
				embed_warnk.add_field(name="Admin", value=ctx.author)
				embed_warnk.add_field(name="Kicked member", value=member)
				await ctx.send(embed=embed_warnk)
				
	#---UNWARN---#
	@commands.command(description="This command fully deletes the warns of the user.")
	async def unwarn(self, ctx, member: discord.Member):
		"""Unwarns an user."""
		embed_notwarned = discord.Embed(title="Unwarn Command", description=f"{member.name} has never been warned!", color=0xFFFFFF)
		if ctx.author.guild_permissions.kick_members:
			if fs.exists(f"./DSB_Files/warns_of_{member.id}.txt"):
				with open(f"./DSB_Files/warns_of_{member.id}.txt", "r") as file:
					warns = int(file.read())
				if warns > 0:
					fs.write(f"./DSB_Files/warns_of_{member.id}.txt", "0")
					await ctx.send(embed=discord.Embed(title="Unwarn Command", description=f"Successfully unwarned {member.name}!", color=0x00FF00))
				else:
					await ctx.send(embed=embed_notwarned)
			else:
				await ctx.send(embed=embed_notwarned)

def setup(bot):
	bot.add_cog(Admin(bot))
