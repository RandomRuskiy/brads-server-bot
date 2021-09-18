import json
import os

import discord
import requests
from discord.ext import commands
from .slash import guild_ids

client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)


TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
EVENTSUB_TOKEN = os.getenv('EVENTSUB_TOKEN')


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @cog_ext.cog_slash(
        name='checklive',
        description='Check if a stream is currently live!',
        guild_ids=guild_ids
    )
    async def checklive(self, ctx: SlashContext, *, channel: str):
        HEADERS = {
            'Authorization': f'Bearer {EVENTSUB_TOKEN}',
            'Client-Id': TWITCH_CLIENT_ID
        }
        url = f'https://api.twitch.tv/helix/streams?user_login={channel}'
        r = requests.get(url, headers=HEADERS)
        received_json = r.json()
        j_conv = f'{received_json}'
        v_json = j_conv.replace("'", '"')
        vv_json = v_json.replace('False', '"False"')
        f_json = f'{vv_json}'
        parse_json = json.loads(f_json)
        s_json = f'{parse_json}'

        if s_json != "{'data': [], 'pagination': {}}":
            for x in parse_json['data']:
                message = f'The user `{channel}` is live!. {channel} is currently playing {x["game_name"]}! Join the stream at https://www.twitch.tv/{channel}'
                await ctx.send(message)

        else:
            await ctx.send(f'The channel `{channel}` is not live.')


def setup(bot):
    bot.add_cog(Twitch(bot))
