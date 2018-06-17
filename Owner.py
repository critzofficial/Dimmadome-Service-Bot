from discord.ext import commands
import discord
import textwrap
import traceback

ownerID = 255802794244571136

class Owner:
	"""This category is all about the commands made specially for the owner of the bot, Jamison Fawkes#7054. You can have a look, but you can also simply ignore them."""

	def __init__(self, bot):
		self.bot = bot


	#---ODISMISS---#
	@commands.command(description="Makes the bot leave the server. This is the owner variant.\nRequired permissions: bot ownership", aliases=["getout"])
	@commands.is_owner()
	async def odismiss(self, ctx):
		"""Make me leave. :["""
		await ctx.guild.leave()

	#---EVAL---#
	@commands.command(description="Okay, fine. This fine command runs anything the bot owner wants it to run. Of course, only the bot owner can use it. :)", aliases=["run", "exec"])
	@commands.is_owner()
	async def eval(self, ctx, *, body):
		"""Do I have to explain?"""
		to_exec = textwrap.indent(body, "  ")
		try:
			exec(f"async def func(ctx):\n\t{to_exec}", globals())
			await func(ctx)
		except Exception as e:
			await ctx.send(f"```{e.__class__.__name__}: {e}```")

	#---QUIT---#
	@commands.command(description="Logs the bot out of discord.\nRequired permissions: Bot ownership")
	@commands.is_owner()
	async def quit(self, ctx):
		"""Logs out of discord."""
		await ctx.send("Shutting down...")
		await self.bot.logout()

	#---OSAY---#
	@commands.command(description="Repeats word after word.\nRequired permissions: Bot ownership")
	@commands.is_owner()
	async def osay(self, ctx, *, msg):
		"""Say something."""
		await ctx.send(msg)

	#---OPM---#
	@commands.command(description="The target must be mentioned.\nRequired permissions: Bot ownership", aliases=["pm"])
	@commands.is_owner()
	async def opm(self, ctx, mention: discord.Member=None, *, msg):
		"""Make the bot PM someone."""
		if mention == None:
			await ctx.send("You didn't mention anyone!")
		else:
			await mention.send(msg)

def setup(bot):
	bot.add_cog(Owner(bot))
