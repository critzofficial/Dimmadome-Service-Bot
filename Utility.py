from discord.ext import commands
import discord
import time
import hashlib

ownerID = 255802794244571136


class Utility:
	"""This category is all about any kind of commands that couldn't fit in other categories. In other words, here go commands that anyone can use!"""

	def __init__(self, bot):
		self.bot = bot

	#---PING---#
	@commands.command(aliases=["p"])
	async def ping(self, ctx):
		"""Check the speed of me!"""
		current_time = int(round(time.time() * 1000))
		m = await ctx.send("Pong! ---ms")
		last_time = int(round(time.time() * 1000))
		last_time -= current_time
		await m.edit(content="Pong! {}ms".format(last_time))

	#---SUGGEST---#
	@commands.command()
	async def suggest(self, ctx, *, suggestion):
		"""Suggest something to the owner!
		
		Parameters:
			suggestion - What you suggest goes here. It will be sent to the owner *pronto*!"""
		suggch = self.bot.get_channel(454695415611260928)
		embed_suggest = discord.Embed(title=ctx.author.name, description=ctx.author.id, color=0x00FF00).set_thumbnail(url=ctx.author.avatar_url)
		embed_suggest.add_field(name=ctx.guild.name, value=ctx.guild.id, inline=False)
		embed_suggest.add_field(name="Suggestion", value=suggestion, inline=False)
		await suggch.send(embed=embed_suggest)

	#---GOOGLE---#
	@commands.command(hidden=True, aliases=["search", "g"])
	async def google(self, ctx, *, msg):
		"""Google something!
		
		Parameters:
			msg - The content to google."""
		rawmsg = "+".join(msg.split(" "))
		await ctx.send(embed=discord.Embed(title="Google Search", description=f"Search Content: {msg}\nClick [here](https://www.google.com/search?q={rawmsg}) to access your generated link.", color=int(hashlib.md5(msg.encode('utf-8')).hexdigest()[:6], 16)))

	#---USERSTATS---#
	@commands.command(aliases=["uinfo", "ustats"])
	async def userstats(self, ctx, user: discord.Member):
		"""Shows information about the mentioned user!
		
		Parameters:
			user - The user to get the statuses from. The user must be mentioned."""
		if user == None:
			await ctx.send("Please mention someone!")
		else:
			roles = user.roles
			printedRoles = []
			for role in roles:
				if role.name == "@everyone":
					printedRoles.append("@everyone")
				else:
					printedRoles.append("<@&{}>".format(role.id))
			createDate = user.created_at
			joinDate = user.joined_at
			rolesStr = ", ".join(printedRoles)
			memActivity = user.activity.name if user.activity is not None else "None"
			embed_userstats = discord.Embed(title="User Statistics", description=f"This embed will show some basic information about {user}!", color=0x0000FF)
			embed_userstats.set_thumbnail(url=user.avatar_url)
			embed_userstats.add_field(name="Username", value=user.display_name, inline=False)
			embed_userstats.add_field(name="ID", value=user.id, inline=False)
			embed_userstats.add_field(name="Nickname", value=user.nick, inline=False)
			embed_userstats.add_field(name="Activity", value=memActivity, inline=False)
			embed_userstats.add_field(name="Roles", value=rolesStr, inline=False)
			embed_userstats.add_field(name="Date of Account Creation", value=createDate.strftime("%A, %d. %B %Y %H:%M"), inline=False)
			embed_userstats.add_field(name="Date of Guild Join", value=joinDate.strftime("%A, %d. %B %Y %H:%M"), inline=False)
			await ctx.send(embed=embed_userstats)

	#---ABOUT---#
	@commands.command()
	async def about(self, ctx):
		"""Something about me!"""
		botOwner = await self.bot.get_user_info(user_id=ownerID)
		embed_about = discord.Embed(title="About", description=f"This embed will showcase all the information about {self.bot.user}!", color=0x00FF00)
		embed_about.add_field(name="Username", value=self.bot.user.name, inline=False)
		embed_about.add_field(name="ID", value=self.bot.user.id, inline=False)
		embed_about.add_field(name="Discriminator", value=self.bot.user.discriminator, inline=False)
		embed_about.add_field(name="Library Version", value=discord.__version__, inline=False)
		embed_about.add_field(name="My Owner", value=botOwner.name, inline=False)
		embed_about.add_field(name="Number of servers I run in", value=len(self.bot.guilds), inline=False)
		await ctx.send(embed=embed_about)


def setup(bot):
	bot.add_cog(Utility(bot))
