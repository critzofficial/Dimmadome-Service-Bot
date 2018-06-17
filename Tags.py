from discord.ext import commands
import discord
import fs
import os

class Tags:
	"""This category is all about the tag commands.
	
	The tag commands are an easy way to save links, text, memes or what not inside of the bot. They will be saved permanently, until you decide to delete them.
	
	Sometimes though, your tags can be deleted by the owner. This is mostly the cause if your tag is found to contain sexual nudity, harrasment of other users, illegal links or anything else that might conflict with the Discord ToS. In that case, your tag will be deleted manually by the bot owner and removed from your list.
	
	This command has a few difficulties, however. It can't save emojis, direct file uploads or any kind of special characters. Please refrain from inserting anything that is not inside of the English and/or Germany keyboard layout, as it may cause problems!
	
	(Original tag idea by R. Danny's bot)"""
	
	def __init__(self, bot):
		self.bot = bot
		
	#---TAG---#
	@commands.command(description="Reads the content of a tag and posts it directly into chat. Tags can be created using the \"tcreate\" tag.")
	async def t(self, ctx, *, name):
		"""Check what a tag says!"""
		if fs.exists(f"../DSB_Files/{name}.txt"):
			with open(f"../DSB_Files/{name}.txt", "r") as file:
				msg = file.read()
			await ctx.send(msg)
		else:
			await ctx.send(":interrobang: - Invalid tag!")

	#---CREATE---#
	@commands.command(description="Used to make a file inside of the owner's PC and save the tag name, along with the value, there. Tags will only be changed or deleted by the owner if they contain sexual or otherwise inappropriate content.")
	async def tcreate(self, ctx, name, *, value):
		"""Create your own tag!"""
		if fs.exists(f"../DSB_Files/{name}.txt"):
			await ctx.send(":interrobang: - The tag name is already occupied!")
		else:
			fs.write(f"../DSB_Files/{name}.txt", value)
			if fs.exists(f"../DSB_Files/tags_by_{ctx.author.id}.txt"):
				fs.append(f"../DSB_Files/tags_by_{ctx.author.id}.txt", f"\n{name}")
			else:
				fs.write(f"../DSB_Files/tags_by_{ctx.author.id}.txt", name)
			await ctx.send(":white_check_mark: - Tag created!")
			
	#---EDIT---#
	@commands.command(description="Edits one of the tags you own. This command directly checks for the tag inside of the storage and checks if it's yours. If it isn't you can't access it. If it is, though, you can save whatever you want in it.")
	async def tedit(self, ctx, name, *, value):
		"""Edit your own tags!"""
		if not fs.exists(f"../DSB_Files/{name}.txt"):
			await ctx.send(":interrobang: - Tag name invalid!")
		else:
			with open(f"../DSB_Files/tags_by_{ctx.author.id}.txt", "r") as file:
				usTags = file.read()
			if not name in usTags:
				await ctx.send(":interrobang: - You don't own this tag!")
			else:
				fs.write(f"../DSB_Files/{name}.txt", value)
				await ctx.send(":white_check_mark: - Edit successful!")
				
	#---DELETE---#
	@commands.command(description="Deletes a tag that you own. Simple, huh?", aliases=["tdelete"])
	async def tdel(self, ctx, name):
		"""Delete one of your tags, or more."""
		if fs.exists(f"../DSB_Files/tags_by_{ctx.author.id}.txt"):
			if fs.exists(f"../DSB_Files/{name}.txt"):
				with open(f"../DSB_Files/tags_by_{ctx.author.id}.txt", "r") as file:
					tags = file.read()
				if name in tags:
					os.remove(f"../DSB_Files/{name}.txt")
					tags = tags.replace(f"\n{name}", "")
					fs.write(f"../DSB_Files/tags_by_{ctx.author.id}.txt", str(tags))
					await ctx.send(":white_check_mark: - Tag Deleted!")
				else:
					await ctx.send(":interrobang: - You don't own this tag!")
			else:
				await ctx.send(":interrobang: - Invalid tag name! Are the letters properly uppercased and lowercased?")
		else:
			await ctx.send(":interrobang: - You don't even own tags!")
			
	#---MYTAGS---#
	@commands.command()
	async def mytags(self, ctx):
		"""Check which tags you own again!"""
		if fs.exists(f"../DSB_Files/tags_by_{ctx.author.id}.txt"):
			with open(f"../DSB_Files/tags_by_{ctx.author.id}.txt", "r") as file:
				tags = file.read()
			await ctx.send(f":white_check_mark: - {ctx.author.mention} , your tags are:\n``{tags}``")

def setup(bot):
	bot.add_cog(Tags(bot))
