## INDENTS ARE SET TO 2 SPACES ON THIS FILE ##
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord_slash import SlashCommand, SlashContext
import os
import logging
from pathlib import Path
from keep_alive import keep_alive

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)
TOKEN = os.getenv('TOKEN')

extentions = ['cogs.Embeds', 'cogs.Config', 'cogs.Help', 'cogs.Events', 'cogs.Slash']

# dump commmand errors to console for debug
@client.event
async def on_command_error(ctx, error):
  pass

#console status event
@client.event
async def on_ready():
  #await client.change_presence(status = discord.Status.online)
  print('yo the bot is on now\n-----')

client.remove_command('help')



'''@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("meaning of O_O"):
    await message.channel.send('Brad is shocked or ran out of things to say lmao')

  if msg.startswith('Hi'):
      ctx = await client.get_context(message)
      await message.channel.send(f'Hey {ctx.author.mention} hope your day is going great'

  await client.process_commands(message)'''

#error loops for commands
'''@support.error
async def clear_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.')'''

'''@setstatus.error
async def clear_error(ctx, error):
  print(error)
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.')'''


#keep this at bottom

if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

keep_alive()
client.run(TOKEN)
