import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, bot
import os
import requests
import json

client = commands.Bot(command_prefix='£')
TOKEN = os.getenv('TOKEN')

sad_words = ["sad", "depressed", ]

# dump commmand errors to console for debug
@client.event
async def on_command_error(ctx, error):
  pass

#console status event
@client.event
async def on_ready():
  await client.change_presence(status = discord.Status.online, activity = discord.Game('yo'))
  print('yo the bot is on now')


def getquote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(resonse.text)  
  quote = json_data[0]["q"] + " -"+ json_data[0]["a"]
  return(quote)

@client.command()
async def ping(ctx):
  await ctx.send(f"There is a round time of {str(round(client.latency, 2))}")

@client.command()
async def donate(ctx):
  embed=discord.Embed(title="Donate", description="This is the link to donate to the YoungMinds charity to aid in the support for mental health. Please donate if you can. Thanks!")
  embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fsocialsolihull.org.uk%2Flocaloffer%2Fwp-content%2Fuploads%2Fsites%2F21%2F2016%2F02%2FYoungMinds.png&f=1&nofb=1")
  embed.add_field(name="Donate Here:", value="https://youngminds.org.uk/donate/", inline=False)
  embed.add_field(name="If you want to know more about the charity, read here:", value="https://youngminds.org.uk/about-us/who-we-are/", inline=True)
  await ctx.send(embed=embed)


#keep this at bottom
client.run(TOKEN)