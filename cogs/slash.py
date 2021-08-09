import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext, SlashContext, SlashCommand
import os
import asyncio
import traceback

client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)
guild_ids = [834037980883582996]
admin_ids = 835960034331590666, 849692224060784720, 868107974655238185, 842689593052889098, 846730005924151318



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
  @commands.cooldown(rate=1, per=30)
  async def setstatusslash(self, ctx: SlashContext, *, text: str):
    activity = discord.Game(name=text)
    await self.bot.change_presence(status=discord.Status.online, activity=activity)
    await ctx.send(f'yo my status is now **"{text}"**')

  @commands.command()
  @commands.is_owner()
  async def print(self, ctx):
    print(admin_ids)
    await ctx.send(admin_ids)


  # errors go here

  @setstatusslash.error
  async def setstatusslash_error(self, ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.')

    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Missing a required argument: You might want to specify the status")

    elif isinstance(error, commands.MissingPermissions):
      await ctx.send("Missing permissions: yo you arent part of the bot team to run this command")


# keep at bottom
def setup(bot):
  bot.add_cog(Slash(bot))
