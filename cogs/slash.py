import csv
import random
import subprocess
import socket
import json
from main import DEBUG, logger
from cogs.db import collection
from lib.colours import BasicColours

import discord
from discord.ext import commands

hostname = socket.gethostname()
if DEBUG:
    logger.info(hostname)

guild_ids = []

if hostname == 'raspberrypi':
    guild_ids = [834037980883582996, 795738345745547365]
    bot_user = 867713807291908137
    member_channel = 1172613820749983814
    mute_id = 879041072486035506
    message_channel = 1172609890934591600
    log_channel = message_channel
    voice_channel = 1172609620305526874
elif hostname != 'raspberrypi':
    guild_ids = [720743461959237722]
    bot_user = 854401220537745408
    log_channel = 720743462508691639
    member_channel = 720743462508691639
    mute_id = 913878775329062982
    message_channel = 720743462508691639
    voice_channel = 720743462508691639
    yt_notif_channel = 720743462508691639

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
)


def save_status(atype: str, aname: str):
    act_dict = {"activityType": f"{atype}", "activityName": f"{aname}"}
    with open("data/laststatus.json", "w") as f:
        json.dump(act_dict, f)
    f.close()


def crash_cmd(input: str):
    cmd = ["cat", "cowsay"]
    if any(w == input for w in cmd):
        return True
    else:
        return False


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def slashtest(self, ctx, *, text: str):
        await ctx.respond(text)

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setstatusslash(self, ctx, *, text: str):
        activity = discord.Game(name=text)
        save_status("Game", text)
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=activity)
        await ctx.respond(f'yo my status is now **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setstream(self, ctx, *, text: str):
        activity = discord.Streaming(name=text, url="https://www.twitch.tv/brad_04_")
        save_status("Streaming", text)
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=activity
        )
        await ctx.respond(f'yo watching live: **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setgame(self, ctx, *, text: str):
        activity = discord.Game(name=text)
        save_status("Game", text)
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=activity
        )
        await ctx.respond(f'yo im now playing: **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setwatching(self, ctx, *, text: str):
        activity = discord.Activity(type=discord.ActivityType.watching, name=text)
        save_status("Watching", text)
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=activity
        )
        await ctx.respond(f'yo im now watching: **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setlistening(self, ctx, *, text: str):
        activity = discord.Activity(type=discord.ActivityType.listening, name=text)
        save_status("Listening", text)
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=activity
        )
        await ctx.respond(f'yo im now Listening to: **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.cooldown(rate=1, per=15)
    async def mentalhealthquote(self, ctx):
        with open('data/quotes.dat', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            random_row = random.choice(list(spamreader))
            lis_str = ' '.join(random_row)
            res_str = lis_str.replace('"', '')
            sec_str = res_str.replace('[', '')
            res_quote = sec_str.replace(']', '')
            await ctx.respond(res_quote)

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def bash(self, ctx, *, input: str):
        if crash_cmd(input) is False:
            cmd = subprocess.run(['bash', '-c', input], capture_output=True)
            out = cmd.stdout.decode()
            err = cmd.stderr.decode()
            cmd_name = input.split()[0]
            if cmd.returncode == 0:
                await ctx.respond(f'{cmd_name}:\n```{out} ```')

            elif cmd.returncode != 0:
                await ctx.respond(f'Error: `{err}`')

        else:
            await ctx.respond(
                'The command you tried to run needs a varible otherwise it will crash the bot lmao'
            )

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def file(self, ctx, *, filename: str):
        await ctx.respond(file=discord.File(rf'./{filename}'))

    @client.slash_command(
        name='db',
        description='Add a user to the DB',
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def db_add(self, ctx, *, member: discord.Member):
        q = {"_id": member.id}
        join_date = int(member.joined_at.timestamp())
        name = None
        if (collection.count_documents(q) == 0):
            post = {"_id": member.id, "username": member.name + member.discriminator, "server_join_date": join_date}
            collection.insert_one(post)
            logger.info(f'New member ({member}) has been added to DB')
            await ctx.respond(f'New member ({member}) has been added to DB')
        else:
            user = collection.find(q)
            try:
                for r in user:
                    name = r['username']
                    date = r['server_join_date']
            except KeyError:
                for r in user:
                    name = r['username']
                    date = None
            if name != member:
                collection.update_one(q, {"$set": {"username": member.name + '#' + member.discriminator}})
            collection.update_one(q, {"$set": {"server_join_date": join_date}})
            logger.info(f'Member ({member}) has DB entries already, join date info has been updated')
            await ctx.respond(f'Member ({member}) has DB entries already, join date info has been updated')

    @client.slash_command(
        name='invite',
        description='Invite the bot',
        guild_ids=guild_ids
    )
    async def invite(self, ctx):
        ctx.respond('How about you invite your mother hahahahahahahahahahahahahahahaahahahaha')

    @client.slash_command(
        name='echo',
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def echo(self, ctx, message: str):
        ctx.interaction.response.defer()
        ctx.send(message)

    @client.slash_command(
        name='dm-user',
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def dmuser(self, ctx, userid: discord.User, message: str):
        # await ctx.interaction.response.defer()
        # id = int(userid)
        # user = await client.get_user(id)
        try:
            await userid.send(message)
            await ctx.respond("done")
        except Exception as e:
            logger.info(e)
            await ctx.respond("Cannot dm member because they are off or something idk")

    @client.slash_command(
        name="serverinfo",
        description="View infomation about the server.",
        guild_ids=guild_ids
    )
    async def serverinfo(self, ctx):
        # [TODO]: member count,
        return

    @client.slash_command(
        name="userinfo",
        description="Get infomation on a user.",
        guild_ids=guild_ids
    )
    @commands.cooldown(1, 30)
    async def userinfo(self, ctx, member: discord.Member):
        # [TODO]: Weekly message count, may require using a different DB than mongoDB, will have to see
        rolesList = [role.mention for role in member.roles]
        del rolesList[0]
        rolesFormatted = ', '.join(rolesList)
        embed = discord.Embed(color=0xFFFFFF, title=f"{member.display_name}'s Info")
        embed.set_author(name=member.name, icon_url=member.display_avatar)
        embed.add_field(name='Account Age', value=f'<t:{int(member.created_at.timestamp())}:R>', inline=False)
        embed.add_field(name='Server Join Date', value=f'<t:{int(member.joined_at.timestamp())}:R>', inline=False)
        embed.add_field(name='Roles', value=str(rolesFormatted), inline=False)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Slash(bot))
