import discord
from discord.ext import commands
from discord.ui import Button, View
from __main__ import logging
from cogs.slash import guild_ids

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
)


class CreateButton(Button):
    def __init__(self):
        super().__init__(label='Create Ticket', style=discord.ButtonStyle.green)