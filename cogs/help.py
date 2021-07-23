import re
import math
import random

import discord
from discord.ext import commands


class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.__class__.__name__} Cog has been loaded\n-----')

  @commands.command(
    name='help',
    aliases=['h', 'commands', 'cmds'],
    description='The command to show commands'
  )
  async def help(self, ctx, cog='1'):
    helpEmbed = discord.Embed(
      title='Help Command',
      color=0x26fff1
    )

    cogs = [c for c in self.bot.cogs.keys()]

    totalPages = math.ceil(len(cogs) / 4)

    cog = int(cog)
    if cog > totalPages or cog < 1:
      await ctx.send(f'Invalid page number: `{cog}`. Please pick from {totalPages}.\nAlternativly, just run help to see the first page')
      return

    neededCogs = []
    for i in range(4):
      x = i + (int(cog) - 1) * 4
      try:
        neededCogs.append(cogs[x])
      except IndexError:
        pass
    
    for cog in neededCogs:
      commandList = ''
      for command in self.bot.get_cog(cog).walk_commands():
        if command.hidden:
          continue
        
        elif command.parent != None:
          continue

        commandList += f'**{command.name}** - *{command.description}*\n'
      commandList += '\n'

      helpEmbed.add_field(
        name=cog,
        value=commandList,
        inline=False
      )

    await ctx.send(embed=helpEmbed)

  @help.error
  async def clear_error(self, ctx, error):
    print(error)





def setup(bot):
  bot.add_cog(Help(bot))