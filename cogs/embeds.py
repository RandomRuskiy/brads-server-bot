import discord
from discord.ext import commands

## im seeing how to do cogs which will help make it look neater and so we shouldnt have to restart the bot everytime we make/edit a command

class Embeds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.last_member = None

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.__class__.__name__} Cog has been loaded\n-----')

  @commands.command(
    name='donate',
    description='Donate to the YoungMinds Charity!'
  )
  async def donate(self, ctx):
    embed=discord.Embed(title="Donate", description="This is the link to donate to the YoungMinds charity to aid in the support for mental health. Please donate if you can. Thanks!")
    embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fsocialsolihull.org.uk%2Flocaloffer%2Fwp-content%2Fuploads%2Fsites%2F21%2F2016%2F02%2FYoungMinds.png&f=1&nofb=1")
    embed.add_field(name="Donate Here:", value="https://youngminds.org.uk/donate/", inline=False)
    embed.add_field(name="If you want to know more about the charity, read here:", value="https://youngminds.org.uk/about-us/who-we-are/", inline=True)
    await ctx.send(embed=embed)

  @commands.command(
    name='socials',
    description="The links to all of Brad's social meadia accounts!"
  )
  async def socials(self, ctx):
    embed=discord.Embed(title="Here are the links for all my socials", color=0x06c4f4)
    embed.add_field(name="Twitch", value="https://www.twitch.tv/brad_04_", inline=False)
    embed.add_field(name="Youtube", value="https://www.youtube.com/channel/UC0aX3Uv0MHTma2ywkGc5IHA", inline=False)
    embed.add_field(name="Tiktok", value="https://www.tiktok.com/@brad_l._.l_?lang=en", inline=False)
    embed.add_field(name="Twitter", value="https://twitter.com/BradD11058775", inline=False)
    embed.add_field(name="Instagram", value="https://www.instagram.com/brad_l._.l_/", inline=False)
    embed.set_footer(text="To Donate to me or YoungMinds do £support to donate to Brad and £Donate for YoungMinds")
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)

  @commands.command(
    name='support',
    description='Donate to Brad'
  )
  @commands.cooldown(rate=1, per=30)
  async def support(self, ctx):
    await ctx.send(f'Hey {ctx.author.mention} before you consider supporting me you can put your money towards YoungMinds by doing £donate however if you are still considering supporting me i appreciate it SOOO much here is where you can support me at: \n \n https://www.buymeacoffee.com/Brad04')

  @commands.command(
    name='hotlines',
    description='A link to where you can find hotlines for your country if you ever need help.'
  )
  async def hotlines(self, ctx):
    embed=discord.Embed(title="Suicide hotlines", description="Here is a list of hotlines if you ever need someone to talk to.")
    embed.set_thumbnail(url="https://res.cloudinary.com/dywkbcfp5/image/upload/w_200,h_200,c_thumb,z_0.65,g_face,e_improve,f_auto/f_auto/v1580072134/therapyRoutePublicImages/avatar.png")
    embed.add_field(name="This link takes you to the list", value="https://www.therapyroute.com/article/helplines-suicide-hotlines-and-crisis-lines-from-around-the-world", inline=False)
    await ctx.send(embed=embed)

  @commands.command(
  name='github',
  description='The link to the bots github repository.'
  )
  @commands.cooldown(rate=1, per=30)
  async def github(self, ctx):
    embed=discord.Embed(title="The bots git repo")
    embed.add_field(name="Want to contribute code to the bot?", value="Go to the github repo and read the README for more info\n https://github.com/RandomRuskiy/brads-server-bot", inline=False)
    await ctx.send(embed=embed)

  #errors go Here

  @github.error
  async def github_error(self, ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.')


def setup(bot):
  bot.add_cog(Embeds(bot))
