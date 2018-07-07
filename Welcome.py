from discord.ext import commands
import discord
import json


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
			await channel.send(msg)
			
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
			await channel.send(msg)
		
	#---SETWELCOME---#
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def setwelcome(self, ctx, channel: discord.TextChannel, *, message: str):
		"""Sets the welcome channel and message!
		
		Whenever a new user joins, bot or not, a message will be sent, when this is defined.
		
		Parameters:
			channel - The channel to use. The channel must be mentioned. (e.g. #general)
			message - The message to use. Please avoid using emojis, as they don't get saved properly!"""
		with open("../DSB_Files/welcome.json", "r") as filetoread:
			srvdict = json.load(filetoread)
		srvdict[str(ctx.guild.id)] = {"chID": str(channel.id), "msg": str(message)}
		with open("../DSB_Files/welcome.json", "w") as filetowrite:
			json.dump(srvdict, filetowrite)
		await ctx.send(":white_check_mark: - Welcome message and channel set!")
		
	#---TESTWELCOME---#
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def testwelcome(self, ctx):
		"""Tests the welcome channel and message!
		
		The bot must have access to send in the specific channel at *all* times."""
		with open("../DSB_Files/welcome.json", "r") as filetoread:
			srvdict = json.load(filetoread)
		if not str(ctx.guild.id) in srvdict:
			await ctx.send(":interrobang: - Your server has no welcome settings defined!")
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
			await channel.send(msg)
	
	#---DELWELCOME---#
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def delwelcome(self, ctx):
		"""Deletes the welcome settings for this guild.
		
		Both channel and message will get deleted."""
		with open("../DSB_Files/welcome.json", "r") as filetoread:
			srvdict = json.load(filetoread)
		if not str(ctx.guild.id) in srvdict:
			await ctx.send(":interrobang: - Your server has no welcome settings defined!")
		else:
			del srvdict[str(ctx.guild.id)]
			with open("../DSB_Files/welcome.json", "w") as filetowrite:
				json.dump(srvdict, filetowrite)
			await ctx.send(":white_check_mark: - Welcome settings deleted!")
				
	#---SETLEAVE---#
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def setleave(self, ctx, channel: discord.TextChannel, *, message: str):
		"""Sets the leave channel and message!
		
		Whenever an user leaves, bot or not, a message will be sent, when this is defined.
		
		Parameters:
			channel - The channel to use. The channel must be mentioned. (e.g. #general)
			message - The message to use. Please avoid using emojis, as they don't get saved properly!"""
		with open("../DSB_Files/leave.json", "r") as filetoread:
			srvdict = json.load(filetoread)
		srvdict[str(ctx.guild.id)] = {"chID": str(channel.id), "msg": str(message)}
		with open("../DSB_Files/leave.json", "w") as filetowrite:
			json.dump(srvdict, filetowrite)
		await ctx.send(":white_check_mark: - Leave message and channel set!")
		
	#---TESTLEAVE---#
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def testleave(self, ctx):
		"""Tests the leave channel and message!
		
		The bot must have access to send in the specific channel at *all* times."""
		with open("../DSB_Files/leave.json", "r") as filetoread:
			srvdict = json.load(filetoread)
		if not str(ctx.guild.id) in srvdict:
			await ctx.send(":interrobang: - Your server has no leave settings defined!")
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
			await channel.send(msg)
	
	#---DELLEAVE---#
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def delleave(self, ctx):
		"""Deletes the leave settings for this guild.
		
		Both channel and message will get deleted."""
		with open("../DSB_Files/leave.json", "r") as filetoread:
			srvdict = json.load(filetoread)
		if not str(ctx.guild.id) in srvdict:
			await ctx.send(":interrobang: - Your server has no welcome settings defined!")
		else:
			del srvdict[str(ctx.guild.id)]
			with open("../DSB_Files/leave.json", "w") as filetowrite:
				json.dump(srvdict, filetowrite)
			await ctx.send(":white_check_mark: - Leave settings deleted!")


def setup(bot):
	bot.add_cog(Welcome(bot))
