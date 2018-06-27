from discord.ext import commands
import discord

ownerID = 255802794244571136


class Developer:
	"""This module is about commands getting tested. Please don't use these, as the bot will be unstable with them until they work the way the bot owner wants them to."""
	
	def __init__(self, bot):
		self.bot = bot


def setup(bot):
	bot.add_cog(Developer(bot))
