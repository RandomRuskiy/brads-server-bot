import os

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from datetime import datetime

c_time = datetime.now()

client = commands.Bot(command_prefix='£')


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log = open("messages.log", "a")
        dt_str = c_time.strftime("%d/%m/%Y %H:%M:%S")
        log_msg_1 = f"{dt_str}: MESSAGE DELETED: author: '{message.author}', msg_content: '{message.content}' channel: '{message.channel}'"
        log_msg_2 = log_msg_1.replace("\n", "(+)")
        log_msg = log_msg_2 + '\n'
        log.write(log_msg)
        log.close
        channel = self.bot.get_channel(720743462508691639)
        await channel.send(log_msg)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        log = open("messages.log", "a")
        dt_str = c_time.strftime("%d/%m/%Y %H:%M:%S")
        log_msg_1 = f"{dt_str}: MESSAGE EDITED: author: '{message_before.author}', msg_before: '{message_before.content}', msg_after: '{message_after.content}' channel: '{message_before.channel}'"
        log_msg_2 = log_msg_1.replace("\n", "(+)")
        log_msg = log_msg_2 + '\n'
        log.write(log_msg)
        log.close
        channel = self.bot.get_channel(720743462508691639)
        await channel.send(log_msg)


def setup(bot):
    bot.add_cog(Logs(bot))
