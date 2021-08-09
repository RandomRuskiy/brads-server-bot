import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
import os
import asyncio
import traceback

client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)
guild_ids = [834037980883582996]



class Slash(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.__class__.__name__} Cog has been loaded\n-----')

  @cog_ext.cog_slash(
  name='slashtest',
  description='test slash command',
  guild_ids=guild_ids
  )
  async def _slashtest(self, ctx: SlashContext):
    await ctx.send('yo this is a test slash command')

  @cog_ext.cog_slash(
  name='setstatuslash',
  description='Set the bots status but with a slash command',
  guild_ids=guild_ids
  )
  @commands.is_owner()
  async def setstatusslash(self, ctx: SlashContext, *, text: str):
    activity = discord.Game(name=text)
    await self.bot.change_presence(status=discord.Status.online, activity=activity)
    await ctx.send(f'yo my status is now **"{text}"**')



# keep at bottom
def setup(bot):
  bot.add_cog(Slash(bot))
