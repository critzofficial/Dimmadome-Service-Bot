from discord.ext import commands
import discord
import random
import time
import hashlib

ownerID = 255802794244571136

class Utility:

    def __init__(self, bot):
        self.bot = bot

    #---SAY---#
    @commands.command(description="Repeats the said words in chat. What can I say more but that?")
    async def say(self, ctx, *, msg):
        """Makes the bot say something!"""
        await ctx.send(msg)

    #---RAND---#
    @commands.command(description="Gives a round number between the first and the second number. Simple, eh?")
    async def rand(self, ctx, num1, num2):
        """Randomizes 2 numbers!"""
        try:
            numproduced = random.randint(int(num1), int(num2))
            await ctx.send(f"Your number is {numproduced} !")
        except Exception as e:
            await ctx.send(f"```Oops, an error has been raised!\nThe error is: {e.__class__.__name__}: {e}```")

    #---DICE---#
    @commands.command()
    async def dice(self, ctx):
        """Roll a dice!"""
        await ctx.send(f":1234: - You rolled a {random.randint(1, 6)}!")
    
    #---PING---#
    @commands.command(description="Checks the latency of the bot in 'ms'. The lower the latency, the faster the bot replies on commands.")
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
        """Suggest something to the owner!"""
        suggch = self.bot.get_channel(454695415611260928)
        await suggch.send(f"{ctx.author.name} ``{ctx.author.id}`` from {ctx.guild.name} ``{ctx.guild.id}`` suggested: ``{suggestion}``")

    #---GOOGLE---#
    @commands.command(description="This app doesn't use any Google API. Instead, it just adds the keywords to the link.")
    async def google(self, ctx, *, msg):
        """Google something!"""
        rawmsg = "+".join(msg.split(" "))
        await ctx.send(embed=discord.Embed(title="Google Search", description=f"Search Content: {msg}\nClick [here](https://www.google.com/search?q={rawmsg}) to access your generated link.", color=int(hashlib.md5(msg.encode('utf-8')).hexdigest()[:6], 16)))

    #---ASKTHE8BALL---#
    @commands.command(description="A simple randomizer of words. Nothing more to it.")
    async def askthe8ball(self, ctx):
        """Ask the 8-ball!"""
        eightball = [
            "Yes",
            "As I see it, yes",
            "Outlook good",
            "Concentrate and ask again",
            "Better not tell you now",
            "Don't count on it",
            "Very doubtful",
            "No"
        ]
        eightballsays = random.randint(1, 9)
        await ctx.send(eightball[eightballsays - 1])
    
    #---USERSTATS---#
    @commands.command(description="Shows information, as the roles, date of when the user joined the server, date when the account got created as well as other basic information.")
    async def userstats(self, ctx, user: discord.Member=None):
        """Shows information about the mentioned user!"""
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
            if user.activity:
                memActivity = user.activity.name
            elif not user.activity:
                memActivity = "None"
            embed_userstats = discord.Embed(title="User Statistics", description=f"This embed will show some basic information about {user}!", color=0x0000FF)
            embed_userstats.add_field(name="Username", value=user.display_name, inline=False)
            embed_userstats.add_field(name="ID", value=user.id, inline=False)
            embed_userstats.add_field(name="Nickname", value=user.nick, inline=False)
            embed_userstats.add_field(name="Activity", value=memActivity, inline=False)
            embed_userstats.add_field(name="Roles", value=rolesStr, inline=False)
            embed_userstats.add_field(name="Date of Account Creation", value=createDate.strftime("%A, %d. %B %Y %H:%M"), inline=False)
            embed_userstats.add_field(name="Date of Guild Join", value=joinDate.strftime("%A, %d. %B %Y %H:%M"), inline=False)
            await ctx.send(embed=embed_userstats)

    #---ABOUT---#
    @commands.command(description="Names a few details about the bot... That's it.")
    async def about(self, ctx):
        """Something about me!"""
        botOwner = await self.bot.get_user_info(user_id=ownerID)
        numOfMembers = 0
        embed_about = discord.Embed(title="About", description=f"This embed will showcase all the information about {self.bot.user}!", color=0x00FF00)
        embed_about.add_field(name="Username", value=self.bot.user.name, inline=False)
        embed_about.add_field(name="ID", value=self.bot.user.id, inline=False)
        embed_about.add_field(name="Discriminator", value=self.bot.user.discriminator, inline=False)
        embed_about.add_field(name="Library Version", value=discord.__version__, inline=False)
        embed_about.add_field(name="My Owner", value=botOwner.name, inline=False)
        embed_about.add_field(name="Number of servers I run in", value=len(self.bot.guilds), inline=False)
        for guild in self.bot.guilds:
            numOfMembers += len(guild.members)
        embed_about.add_field(name="Number of members I serve in total", value=numOfMembers, inline=False)
        await ctx.send(embed=embed_about)

def setup(bot):
    bot.add_cog(Utility(bot))