import logging
import os
import sys
from pathlib import Path
import json

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import subprocess
import time
import traceback
import random
import csv
import asyncio

from keep_alive import keep_alive

DEBUG = False

logger = logging.getLogger('discord')
if DEBUG is True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8', mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s ')
)
logger.addHandler(handler)

cwd = Path(__file__).parents[0]
cwd = str(cwd)
if DEBUG:
    logger.info(cwd)

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
              'cogs.Logs',
              'cogs.lofi'
              ]


@client.event
async def on_command_error(ctx, error):
    logger.error(f'Error From Command "{ctx.message.content}": {error}')


@client.event
async def on_ready():
    with open("data/laststatus.json") as f:
        data = json.load(f)
    if data["activityType"] == "Game":
        activity = discord.Game(name=data["activityName"])
    elif data["activityType"] == "Watching":
        activity = discord.Activity(type=discord.ActivityType.watching, name=data["activityName"])
    elif data["activityType"] == "Streaming":
        activity = discord.Streaming(name=data["activityName"], url="https://www.twitch.tv/brad_04_")
    elif data["activityType"] == "Listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=data["activityName"])
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('yo the bot is on now\n-----')
    f.close()
    logger.info(
        msg="bot is ready"
    )

client.remove_command('help')
client.remove_command('unban')


# keep this at bottom


if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")
    #client.load_extension('cogs.config')

    client.run(TOKEN)
