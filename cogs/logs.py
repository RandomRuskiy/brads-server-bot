import os

import discord
from discord import guild
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from datetime import datetime
from lib.colours import RoleColours as colours
import cogs.slash as slash_ids
from cogs.slash import guild_ids, message_channel

message_channel_id = slash_ids.message_channel

c_time = datetime.now()

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
)


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        message_channel = discord.utils.get(message.author.guild.channels, id=message_channel_id)

        def to_file(message):
            log = open("messages.log", "a")
            dt_str = c_time.strftime("%d/%m/%Y %H:%M:%S")
            log_msg_1 = f"{dt_str}: MESSAGE DELETED: author: '{message.author}', msg_content: '{message.content}' channel: '{message.channel}'"
            log_msg_2 = log_msg_1.replace("\n", "(+)")
            log_msg = log_msg_2 + '\n'
            log.write(log_msg)
            log.close

        async def to_discord(message):
            filter_id = 795738345745547365
            if message.guild.id != filter_id:
                embed = discord.Embed(
                    description=f"A message has been deleted in {message.channel.mention}",
                    color=colours["red"]
                )
                embed.add_field(
                    name="Content",
                    value=message.content,
                    inline=False
                )
                embed.add_field(
                    name="Date",
                    value=f"<t:{int(c_time.timestamp())}>",
                    inline=False
                )
                embed.add_field(
                    name="ID",
                    value=f"```ini\nUserID = {message.author.id}\nMessageID = {message.id}```",
                    inline=False
                )
                embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
                await message_channel.send(embed=embed)
            else:
                return
        await to_discord(message)
        to_file(message)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        def to_file():
            log = open("messages.log", "a")
            dt_str = c_time.strftime("%d/%m/%Y %H:%M:%S")
            log_msg_1 = f"{dt_str}: MESSAGE EDITED: author: '{message_before.author}', msg_before: '{message_before.content}', msg_after: '{message_after.content}' channel: '{message_before.channel}'"
            log_msg_2 = log_msg_1.replace("\n", "(+)")
            log_msg = log_msg_2 + '\n'
            log.write(log_msg)
            log.close
        async def to_discord():
            channel = discord.utils.get(message_before.author.guild.channels, id=message_channel)
            embed = discord.Embed(
                colour=colours['pink'],
                description=f'{message_before.author} has updated thir message in {message_before.channel}!'
            )
            embed.add_field(
                name='Channel',
                value=f'{message_before.channel.mention}\n{message_before.jump_url}',
                inline=False
            )
            embed.add_field(
                name='Now',
                value=message_after.content,
                inline=False
            )
            embed.add_field(
                name='Before',
                value=message_before.content,
                inline=False
            )
            embed.add_field(
                name='ID',
                value=f'```ini\nUserID = {message_before.author.id}\nMessageID = {message_before.id}```',
                inline=False
            )
            embed.set_author(name=message_before.author, icon_url=message_before.author.display_avatar.url)
            await channel.send(embed=embed)
        to_file()
        await to_discord()



def setup(bot):
    bot.add_cog(Logs(bot))
