import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import subprocess
import time
import traceback
import random
import csv
import asyncio
from cogs.slash import guild_ids

from keep_alive import keep_alive

run = True

if run is False:
    exit()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8', mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
)
logger.addHandler(handler)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix='£', intents=intents)
TOKEN = os.getenv('TOKEN')

extentions = ['cogs.Embeds',
              'cogs.Config',
              'cogs.Help',
              'cogs.Events',
              'cogs.Slash',
              'cogs.Twitch',
              'cogs.Mod',
              'cogs.Logs'
              ]


@client.event
async def on_command_error(ctx, error):
    # dump commmand errors to console for debug
    pass

# console status event


@client.event
async def on_ready():
    # await client.change_presence(status = discord.Status.online)
    print('yo the bot is on now\n-----')

client.remove_command('help')
client.remove_command('unban')


class Commands():

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def slashtest(ctx, text: str):
        await ctx.send(text)

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setstatus(ctx, text: str):
        activity = discord.Game(name=text)
        await client.change_presence(
            status=discord.Status.online,
            activity=activity
        )
        await ctx.send(f'yo my status is now **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.cooldown(rate=1, per=15)
    async def mentalhealthquote(ctx):
        with open('data/quotes.dat', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            random_row = random.choice(list(spamreader))
            lis_str = ' '.join(random_row)
            res_str = lis_str.replace('"', '')
            sec_str = res_str.replace('[', '')
            res_quote = sec_str.replace(']', '')
            await ctx.send(res_quote)

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def bash(ctx, input: str):
        if input != 'cat':
            cmd = subprocess.run(['bash', '-c', input], capture_output=True)
            out = cmd.stdout.decode()
            err = cmd.stderr.decode()
            if cmd.returncode == 0:
                await ctx.send(f'{input}: `{out}`')
                pass

            elif cmd.returncode != 0:
                await ctx.send(f'Error: `{err}`')
                pass

        else:
            await ctx.send(
                'The command you tried to run needs a varible otherwise it will crash the bot lmao'
            )
            pass


# keep this at bottom

if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

keep_alive()
client.run(TOKEN)
