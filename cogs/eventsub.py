import discord
import discord_slash
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
import os
from twitchAPI.twitch import Twitch
import json


client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)
guild_ids = [834037980883582996]  # << brads server id
# guild_ids = [720743461959237722]
# ^^ my test server id. change if your testing elsewhere


class EventSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')


def setup(bot):
    bot.add_cog(EventSub(bot))
