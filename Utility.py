from discord.ext import commands
import discord
import time
import hashlib


async def say(ctx, cont: str):
    return await ctx.send(cont)


async def esay(ctx, embed: discord.Embed):
    return await ctx.send(embed=embed)

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
        await esay(ctx, embed=discord.Embed(title="Google Search", description=f"Search Content: {msg}\nClick [here](https://www.google.com/search?q={rawmsg}) to access your generated link.", color=int(hashlib.md5(msg.encode('utf-8')).hexdigest()[:6], 16)))

    #---USERSTATS---#
    @commands.command(aliases=["uinfo", "ustats"])
    async def userstats(self, ctx, *, user: int):
        """Shows information about the mentioned user!

        Parameters:
            user - The user to get the statuses from. The user must be mentioned."""
        def infogather():
            is_in_guild = False
            for guser in ctx.guild.members:
                if guser.id == user:
                    is_in_guild = True
                    break
                else:
                    continue
            if is_in_guild:
                print("True!")
                return True
            else:
                print("False...")
                return False
        x = infogather()
        if x:
            user = ctx.guild.get_member(user)
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
        else:
            user = self.bot.get_user_info(user_id=user)
            createDate = user.created_at
            embed_userstats_out = discord.Embed(title="User Statistics", description=f"{user} has not been found inside of the current guild, which means the data this command can deliver is limited.", color=0x0000FF)
            #embed_userstats_out.add_thumbnail(url=user.avatar_url)
            embed_userstats_out.add_field(name="Username#Discriminator", value=user)
            embed_userstats_out.add_field(name="ID", value=user.id)
            embed_userstats_out.add_field(name="Date of Account Creation", value=createDate.strftime("%A, %d. %B %Y %H:%M"))
            await esay(ctx, embed_userstats_out)

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
        await esay(ctx, embed_about)


def setup(bot):
    bot.add_cog(Utility(bot))
