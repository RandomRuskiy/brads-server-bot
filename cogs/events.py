
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.__class__.__name__} Cog has been loaded\n-----')
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.bot.user:
      return

    elif message.content == '.test respond':
      await message.channel.send('worked')

    elif message.content == 'yo im saying something':
      await message.channel.send('yo im responding')

    elif message.content == 'meaning of O_O':
      await message.channel.send('Brad is shocked or ran out of things to say lmao')

    elif message.content == 'yo':
      ctx = await self.bot.get_context(message)
      await message.channel.send(f'yo {ctx.author.mention}')

    elif message.content == 'Yo':
      ctx = await self.bot.get_context(message)
      await message.channel.send(f'yo {ctx.author.mention}')

    #await self.bot.process_commands(message)
  





def setup(bot):
  bot.add_cog(Events(bot))
