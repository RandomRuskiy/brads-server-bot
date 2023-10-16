import discord
from discord.ext import commands
from __main__ import logging
from cogs.slash import guild_ids

logger.debug('import')

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
)


class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @client.slash_command(
        name='whitelist',
        guild_ids=guild_ids
    )
    async def create_commands(ctx, channel: discord.GuildChannel()):
        channel = discord.utils.get(ctx.guild.channels, name=channel)

        messages = await channel.history().flatten()

        print(messages)


def setup(bot):
    bot.add_cog(Whitelist(bot))
