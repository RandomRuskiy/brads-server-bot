import discord
from discord import Webhook
from discord.ext import commands, tasks
import xmltodict
import json
from cogs.slash import yt_notif_channel, guild_ids
from flask import Flask, request
from xml.parsers.expat import ExpatError
from __main__ import logger

yt_channel_id = 'UC0aX3Uv0MHTma2ywkGc5IHA'
notif_channel = yt_notif_channel

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
)

app = Flask(__name__)


@app.route('/')
def index():
    return 'Test'


@app.route('/feed', methods=['GET', 'POST'])
async def feed():
    challenge = request.args.get('hub.challenge')
    if challenge:
        return challenge

    try:
        xml_dict = xmltodict.parse(request.data)

        channel_id = xml_dict["feed"]["entry"]["yt:channelId"]
        if channel_id != yt_channel_id:
            logger.error('Channel ID incorrect, sent 403')
            return '', 403

        video_url = xml_dict["feed"]["entry"]["link"]["@href"]
        logger.info(f'Recived new URL: {video_url}')

        message = f'Brad just posted a new video go check it out! :D {video_url}'
        webhook = Webhook.from_url('https://canary.discord.com/api/webhooks/856140270219558912/W1W8CsB_5pAZBRo1ftMX7LMJrIdY7AhAmK2QZdE9eeZZOoMYU_mjJbs1KfeURspZfYwt')
        response = webhook.send(message)

    except (ExpatError, LookupError):
        return '', 403

    return '', 204


class YtNotif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')


app.run()


def setup(bot):
    bot.add_cog(YtNotif(bot))
