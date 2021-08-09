import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os
import asyncio
import traceback

client = commands.Bot(command_prefix='£')


class Slash(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.__class__.__name__} Cog has been loaded\n-----')

  @cog_ext.cog_slash(
  name='slashtest',
  description='test slash command'
  )
  async def slashtest(self, ctx: SlashContext):
    await ctx.send('yo this is a test slash command')




# keep at bottom
def setup(bot):
  bot.add_cog(Slash(bot))
