import asyncio
import csv
import os
import random
import subprocess
import time
import traceback
import socket
import json

import discord
from discord.ext import commands

# guild_ids = [834037980883582996]  # << brads server id
# guild_ids = [720743461959237722, 875804519605370911]
# ^^ my test server id. change if your testing elsewhere

hostname = socket.gethostname()
print(hostname)
if hostname == 'ruskiy-linux.lan' or 'DESKTOP-87U253A' or 'LAPTOP-BRGNIO26':
    guild_ids = [720743461959237722, 875804519605370911]
    bot_user = 854401220537745408
    log_channel = 720743462508691639
    member_channel = 720743462508691639
    mute_id = 913878775329062982
    message_channel = 720743462508691639

if hostname == 'raspberrypi':
    guild_ids = [834037980883582996, 795738345745547365]
    bot_user = 867713807291908137
    log_channel = 851170405356011520
    member_channel = 873869752169271327
    mute_id = 879041072486035506
    message_channel = 851170405356011520

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
