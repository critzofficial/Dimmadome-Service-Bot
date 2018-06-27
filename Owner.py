from discord.ext import commands
import discord
import textwrap

ownerID = 255802794244571136


class Owner:
	"""This category is all about the commands made specially for the owner of the bot, Dr. Heinz Doofenshmirtz. You can have a look, but you can also simply ignore them."""

	def __init__(self, bot):
		self.bot = bot

	#---EVAL---#
	@commands.command(aliases=["run", "exec"])
	@commands.is_owner()
	async def eval(self, ctx, *, body):
		"""Run any quick command.
		
		Parameters:
			body - The code to execute.
			
		Requirements:
			Bot ownership"""
		to_exec = textwrap.indent(body, "  ")
		try:
			exec(f"async def func(ctx):\n\t{to_exec}", globals())
			await func(ctx)
		except Exception as e:
			await ctx.send(f"```{e.__class__.__name__}: {e}```")

	#---QUIT---#
	@commands.command()
	@commands.is_owner()
	async def quit(self, ctx):
		"""Logs out of discord.
		
		Requirements:
			Bot ownership"""
		await ctx.send("Shutting down...")
		await self.bot.logout()


def setup(bot):
	bot.add_cog(Owner(bot))
