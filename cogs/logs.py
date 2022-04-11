import os

import discord
from discord import guild
from discord.ext import commands
from discord.embeds import Embed
from discord.ext.commands import BucketType, cooldown
from datetime import datetime
from lib.colours import RoleColours as colours
import cogs.slash as slash_ids
from cogs.slash import guild_ids, message_channel, voice_channel
from __main__ import logger

message_channel_id = slash_ids.message_channel


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
            log_msg_1 = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: MESSAGE DELETED: author: '{message.author}', msg_content: '{message.content}' channel: '{message.channel}' link: {message.jump_url}"
            log_msg_2 = log_msg_1.replace("\n", "(+)")
            log_msg = log_msg_2 + '\n'
            log.write(log_msg)
            log.close

        async def to_discord(message):
            filter_id = 795738345745547365
            if (message.guild.id != filter_id) and (message.author.bot is False):
                embed = discord.Embed(
                    description=f"A message has been deleted in {message.channel.mention}",
                    color=colours["red"]
                )
                embed.add_field(
                    name="Content",
                    value=f"{message.content}",
                    inline=False
                )
                embed.add_field(
                    name="Date",
                    value=f"<t:{int(datetime.timestamp(datetime.now()))}>",
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
            log_msg_1 = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: MESSAGE EDITED: author: '{message_before.author}', msg_before: '{message_before.content}', msg_after: '{message_after.content}' channel: '{message_before.channel}'"
            log_msg_2 = log_msg_1.replace("\n", "(+)")
            log_msg = log_msg_2 + '\n'
            log.write(log_msg)
            log.close

        async def to_discord():
            if str(message_after) == str(message_before):
                return
            channel = discord.utils.get(message_before.author.guild.channels, id=message_channel)
            embed = discord.Embed(
                colour=colours['pink'],
                description=f'{message_before.author} has updated their message in {message_before.channel}!'
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

        if message_before.guild.id != 795738345745547365 and message_before.author.bot is False:
            await to_discord()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = discord.utils.get(member.guild.channels, id=voice_channel)
        logger.debug(f'Member: {member} VoiceStateBefore: {before.channel} VoiceStateAfter: {after.channel}')

        def voice_join(before, after):
            if before.channel is None:
                return True
            elif after.channel is None:
                return False
        logger.debug(f'Member Joined: {voice_join(before, after)}')

        async def join_log(member, after):
            embed = discord.Embed(colour=colours['green'], description=f'{member} has joined {after.channel}')
            embed.set_author(name=member, icon_url=member.display_avatar.url)
            embed.add_field(
                name='Channel',
                value=f'{after.channel.mention} ({after.channel})',
                inline=False
            )
            embed.add_field(
                name='ID',
                value=f'```ini\nUserID = {member.id}\nChannelID = {after.channel.id}```'
            )
            await channel.send(embed=embed)

        async def leave_log(member, before, after):
            embed = discord.Embed(colour=colours['red'], description=f'{member} has left {before.channel}')
            embed.set_author(name=member, icon_url=member.display_avatar.url)
            embed.add_field(
                name='Channel',
                value=f'{before.channel.mention} ({before.channel})',
                inline=False
            )
            embed.add_field(
                name='ID',
                value=f'```ini\nUserID = {member.id}\nChannelID = {before.channel.id}```'
            )
            await channel.send(embed=embed)

        async def move_log(member, before, after):
            if (before.channel is not None and after.channel is not None) and (before.channel != after.channel):
                embed = discord.Embed(colour=0x59515E, description=f'{member} has moved to {after.channel}')
                embed.set_author(name=member, icon_url=member.display_avatar.url)
                embed.add_field(
                    name='Channel Before',
                    value=f'{before.channel.mention} ({before.channel})',
                    inline=False
                )
                embed.add_field(
                    name='Channel After',
                    value=f'{after.channel.mention} ({after.channel})',
                    inline=False
                )
                embed.add_field(
                    name='ID',
                    value=f'```ini\nUserID = {member.id}\nChannelID = {after.channel.id}```'
                )
                await channel.send(embed=embed)

        if voice_join(before, after) is True:
            await join_log(member, after)
        elif voice_join(before, after) is False:
            await leave_log(member, before, after)
        else:
            await move_log(member, before, after)


def setup(bot):
    bot.add_cog(Logs(bot))
