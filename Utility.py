from discord.ext import commands
import discord
import time
import hashlib
import names
from faker import Faker
from samp_client.client import SampClient
fake = Faker()

address = "23.94.75.34"
port = 7797

with SampClient(address=address, port=port) as client:
    serverinfo = client.get_server_info()


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)

ownerID = 255802794244571136


class Utility:
    """This category is all about any kind of commands that couldn't fit in other categories. In other words, here go commands that anyone can use!"""

    def __init__(self, bot):
        self.bot = bot

    #---DIY <3---#
    @commands.command(aliases=["diy"])
    async def diytech(self, ctx):
        """Join the DIY Tech server!"""
        owner = await self.bot.get_user_info(user_id=ownerID)
        embed_diy = discord.Embed(title="DIY Tech", description="DIY Tech is a server dedicated to the assistance of all users that may experience any kind of technology related problems. They can help you with coding, setting up your new PC, software errors and beyond! The server has a custom invite link too, since it's partnered with Discord.", color=0x00FFFF)
        embed_diy.add_field(name="Want to join?", value="Simply click [here](http://discordapp.com/invite/diytech) to join the server!")
        embed_diy.add_field(name="Why should I join?", value="As the server name suggests (and it has been explained already), the server is dedicated to help users with their tech questions and problems! However, you don't *have* to have a question or problem - just goof around in the off-topic and meme channels!")
        embed_diy.add_field(name="How big is the server?", value="The server has hit 3k recently, however, the number of users has fallen again. We're still around 3000 members, however!")
        embed_diy.add_field(name="Anything else you should know?", value="As per usual, please read the rules and info, feel free to ask staff any questions and enjoy your stay!")
        embed_diy.set_footer(text="Permission for this embed was given by Robben.")
        embed_diy.set_author(name="CritZ#7054", icon_url=owner.avatar_url)
        await esay(ctx, embed_diy)

    def is_correct_server(ctx):
        return ctx.guild.id == 475902932190101504

    #---SERVERINFO---#
    @commands.command()
    @commands.check(is_correct_server)
    async def serverinfo(self, ctx):
        """Get the info of the SA:MP server Los Santos Gaming!"""
        embed_info = discord.Embed(title="Server Info", description=f"Some server information about {serverinfo.hostname} !", color=0x00FF00)
        embed_info.set_thumbnail(url=ctx.guild.icon_url)
        embed_info.add_field(name="IP", value=f"{address}:{port}")
        embed_info.add_field(name="Gamemode", value=serverinfo.gamemode)
        embed_info.add_field(name="Max Player Count", value=serverinfo.max_players)
        embed_info.add_field(name="Current Player Count", value=serverinfo.players)
        await esay(ctx, embed_info)

    #---PING---#
    @commands.command(aliases=["p"])
    async def ping(self, ctx):
        """Check the speed of me!"""
        current_time = int(round(time.time() * 1000))
        m = await say(ctx, "Pong! ---ms")
        last_time = int(round(time.time() * 1000))
        last_time -= current_time
        await m.edit(content="Pong! {}ms".format(last_time))

    #---SUGGEST---#
    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        """Suggest something to the owner!

        Parameters:
          suggestion - What you suggest goes here. It will be sent to the owner *pronto*!"""
        suggch = self.bot.get_channel(480052144938942465)
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
        await esay(ctx, embed=discord.Embed(title="Google Search", description=f"Search Content: {msg}\nClick [here](https://www.google.com/search?q={rawmsg}) to access your generated link.", color=int(hashlib.md5(msg.encode('utf-8')).hexdigest()[:6], 16)))

    #---NAME GENERATOR---#
    @commands.command(aliases=["ng"])
    async def namegen(self, ctx):
        """Generate a 'fake' name!

        Parameters:
          gender - The gender to use. Only correct inputs are 'Male' and 'Female', case sensitive! Defaults to None, which makes the name be at random gender."""
        genname = names.get_full_name()
        await say(ctx, f":abc: - Your generated name is ``{genname}``! They live at ``{fake.address()}``.")

    #---USERSTATS---#
    @commands.command(aliases=["uinfo", "ustats"])
    async def userstats(self, ctx, *, user):
        """Shows information about the mentioned user!

        Parameters:
          user - The user to get the statuses from. The user can get identified using mentions, IDs or names."""
        try:
            converter = commands.MemberConverter()
            user = await converter.convert(ctx, user)
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
            embed_userstats = discord.Embed(title="User Statistics", description=f"This embed will show some general and guild information about {user}!", color=0x0000FF)
            embed_userstats.set_thumbnail(url=user.avatar_url)
            embed_userstats.add_field(name="Username", value=user.display_name, inline=False)
            embed_userstats.add_field(name="ID", value=user.id, inline=False)
            embed_userstats.add_field(name="Nickname", value=user.nick, inline=False)
            embed_userstats.add_field(name="Activity", value=memActivity, inline=False)
            embed_userstats.add_field(name="Roles", value=rolesStr, inline=False)
            embed_userstats.add_field(name="Date of Account Creation", value=createDate.strftime("%A, %d. %B %Y %H:%M"), inline=False)
            embed_userstats.add_field(name="Date of Guild Join", value=joinDate.strftime("%A, %d. %B %Y %H:%M"), inline=False)
            await esay(ctx, embed_userstats)
        except commands.CommandError:
            if user.isdigit():
                user = await self.bot.get_user_info(user_id=user)
                createDate = user.created_at
                embed_userstats_out = discord.Embed(title="User Statistics", description=f"{user} has not been found inside of the current guild, which means that the global user list has been used to identify the user. The data this instance can deliver is limited.", color=0x0000FF)
                embed_userstats_out.set_thumbnail(url=user.avatar_url)
                embed_userstats_out.add_field(name="Username#Discriminator", value=user)
                embed_userstats_out.add_field(name="ID", value=user.id)
                embed_userstats_out.add_field(name="Date of Account Creation", value=createDate.strftime("%A, %d. %B %Y %H:%M"))
                await esay(ctx, embed_userstats_out)
            else:
                await say(ctx, ":interrobang: - The given information hasn't resulted a guild member. If your intention is to get an User, please use a valid ID!")

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
        embed_about.add_field(name="My Owner", value=f"{botOwner} - {botOwner.id}", inline=False)
        await esay(ctx, embed_about)


def setup(bot):
    bot.add_cog(Utility(bot))
