import asyncio
import csv
from doctest import debug_script
import os
import random
import subprocess
import time
import traceback
import socket
import json
from main import DEBUG, logger
from datetime import datetime
from cogs.db import collection

import discord
from discord.ext import commands

from discord import voice_client

hostname = socket.gethostname()
if DEBUG:
    logger.info(hostname)


if hostname == 'raspberrypi':
    guild_ids = [834037980883582996, 795738345745547365]
    bot_user = 867713807291908137
    log_channel = 851170405356011520
    member_channel = 873869752169271327
    mute_id = 879041072486035506
    message_channel = 851170405356011520
    voice_channel = 851170790367559720
elif hostname != 'raspberrypi':
    guild_ids = [720743461959237722, 875804519605370911]
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
    async def dmuser(self, ctx, userid: str, message: str):
        ctx.interaction.response.defer()
        user = await client.get_user(userid)
        try:
            await user.send(message)
        except Exception as e:
            logger.info(e)
            ctx.respond("Cannot dm member because they are off or something idk")

    # errors go here

    '''@setstatusslash.error
    async def setstatusslash_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.'
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "Missing a required argument: You might want to specify the status"
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Missing permissions: yo you arent part of the bot team to run this command"
            )

    @mentalhealthquote.error
    async def mentalhealthquote_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.'
            )'''

# keep at bottom


def setup(bot):
    bot.add_cog(Slash(bot))
