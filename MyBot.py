# coding=utf-8
#from typing import List

import logging
import discord
import sys
import random
import time
import asyncio
import fs
from datetime import datetime
import os
from samp_client.client import SampClient
with SampClient(address='23.94.75.34', port=7847) as client:
    srvinfo = client.get_server_info()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

logging.basicConfig(level=logging.ERROR)

ownerID = 255802794244571136
botID = 269533424916627457
Robben = 351077471241764876

p = "DD!"

curse_list = ["fuck", "shit", "crap", "bitch", "nigga", "nigger", "fak", "shet", "sht", "fck"]


class MyClient(discord.Client):
    async def on_connect(self):
        print("Connecting...\n")
        game_name = "Connecting, please wait!"
        prebot_game = discord.Game(name=str(game_name))
        prebot_status = discord.Status("idle")
        await client.change_presence(activity=prebot_game, status=prebot_status)

    async def on_ready(self):
        print(f"Script loaded and ready to be used!\nName: {self.user}\nID: {self.user.id}\nDiscriminator: {self.user.discriminator}\n\nCurrently running on - {len(self.guilds)} - servers!\n")
        #for guild in self.guilds:
        #    print(f"Guild name: {guild.name} | Guild ID: {guild.id}")
        #game_name = "Bot under development"
        game_name = f"| {p}help |"
        bot_game = discord.Game(name=str(game_name))
        #bot_status = discord.Status("dnd")
        bot_status = discord.Status("online")
        await client.change_presence(activity=bot_game, status=bot_status)

    async def on_guild_join(self, guild):
        await guild.create_role(name="DSB Muted", permissions=discord.Permissions(permissions=66560), color=discord.Colour(value=0xFF0000), hoist=False, mentionable=False)

    async def on_member_join(self, member):
        if fs.exists(f"welc_ch_of_{member.guild.id}.txt"):
            if fs.exists(f"welc_msg_of_{member.guild.id}.txt"):
                with open(f"welc_ch_of_{member.guild.id}.txt") as file1:
                    chID = file1.read()
                channel = client.get_channel(int(chID))
                with open(f"welc_msg_of_{member.guild.id}.txt") as file2:
                    msg = file2.read()
                if "{USERNAME}" in msg:
                    msg = msg.replace("{USERNAME}", f"{member.name}")
                if "{USERID}" in msg:
                    msg = msg.replace("{USERID}", f"{member.id}")
                if "{MENTION}" in msg:
                    msg = msg.replace("{MENTION}", f"<@{member.id}>")
                if "{SRVNAME}" in msg:
                    msg = msg.replace("{SRVNAME}", f"{member.guild.name}")
                await channel.send(msg)

    async def on_message(self, message):
        global memActivity, log_channel
        channel = message.channel

        if not message.author.bot:

            #Log Check
            try:
                file = open(f"log_of_{message.guild.id}.txt", "r+")
                logID = file.read()
                log_channel = self.get_channel(int(logID))
            except:
                log_channel = message.channel

            #Curse Check
            if any(x in curse_list for x in message.content.split(" ")):
                if fs.exists(f"cfil_of_{message.guild.id}.txt"):
                    with open(f"cfil_of_{message.guild.id}.txt", "r+") as file:
                        cfilsetting = int(file.read())
                    if cfilsetting == 1:
                        await message.delete()
                        await channel.send(f"<@{message.author.id}> , please don't swear!")
                    else:
                        pass

            #About Command
            if message.content == f"{p}about":
                numOfMembers = 0
                numOfMembersToReduce = len(client.get_guild(264445053596991498).members)
                embed_about = discord.Embed(title="About", description=f"This embed will showcase all the information about {self.user}!", color=0x00FF00)
                embed_about.add_field(name="Username", value=self.user, inline=False)
                embed_about.add_field(name="ID", value=self.user.id, inline=False)
                embed_about.add_field(name="Discriminator", value=self.user.discriminator, inline=False)
                embed_about.add_field(name="Library Version", value=discord.__version__, inline=False)
                embed_about.add_field(name="My Owner", value=await client.get_user_info(user_id=ownerID), inline=False)
                embed_about.add_field(name="Number of servers I run in", value=len(client.guilds), inline=False)
                for guild in client.guilds:
                    numOfMembers += len(guild.members)
                embed_about.add_field(name="Number of members I serve in total (not including DiscordBots)", value=numOfMembers - numOfMembersToReduce, inline=False)
                await channel.send(embed=embed_about)

            #Rules Command
            #This one is undocumented inside of the help command, because it's for special use of the Support server.
            if message.content == f"{p}rules":
                if message.author.id == ownerID:
                    await message.delete()
                    embed_rules = discord.Embed(title="Rules of the DSB Support server.", description="Please note that these rules ONLY apply in the DSB Support server! Rules in other servers are not based off of these rules, or vice versa.", color=0x00FFFF)
                    embed_rules.add_field(name="1) No excessive cursing/insulting", value="We understand that some people can have bad days and have to steam off somewhere, but this server is *NOT* made for that. If you are found by one of the admins to curse in an extreme ammount or are insulting other members (directly or indirectly), you will be punished. Punishments vary from a simple mute to a ban from the server. Watch your tongue!")
                    embed_rules.add_field(name="2) No racism", value="Even as a joke, any kind of racist acts are strictly prohobited and will be punished with a ban. Talking about racism is okay (mistakes while talking about it are forgiven once), but directly being racist will lead to direct punishment, no excuse.")
                    embed_rules.add_field(name="3) No advertising", value="This server has a strict policy against absolutely NO ADVERTISING. Whoever is found to do so intentionally will be directly banned. If you'd like to make sure any links you want to post are NOT counting as advertisement, consult one of our Staff members!")
                    embed_rules.add_field(name="4) No spamming", value="Here counts everything that might flood the chat with unnecessary content. Always stick to the topic! Spamming in chat will result in a mute, spamming in private messages will result in a kick/ban!")
                    embed_rules.add_field(name="5) No mass pinging", value="Under 'mass pinging', we count unnecessary mentioning of 4+ users. Anyone caught will get muted.")
                    embed_rules.add_field(name="6) Privacy", value=f"This server puts privacy at the front of everything. We'd kindly ask everyone to **NEVER** give out any kind of personal information, not even when staff members ask to. If they do, and threaten you with punishments if you don't listen to them, instantly message <@{ownerID}> and hold your ground. If the report is found to be true, the abuser will instantly get banned from the server and you will be rewarded. If it's false, however, you will be punished for false reporting with a warn. **Only share your personal information if you know what the consequences are.**")
                    await channel.send(embed=embed_rules)

            #Enable/Disable Curse Filter
            if message.content.startswith(f"{p}cursefil"):
                if message.author.guild_permissions.administrator:
                    if "0" in message.content[len(f"{p}cursefil "):] or "1" in message.content[len(f"{p}cursefil "):]:
                        if not fs.exists(f"cfil_of_{message.guild.id}.txt"):
                            fs.write(f"cfil_of_{message.guild.id}.txt", "0")
                        fs.write(f"cfil_of_{message.guild.id}.txt", message.content[len(f"{p}cursefil "):])
                        await channel.send(":white_check_mark: - Settings saved!")
                    else:
                        await channel.send(":interrobang: - Input wrong!")
                else:
                    await channel.send(":interrobang: - You do not have permission to use this command!")

            #New Username
            if message.content.startswith(f"{p}newname"):
                if message.author.id == ownerID:
                    numb = len(p + "newname")
                    newUsername = message.content[numb:]
                    await message.delete()
                    await self.user.edit(username=str(newUsername))
                    await channel.send(f"My name is now set to ``{newUsername}``!")

            #Dimmadab
            if message.content == f"{p}dimmadone":
                dab = discord.File("C:/Users/CritZ/Pictures/dab.jpg")
                await channel.send("I'm dimmadone with all these haters.", file=dab)

            #Special SAMP Command
            if message.content == f"{p}server":
                embed_server_color = 0xff8000
                vAAssassins = client.get_guild(424073177329565696)
                embed_server = discord.Embed(description=f"**Server Info**", colour=embed_server_color).set_thumbnail(url=vAAssassins.icon_url).add_field(name="Server Name", value=srvinfo.hostname, inline=False).add_field(name="Host IP", value="23.94.75.34:7847", inline=False).add_field(name="Server Language", value=srvinfo.language, inline=False).add_field(name="Server Gamemode", value=srvinfo.gamemode, inline=False).add_field(name="Max Players", value=srvinfo.max_players, inline=False).add_field(name="Current Players", value=srvinfo.players, inline=False)
                await channel.send(embed=embed_server)

            #Time Command
            if message.content == f"{p}time":
                tn = datetime.now()
                await channel.send(tn.strftime("Today is the %dth of %A, %Y. The bot's local time is %I:%M %p."))

            #Log Channel Command
            if message.content.startswith(f"{p}setlog"):
                if message.author.guild_permissions.administrator or message.author.id == ownerID:
                    if len(message.content[len(f"{p}setlog "):]) > 0:
                        if message.content.split()[1].isdigit():
                            if not fs.exists(f"log_of_{message.guild.id}.txt"):
                                fs.write(f"log_of_{message.guild.id}.txt", "none")
                            fs.write(f"log_of_{message.guild.id}.txt", message.content.split()[1])
                            await channel.send(":white_check_mark: - Log Channel set!")
                        elif message.content.split()[1].startswith("<#"):
                            chanID = message.content[len(p + "setlog <#"):-1]
                            if not fs.exists(f"log_of_{message.guild.id}.txt"):
                                fs.write(f"log_of_{message.guild.id}.txt", "none")
                            fs.write(f"log_of_{message.guild.id}.txt", "".join(chanID))
                            await channel.send(":white_check_mark: - Log Channel set!")
                        else:
                            await channel.send(":interrobang: - The input is not right!")
                    else:
                        if fs.exists(f"log_of_{message.guild.id}.txt"):
                            os.remove(f"log_of_{message.guild.id}.txt")
                        await channel.send(":exclamation: - Log channel reset!")
                else:
                    await channel.send("I'm sorry, but only users with the ``administrator`` permissions may use this command! Make sure to call your owner or anyone else who can use this to set it.")

            #Mute Command
            if message.content.startswith(f"{p}mute"):
                if message.author.guild_permissions.manage_roles or message.author.guild_permissions.administrator or message.author.id == ownerID:
                    if len(message.mentions) > 0:
                        muteTarget = message.mentions[0]
                    else:
                        muteTarget = message.guild.get_member(int(message.content.split(" ")[1]))
                    isAlreadyMuted = False
                    for role in muteTarget.roles:
                        if role.name == "DSB Muted":
                            isAlreadyMuted = True
                            break
                    if not isAlreadyMuted:
                        if muteTarget.id == ownerID:
                            await channel.send(":exclamation: - Hey, you can't mute my owner!")
                        else:
                            roles = [mutedRole for mutedRole in message.guild.roles if mutedRole.name == "DSB Muted"]
                            if len(roles) < 1:
                                await channel.send(":interrobang: - There was an error muting the target. The role does not even exist!\nIf you are the owner of this server, please add the following role: ``DSB Muted`` and restrict anyone to send messages in the channels you choose!")
                            else:
                                await muteTarget.add_roles(roles[0])
                                if len(message.content.split()[2:]) > 0:
                                    reason = " ".join(message.content.split()[2:])
                                else:
                                    reason = "No reason provided."
                                await muteTarget.add_roles(roles[0])
                                await channel.send(embed=discord.Embed(title="User Muted", description=f"The user {muteTarget.name} has been successfully muted!", color=0xFFFF00))
                                embed_mute_color = 0xFFFF00
                                embed_mute = discord.Embed(title="Admin Log: Mute", description=f"A mute has been issued on {muteTarget.name}", colour=embed_mute_color).add_field(name="Admin", value=message.author.name).add_field(name="Muted Member", value=muteTarget.name).add_field(name="Reason", value=reason, inline=False)
                                await log_channel.send(embed=embed_mute)
                    else:
                        await channel.send(":interrobang: - This user is already muted once!")
                else:
                    await channel.send(":interrobang: - Hey, you can't use this!")

            #Unmute Command
            if message.content.startswith(f"{p}unmute"):
                if message.author.guild_permissions.manage_roles or message.author.guild_permissions.administrator or message.author.id == ownerID:
                    if len(message.mentions) > 0:
                        unmuteTarget = message.mentions[0]
                    else:
                        unmuteTarget = message.guild.get_member(int(message.content.split(" ")[1]))
                    isMuted = False
                    for role in unmuteTarget.roles:
                        if role.name == "DSB Muted":
                            isMuted = True
                            break
                    if isMuted:
                        roles = [mutedRole for mutedRole in message.guild.roles if mutedRole.name == "DSB Muted"]
                        if len(roles) < 1:
                            await channel.send(":interrobang: - There was an error unmuting the target. The role does not even exist!")
                        else:
                            if len(message.content.split()[2:]) > 0:
                                reason = " ".join(message.content.split()[2:])
                            else:
                                reason = "No reason provided."
                            await unmuteTarget.remove_roles(roles[0])
                            await channel.send(embed=discord.Embed(title="User Unmuted", description=f"The user {unmuteTarget.name} has been successfully unmuted!", color=0xFFFF00))
                            embed_unmute_color = 0x00FF00
                            embed_unmute = discord.Embed(title="Admin Log: Unmute", description=f"An unmute has been issued on {unmuteTarget.name}", colour=embed_unmute_color).add_field(name="Admin", value=message.author.name).add_field(name="Unmuted Member", value=unmuteTarget.name).add_field(name="Reason", value=reason, inline=False)
                            await log_channel.send(embed=embed_unmute)
                    if not isMuted:
                        await channel.send(":interrobang: - This user isn't muted!")
                else:
                    await channel.send(":interrobang: - Hey, you can't use this!")

            #Unwarn Command
            if message.content.startswith(f"{p}unwarn"):
                if message.author.guild_permissions.kick_members or message.author.guild_permissions.administrator:
                    if len(message.mentions) > 0:
                        unwarnTarget = message.mentions[0]
                    else:
                        unwarnTarget = message.guild.get_member(message.content.split(" ")[1])
                    if not fs.exists(f"admin_warns_of_{unwarnTarget.id}.txt"):
                        await channel.send("The mentioned user has never been warned at all...!")
                    elif fs.exists(f"admin_warns_of_{unwarnTarget.id}.txt"):
                        with open(f"admin_warns_of_{unwarnTarget.id}.txt", "r+") as file:
                            warn = int(file.read())
                        if warn > 0:
                            fs.write(f"admin_warns_of_{unwarnTarget.id}.txt", "0")
                            await channel.send("User's warns have been cleaned!")
                            file.close()
                        elif warn == 0:
                            await channel.send("This user has no warnings, but the file is found.")
                else:
                    await channel.send("You do not have permission to execute this command!")

            #Warn Command
            if message.content.startswith(f"{p}warn"):
                if message.author.guild_permissions.kick_members or message.author.guild_permissions.administrator:
                    if len(message.mentions) > 0:
                        warnTarget = message.mentions[0]
                    else:
                        warnTarget = message.guild.get_member(message.content.split(" ")[1])
                    if not fs.exists(f"admin_warns_of_{warnTarget.id}.txt"):
                        fs.write(f"admin_warns_of_{warnTarget.id}.txt", "0")
                    with open(f"admin_warns_of_{warnTarget.id}.txt", "r+") as file:
                        warn = int(file.read())
                    if warn < 3:
                        warn += 1
                        await channel.send("Warn successful!")
                        fs.write(f"admin_warns_of_{warnTarget.id}.txt", str(warn))
                        file.close()
                    elif warn == 3:
                        if not fs.exists(f"ban_warns_of_{warnTarget.id}.txt"):
                            fs.write(f"ban_warns_of_{warnTarget.id}.txt", "0")
                        with open(f"ban_warns_of_{warnTarget.id}.txt", "r+") as banfile:
                            banwarns = banfile.read()
                        if banwarns < 2:
                            banwarns += 1
                            fs.write(f"ban_warns_of_{warnTarget.id}.txt", str(banwarns))
                            warn_kick_embed_color = 0xFFFF00
                            await warnTarget.kick(reason=f"The user has been warned by {message.author.name} and the warns have been exceeded.")
                            warn_kick_embed = discord.Embed(title="Admin Log: Member Kick", description=f"A kick has been issued on {warnTarget.name}", colour=warn_kick_embed_color).set_thumbnail(url=message.author.avatar_url).add_field(name="Admin", value=f"{message.author.name}").add_field(name="Kicked Member", value=f"{warnTarget.name}").add_field(name="Reason", value="Warns have been exceeded.")
                            await channel.send(embed=warn_kick_embed)
                        elif banwarns == 2:
                            warn_ban_embed_color = 0xFF0000
                            await warnTarget.ban(reason=f"The user has been warned by {message.author.name} and has been kicked too many times for exceeded warns.")
                            warn_ban_embed = discord.Embed(title="Admin Log: Member Ban", description=f"A ban has been issued on {warnTarget.name}", colour=warn_ban_embed_color).set_thumbnail(url=message.author.avatar_url).add_field(name="Admin", value=f"{message.author.name}").add_field(name="Banned Member", value=f"{warnTarget.name}").add_field(name="Reason", value="\"Ban\" warns have been exceeded.")
                            await channel.send(embed=warn_ban_embed)
                else:
                    await channel.send("You do not have permission to execute this command!")

            #@everyone Filter
            if not message.content.startswith(f"{p}osay"):
                if message.mention_everyone:
                    if message.author.guild_permissions.administrator or message.author.guild_permissions.kick_members or message.author.guild_permissions.ban_members or message.author.guild_permissions.manage_channels or message.author.guild_permissions.view_audit_log or message.author.guild_permissions.manage_guild or message.author.guild_permissions.manage_messages:
                        pass
                    else:
                        if not fs.exists(f"warns_of_{message.author.id}.txt"):
                            fs.write(f"warns_of_{message.author.id}.txt", "0")
                        with open('warns_of_{}.txt'.format(message.author.id), 'r+') as file:
                            warn = int(file.read())
                        if warn < 3:
                            warn += 1
                            await message.delete()
                            await channel.send(f"<@{message.author.id}> , please don't use ``@everyone``!")
                            fs.write(f"warns_of_{message.author.id}.txt", str(warn))
                            file.close()  # here
                        elif warn == 3:
                            await message.delete()
                            filterTargetName = message.author.name
                            await message.author.kick(reason="Filter Kick - Excessive use of \"@everyone\"")
                            filter_embed_color = 0xFFFF00
                            filter_embed = discord.Embed(title="Filter Kick", description=f"The bot has issued an automated kick on {filterTargetName}", colour=filter_embed_color).set_thumbnail(url=message.author.avatar_url).add_field(name="Kicked Member", value=str(filterTargetName)).add_field(name="Reason", value="Filter Kick - Excessive use of \"@everyone\"")
                            await log_channel.send(embed=filter_embed)

            #ID Command
            if message.content == f"{p}id":
                await channel.send("<@{0.id}> , your ID is \"{0.id}\"!".format(message.author))

            #Name Command
            if message.content.startswith(f"{p}name"):
                args = message.content.split()[1:]
                target = args[0]
                uName = message.guild.get_member(int(target))
                if not uName:
                    await channel.send(":interrobang: - Invalid ID!")
                else:
                    await channel.send(f":white_check_mark: - Your target's name is ``{uName.name}``!")

            #Say Command
            if message.content.startswith(f"{p}say"):
                await message.delete()
                if message.mention_everyone:
                    await channel.send("Please do not mention everyone, <@{}>!".format(message.author.id))
                else:
                    if len(message.content.split(" ")[1:]) != 0:
                        msg = message.content.split(" ")[1:]
                        await channel.send("{} said: {}".format(message.author.mention, " ".join(msg)))
                    else:
                        await channel.send("You didn't say anything!")

            #OSay Command
            if message.content.startswith(f"{p}osay"):
                has_forbidden_role = False
                await message.delete()
                for role in message.author.roles:
                    if role.id in [424104352920240140]:
                        has_forbidden_role = True
                        break
                    else:
                        continue
                if has_forbidden_role or message.author.id == ownerID:
                    if not message.mention_everyone:
                        msg = message.content.split(" ")[1:]
                        await channel.send(" ".join(msg))
                    else:
                        await channel.send("Please don't use ``@everyone``!")

            #OPM Command
            if message.content.startswith(f"{p}opm"):
                try:
                    await message.delete()
                    memberToPM = message.mentions[0]
                    messageToPM = message.content.split(" ")[2:]
                    await memberToPM.send(" ".join(messageToPM))
                except Exception as e:
                    await channel.send(f"An error was given: ``{e}``")
                    print(f"{memberToPM}\n{messageToPM}")

            #Rand Command
            if message.content.startswith(f"{p}rand"):
                number = message.content.split()[1]
                if number.isdigit():
                    randomized = random.uniform(1, int(number))
                    await channel.send("{}, your number is ``{}``!".format(message.author.mention, int(randomized)))
                elif not number.isdigit():
                    await channel.send("{}, please use numbers!".format(message.author.mention))

            #Dice Command
            if message.content == f"{p}dice":
                numberInt = int(random.uniform(1, 7))
                await channel.send(f"<@{message.author.id}> , you rolled a ``{numberInt}``!")

            #UserCount Command
            if message.content == f"{p}usercount":
                await channel.send("``{}`` members are on this server!".format(len(message.guild.members)))

            #Quit Command
            if message.content == f"{p}quit":
                if message.author.id == ownerID:
                    await channel.send("Shutting down...")
                    await client.logout()
                else:
                    await channel.send("You do not have permission to execute this command!")

            #Quick Quit Command
            if message.content == "q":
                if message.author.id == ownerID:
                    await client.logout()

            #UserStats Command
            if message.content.startswith(f"{p}userstats"):
                try:
                    if len(message.content.split()[1:]) != 0:
                        if len(message.mentions) > 0:
                            intendedMember = message.mentions[0]
                        else:
                            intendedMember = message.guild.get_member(int(message.content.split()[1:]))
                    else:
                        intendedMember = message.author
                    roles = intendedMember.roles
                    printedRoles = []
                    for role in roles:
                        if role.name == "@everyone":
                            printedRoles.append("@everyone")
                        else:
                            printedRoles.append("<@&{}>".format(role.id))
                    createDate = intendedMember.created_at
                    joinDate = intendedMember.joined_at
                    if intendedMember.activity:
                        memActivity = intendedMember.activity.name
                    elif not intendedMember.activity:
                        memActivity = "None"
                    if fs.exists(f"warns_of_{intendedMember.id}.txt"):
                        with open(f"warns_of_{intendedMember.id}.txt", "r+") as file1:
                            filter_warns = file1.read()
                    else:
                        filter_warns = "0"
                    if fs.exists(f"admin_warns_of_{intendedMember.id}.txt"):
                        with open(f"admin_warns_of_{intendedMember.id}.txt", "r+") as file2:
                            admin_warns = file2.read()
                    else:
                        admin_warns = "0"
                    if fs.exists(f"ban_warns_of_{intendedMember.id}.txt"):
                        with open(f"ban_warns_of_{intendedMember.id}.txt", "r+") as file3:
                            ban_warns = file3.read()
                    else:
                        ban_warns = "0"
                    embed_userstats_color = 0x0000FF
                    embed_userstats = discord.Embed(title="UserStats", description="Information about {}".format(intendedMember), colour=embed_userstats_color).set_thumbnail(url=intendedMember.avatar_url).set_footer(text="Please contact the owner of the bot if any information is wrong!").set_author(name="{}".format(message.author)).add_field(name="User's Status", value=str(intendedMember.status)).add_field(name="Username", value=intendedMember.name, inline=False).add_field(name="ID", value=intendedMember.id, inline=False).add_field(name="When the user joined this Guild", value=joinDate.strftime("%A, %d. %B %Y %H:%M"), inline=False).add_field(name="When the account was created", value=createDate.strftime("%A, %d. %B %Y %H:%M"), inline=False).add_field(name="Discriminator", value="#" + intendedMember.discriminator, inline=False).add_field(name="Nickname", value=intendedMember.nick).add_field(name="Activity", value=memActivity, inline=False).add_field(name="Member's roles", value=", ".join(printedRoles), inline=False).add_field(name="Filter Warns", value=filter_warns).add_field(name="Normal/Ban Warns", value=f"{admin_warns}/{ban_warns}")
                    await channel.send(embed=embed_userstats)
                except Exception as e:
                    await channel.send(f"<@{message.author.id}> , did you use a correct ID or mention? Your input is wrong!")
                    await channel.send(e)

            #Purge Command
            if message.content.startswith(f"{p}purge"):
                if message.author.id == ownerID or message.author.guild_permissions.manage_messages:
                    if message.content.split()[1].isdigit():
                        await message.delete()
                        purgeAmount = int(message.content.split()[1])
                        await channel.purge(limit=purgeAmount)
                        await asyncio.sleep(1)
                        await channel.send(":white_check_mark: - Messages purged!")
                    else:
                        await channel.send("Please use numbers!")
                else:
                    await channel.send("You do not have permission to execute this command!")

            #8ball Command
            if message.content.startswith(f"{p}8ball"):
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
                eightballsays = int(random.uniform(1, 9))
                if eightballsays == 1:
                    await channel.send(eightball[0])
                elif eightballsays == 2:
                    await channel.send(eightball[1])
                elif eightballsays == 3:
                    await channel.send(eightball[2])
                elif eightballsays == 4:
                    await channel.send(eightball[3])
                elif eightballsays == 5:
                    await channel.send(eightball[4])
                elif eightballsays == 6:
                    await channel.send(eightball[5])
                elif eightballsays == 7:
                    await channel.send(eightball[6])
                elif eightballsays == 8:
                    await channel.send(eightball[7])
                elif eightballsays == 9:
                    await channel.send("Maybe later")

            #Kick Command
            if message.content.startswith(f"{p}kick"):
                if message.author.guild_permissions.administrator or message.author.guild_permissions.kick_members or message.author.id == ownerID:
                    memberToKick = message.mentions[0]
                    if len(message.content.split(" ")[2:]) > 0:
                        kick_reason = message.content.split(" ")[2:]
                    else:
                        kick_reason = "No reason provided."
                    await memberToKick.kick(reason=f"Performed by {message.author.name} - " + " ".join(kick_reason))
                    await channel.send(embed=discord.Embed(title="User Kick", description=f"{memberToKick.name} successfully kicked!", color=0xFFFF00))
                    kick_embed_color = 0xFFFF00
                    kick_embed = discord.Embed(title="Admin Log: Member Kick", description=f"A kick has been issued in {message.channel.name}", colour=kick_embed_color).set_thumbnail(url=message.author.avatar_url).add_field(name="Admin", value=f"{message.author.name}").add_field(name="Kicked Member", value=f"{memberToKick.name}").add_field(name="Reason", value=" ".join(kick_reason))
                    await log_channel.send(embed=kick_embed)
                    await message.delete()
                else:
                    await channel.send("You do not have permission to execute this command!")

            #Ban Command
            if message.content.startswith(f"{p}ban"):
                if message.author.guild_permissions.administrator or message.author.guild_permissions.ban_members or message.author.id == ownerID:
                    memberToBan = message.mentions[0]
                    if len(message.content.split(" ")[2:]) > 0:
                        ban_reason = message.content.split(" ")[2:]
                    else:
                        ban_reason = "No reason provided."
                    await memberToBan.ban(reason=f"Performed by {message.author.name} - " + " ".join(ban_reason))
                    await channel.send(embed=discord.Embed(title="User Ban", description=f"{memberToBan.name} successfully banned!", color=0xFF0000))
                    ban_embed_color = 0xFF0000
                    ban_embed = discord.Embed(title="Admin Log: Member Ban", description=f"A ban has been issued on {message.channel.name}", colour=ban_embed_color).set_thumbnail(url=message.author.avatar_url).add_field(name="Admin", value=f"{message.author.name}").add_field(name="Banned Member", value=f"{memberToBan.name}").add_field(name="Reason", value=" ".join(ban_reason))
                    await log_channel.send(embed=ban_embed)
                    await message.delete()
                else:
                    await channel.send("You do not have permission to execute this command!")

            #Unban Command
            if message.content.startswith(f"{p}unban") and (
                    message.author.guild_permissions.administrator or message.author.guild_permissions.ban_members or message.author.id == ownerID):
                await message.delete()
                if len(message.content.split()[1]) == 0:
                    await channel.send("Hey, make sure to use the ID of the banned user! Use ``pirabot-blist`` to see who you'd like to unban.")
                else:
                    try:
                        memberToUnban = await client.get_user_info(user_id=message.content.split()[1])
                        if len(message.content.split(" ")[2:]) > 0:
                            unban_reason = message.content.split(" ")[2:]
                        else:
                            unban_reason = "No reason provided."
                        await message.guild.unban(user=memberToUnban, reason=" ".join(unbanReason))
                        await channel.send(embed=discord.Embed(title="User Unban", description=f"{memberToUnban} successfully unbanned!", color=0x00FF00))
                        embed_unban_color = 0x00FF00
                        embed_unban = discord.Embed(title="Admin Log: Member Unban", description=f"An unban has been issued on the user {memberToUnban}", colour=embed_unban_color).set_thumbnail(url=message.author.avatar_url).add_field(name="Admin", value=f"{message.author.name}").add_field(name="Unbanned User", value=f"{memberToUnban}").add_field(name="Reason", value=" ".join(unban_reason))
                        await log_channel.send(embed=embed_unban)
                    except Exception as e:
                        await channel.send(f"Are you sure your ID is correct? The input threw a ``{e.__class__.__name__}``!\nStatistics for nerds: ``{e.__class__.__name__}: {e}``")

            #Ban List Command
            if message.content == f"{p}blist":
                if message.author.guild_permissions.administrator or message.author.guild_permissions.ban_members or message.author.id == ownerID:
                    if len(await message.guild.bans()) != 0:
                        await channel.send("\n".join([":hammer: Name: {.user.name} ID: {.user.id} Reason: {.reason}".format(entry, entry, entry) for entry in await message.guild.bans()]))
                    else:
                        await channel.send(":interrobang: - No one is banned!")

            #Log Test Command
            if message.content == f"{p}testlog":
                if fs.exists(f"log_of_{message.guild.id}.txt"):
                    with open(f"log_of_{message.guild.id}.txt", "r+") as file:
                        teststr = file.read()
                    await channel.send(f"The log ID of this guild is ``{teststr}``, which points to <#{teststr}> !")
                else:
                    await channel.send("This guild has no log channel defined!")

            #Set Announce Ch Command
            if message.content.startswith(f"{p}setannounce"):
                if message.author.guild_permissions.administrator:
                    if len(message.content[len(f"{p}setannounce "):]) > 0:
                        if message.content.split()[1].isdigit():
                            if not fs.exists(f"annch_of_{message.guild.id}.txt"):
                                fs.write(f"annch_of_{message.guild.id}.txt", "none")
                            fs.write(f"annch_of_{message.guild.id}.txt", message.content.split()[1])
                            await channel.send(":white_check_mark: - Log Channel set!")
                        elif message.content.split()[1].startswith("<#"):
                            chanID = message.content[len(p + "setannounce <#"):-1]
                            if not fs.exists(f"annch_of_{message.guild.id}.txt"):
                                fs.write(f"annch_of_{message.guild.id}.txt", "none")
                            fs.write(f"annch_of_{message.guild.id}.txt", "".join(chanID))
                            await channel.send(":white_check_mark: - Log Channel set!")
                        else:
                            await channel.send(":interrobang: - The input is not right!")
                else:
                    await channel.send(":interrobang: - You can't use this!")

            #Announce Command
            if message.content.startswith(f"{p}announce"):
                if message.author.guild_permissions.administrator:
                    if len(message.content[len(f"{p}announce "):]) > 0:
                        await message.delete()
                        if fs.exists(f"annch_of_{message.guild.id}.txt"):
                            with open(f"annch_of_{message.guild.id}.txt", "r+") as file:
                                chanID = file.read()
                            annChan = message.guild.get_channel(int(chanID))
                            await annChan.send(f"@everyone\n**This announcement is made by <@{message.author.id}> !**\n\n " + " ".join(message.content.split(" ")[1:]))
                        else:
                            await channel.send(f":interrobang: - This guild has no log channel set! Make sure to set it using ``{p}setlog``!")
                    else:
                        await channel.send(":interrobang: - You didn't say anything!")
                else:
                    await channel.send(":interrobang: - You're not allowed to use this command!")

            #Test Command
            if message.content.startswith(f"{p}testthis"):
                await channel.send("I work!")

            #Set Welcome Command
            if message.content.startswith(f"{p}setwelcome"):
                if message.author.guild_permissions.administrator:
                    if len(message.channel_mentions) > 0:
                        if len(message.content.split()[2:]) > 0:
                            if not fs.exists(f"welc_ch_of_{message.guild.id}.txt"):
                                fs.write(f"welc_ch_of_{message.guild.id}.txt", "0")
                            fs.write(f"welc_ch_of_{message.guild.id}.txt", f"{message.channel_mentions[0].id}")
                            if not fs.exists(f"welc_msg_of_{message.guild.id}.txt"):
                                fs.write(f"welc_msg_of_{message.guild.id}.txt", "None")
                            welcMsg = " ".join(message.content.split(" ")[2:])
                            fs.write(f"welc_msg_of_{message.guild.id}.txt", welcMsg)
                            await channel.send(f":white_check_mark: - Channel saved as <#{message.channel_mentions[0].id}> and message saved as:\n\n{welcMsg}\n")
                        else:
                            await channel.send(":interrobang: - Please define a message!")
                    else:
                        if fs.exists(f"welc_msg_of_{message.guild.id}.txt"):
                            os.remove(f"welc_msg_of_{message.guild.id}.txt")
                        if fs.exists(f"welc_ch_of_{message.guild.id}.txt"):
                            os.remove(f"welc_ch_of_{message.guild.id}.txt")
                        await channel.send(":exclamation: - Deleted all welcome settings for this server!")
                else:
                    await channel.send(":interrobang: - You don't have permission to do this!")

            #Test Welcome Command
            if message.content.startswith(f"{p}testwelcome"):
                if message.author.guild_permissions.administrator or message.author.id == ownerID:
                    if fs.exists(f"welc_ch_of_{message.guild.id}.txt"):
                        if fs.exists(f"welc_msg_of_{message.guild.id}.txt"):
                            with open(f"welc_ch_of_{message.guild.id}.txt", "r+") as file1:
                                welcCh = client.get_channel(int(file1.read()))
                            with open(f"welc_msg_of_{message.guild.id}.txt", "r+") as file2:
                                msg = file2.read()
                            if "{USERNAME}" in msg:
                                msg = msg.replace("{USERNAME}", f"{message.author.name}")
                            if "{USERID}" in msg:
                                msg = msg.replace("{USERID}", f"{message.author.id}")
                            if "{MENTION}" in msg:
                                msg = msg.replace("{MENTION}", f"<@{message.author.id}>")
                            if "{SRVNAME}" in msg:
                                msg = msg.replace("{SRVNAME}", f"{message.guild.name}")
                            await welcCh.send(msg)
                        else:
                            await channel.send(":interrobang: - Mysteriously enough, the message to send is missing! Please redefine your channel and message and try again.")
                    else:
                        await channel.send(f":interrobang: - No channel is set as the welcome channel! Did you use ``{p}setwelcome``?")
                else:
                    await channel.send(":interrobang: - You are not allowed to use this here!")

            #Ping Command
            if message.content.startswith(f"{p}ping"):
                current_time = int(round(time.time()*1000))
                m = await channel.send("Pong! ---ms")
                last_time = int(round(time.time()*1000))
                last_time -= current_time
                await m.edit(content="Pong! {}ms".format(last_time))

            #Help Command
            if message.content == f"{p}help":
                embed_help_colour = 0xFF00FF
                embed_help = discord.Embed(title="Help Window", description=f"This bot's prefix is ``{p}``.", colour=embed_help_colour).set_thumbnail(url=message.author.avatar_url).set_footer(text="All commands HAVE to be lower-case!").set_author(name=message.author).add_field(name="suggest <message>", value="Suggests something to the bot owner!", inline=False).add_field(name="about", value="Basic/advanced information about the bot!").add_field(name="id", value="Gets the ID of the user who uses the command and says it openly in chat.", inline=False).add_field(name="name <ID>", value="Shows the name based of an user's ID.", inline=False).add_field(name="say <message>", value="Repeats the words said. If @everyone is inside of the input, the message will get replaced.", inline=False).add_field(name="ping", value="Check the speed of the bot!", inline=False).add_field(name="rand <number>", value="Randomizes a number between 1 and the number input.", inline=False).add_field(name="usercount", value="Says how many users are inside of the server.", inline=False).add_field(name="userstats [mention or ID of user]", value="Gives the statuses of a user, either by ID or by mention. If no one is mentioned, the author's statuses get shown.", inline=False).add_field(name="dice", value="Rolls a number between 1 and 6.", inline=False).add_field(name="8ball <message>", value="Speaks for itself.", inline=False).add_field(name="testlog", value="Shows the log channel of the guild, if defined.", inline=False)
                await channel.send(embed=embed_help)
                await channel.send(f"If you want to see the admin commands of this bot, use ``{p}help +admin``!\nThis bot also has a ``@everyone`` filter! Make sure to use ``{p}help +everyone`` to see how it works!\nLastly, the bot has a welcome feature! Make sure to check it using ``{p}help +welcome``!")

            if message.content == f"{p}help +welcome":
                await channel.send("This bot supports a welcome feature that welcomes everyone new into the server! To enable it, use the following command:\n\n``DD!setwelcome <channel> <message>``\n\nRequired permissions to use this feature: ``administrator``\nThe channel must be mentioned normally.\nThe message to send also supports a few tricks to make it fancier!\nIn order to use these, please write them down WITH the brackets!\n```{USERNAME} - The username of the new member.\n{USERID} - The simple ID of the new member.\n{MENTION} - Mentions the new member.\n{SRVNAME} - The server's name.```\n\n:exclamation: **PLEASE NOTICE!** Not mentioning any channel will delete any current settings for the entire guild. Please make sure the channel is valid and that the bot can use it!")

            #Everyone Help Command
            if message.content == f"{p}help +everyone":
                await channel.send("This bot uses a ``everyone`` filter that only certain users can bypass. To make it globally server-friendly, it's summarized in permissions.\nThe permissions you need (at least 1 of them) are:```administrator\nkick_members\nban_members\nmanage_channels\nview_audit_log\nmanage_guild\nmanage_messages```As long as ONE of these is present inside of your role(s), you are whitelisted and can spam as much as you feel like!")

            #Admin Help Command
            if message.content == f"{p}help +admin":
                embed_help_admin_colour = 0xFF00FF
                embed_help_admin = discord.Embed(title="Admin Commands", description="Please make sure you meet the requirements before using any of these!", colour=embed_help_admin_colour)
                embed_help_admin.add_field(name="mute <mention>", value="Mutes an user. The role ``PiraBot Muted`` must be present inside of the server.\nRequired permissions: ``manage_roles`` OR ``administrator``", inline=False)
                embed_help_admin.add_field(name="unmute <mention>", value="Unmutes the user. Same role and permissions required as from ``mute``.", inline=False)
                embed_help_admin.add_field(name="warn <mention>", value="Warns a mentioned user. On the 4th usage of the command, the user gets kicked, a log for it gets placed in the SAME channel and the user gets a \"ban\" warn. On the 3rd warn kick, a ban is executed instead.\nRequired permissions: ``kick_members`` OR ``administrator``", inline=False)
                embed_help_admin.add_field(name="unwarn <mention>", value="Unwarns a mentioned user. Same permissions required as from ``warn``.", inline=False)
                embed_help_admin.add_field(name="kick <mention> <reason>", value="Kicks a mentioned user from the server. Log is set using ``setlog``, or defaults back to where the command is used..\nRequired permissions: ``kick_members`` OR ``administrator``", inline=False)
                embed_help_admin.add_field(name="ban <mention> <reason>", value="Bans a mentioned user from the server. Log is stored in the same channel as ``kick``.\nRequired permissions: ``ban_members`` OR ``administrator``", inline=False)
                embed_help_admin.add_field(name="setlog <mention/ID>", value="Sets the log channel of the server. This is used for all commands except mute/unmute. If the channel is not found or invalid, it defaults back to the channel where the certain command is used.\nRequired permissions: ``administrator``", inline=False)
                embed_help_admin.add_field(name="setannounce <mention/ID>", value="Sets the announcement channel of the server. This is only used for ``DD!announce``.\nRequired permissions: ``administrator``")
                embed_help_admin.add_field(name="announce <message>", value="Announces something into the announcement channel!\nRequired permissions: ``administrator``")
                embed_help_admin.add_field(name="purge <number>", value="Bulk deletes a set amount of messages. Don't worry doing too much, the bot will still work.\nRequired permissions: ``manage_messages``")
                embed_help_admin.add_field(name="testwelcome", value="Tests the welcome message. The info required for the user fields will always be gathered from the author.\nRequired permissions: ``administrator``")
                embed_help_admin.add_field(name="cursefil <0/1>", value="Enables/disables the curse filter for the server. Default is at ``0``. ``0`` - Disabled; ``1`` - Enabled.\nRequired permissions: ``administrator``")
                await channel.send(embed=embed_help_admin)

            #Good Bot
            if message.content == "good bot!":
                await channel.send(":heart: :robot:")

            #Bad Bot
            if message.content == "bad bot!":
                await channel.send(":C")

            #Bot Gei
            if message.content == "bot gei":
                no = discord.File("C:/Users/CritZ/Pictures/nobelium.png")
                u = discord.File("C:/Users/CritZ/Pictures/uranium.png")
                await channel.send(file=no)
                await channel.send(file=u)

            #Suggest Command
            if message.content.startswith(f"{p}suggest"):
                await message.delete()
                suggestion = message.content.split(" ")[1:]
                suggch = client.get_channel(448496794809401354)
                await suggch.send(f"{message.author.name} ``{message.author.id}`` from {message.guild.name} ``{message.guild.id}`` suggested: ``" + " ".join(suggestion) + "``")


client = MyClient()
with open('TOKEN.txt', 'r') as auth:
    client.run(auth.read())
