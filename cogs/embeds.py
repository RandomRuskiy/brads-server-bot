from logging import debug
import discord
from discord.ext import commands
from .slash import guild_ids
import asyncio
from lib.colours import BasicColours

# im seeing how to do cogs which will help make it look neater and so we shouldnt have to restart the bot everytime we make/edit a command


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.slash_command(
        name='donate',
        description="Donate to YoungMinds!",
        debug_guilds=guild_ids
    )
    @commands.cooldown(1, 30)
    async def donate(self, ctx):
        embed = discord.Embed(title="Donate", description="This is the link to donate to the YoungMinds charity to aid in the support for mental health. Please donate if you can. Thanks!")
        embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fsocialsolihull.org.uk%2Flocaloffer%2Fwp-content%2Fuploads%2Fsites%2F21%2F2016%2F02%2FYoungMinds.png&f=1&nofb=1")
        embed.add_field(name="Donate Here:", value="https://www.youngminds.org.uk/support-us/donate/", inline=False)
        embed.add_field(name="If you want to know more about the charity, read here:", value="https://www.youngminds.org.uk/", inline=True)
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name='socials',
        description="The links to all of Brad's social meadia accounts!",
        debug_guilds=guild_ids
    )
    @commands.cooldown(1, 30)
    async def socials(self, ctx):
        embed = discord.Embed(title="Here are the links for all my socials", color=0x06c4f4)
        embed.add_field(name="Twitch", value="https://www.twitch.tv/brad_04_", inline=False)
        embed.add_field(name="Youtube", value="https://www.youtube.com/channel/UC0aX3Uv0MHTma2ywkGc5IHA", inline=False)
        embed.add_field(name="Tiktok", value="https://www.tiktok.com/@brad_l._.l_?lang=en", inline=False)
        embed.add_field(name="Twitter", value="https://twitter.com/BradD11058775", inline=False)
        embed.add_field(name="Instagram", value="https://www.instagram.com/brad_l._.l_/", inline=False)
        embed.set_footer(text="To Donate to me or YoungMinds do /support to donate to Brad and /Donate for YoungMinds")
        await ctx.respond(f'{ctx.author.mention}', embed=embed)

    @commands.slash_command(
        name='support',
        description="Help support Brad!",
        debug_guilds=guild_ids
    )
    @commands.cooldown(rate=1, per=30)
    async def support(self, ctx):
        await ctx.respond(f'Hey {ctx.author.mention} before you consider supporting me you can put your money towards YoungMinds by doing `/donate`, however if you are still considering supporting me I appreciate it SOOO much here is where you can support me at: \n \n https://streamelements.com/brad_04_/tip')

    @commands.slash_command(
        name='hotlines',
        description="Hotline numbers for those in need.",
        debug_guilds=guild_ids
    )
    async def hotlines(self, ctx):
        embed = discord.Embed(title="Suicide hotlines", description="Here is a list of hotlines if you ever need someone to talk to.")
        embed.set_thumbnail(url="https://res.cloudinary.com/dywkbcfp5/image/upload/w_200,h_200,c_thumb,z_0.65,g_face,e_improve,f_auto/f_auto/v1580072134/therapyRoutePublicImages/avatar.png")
        embed.add_field(name="This link takes you to the list", value="https://www.therapyroute.com/article/helplines-suicide-hotlines-and-crisis-lines-from-around-the-world", inline=False)
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name='github',
        description='The link to the bots github repository.',
        debug_guilds=guild_ids
    )
    @commands.cooldown(rate=1, per=30)
    async def github(self, ctx):
        embed = discord.Embed(title="The bots git repo")
        embed.add_field(name="Want to contribute code to the bot?", value="Go to the github repo and read the README for more info\n https://github.com/RandomRuskiy/brads-server-bot", inline=False)
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name='twitchemotes',
        description="Infomation on how to see the additional emotes in brad's twitch chat!",
        debug_guilds=guild_ids
    )
    @commands.cooldown(1, 30)
    async def twitchemotes(self, ctx):
        embed = discord.Embed(title="Can't see these emotes in Brad's twitch chat?", url="https://imgur.com/a/NsYNY6P", description="Then go-to https://www.frankerfacez.com/ and download the browser extention. To see the additional emotes, click on the icon next to your profile icon on twitch (its in the top-right), go to the add-ons tab and enable the Better TTV and 7tv add-ons!")
        embed.add_field(name="On Mobile?", value="Go to your phones app-store and download the 'Chatsen' app so you can watch the stream and chat with all the additional emotes!", inline=False)
        embed.set_footer(text="Need help? Feel free to ping RandomRuskiy for help")
        await ctx.respond(embed=embed)

    @commands.command(
        name='info-embed',
    )
    @commands.is_owner()
    async def info_embed(self, ctx):
        embed = discord.Embed(title="Read About & Info", url='https://docs.google.com/document/d/1YVRzTlDcg4wVyWQuPRpFSu2PwK47N1jIclz2YDRlVP8/edit?usp=sharing', description='This is the About and Info Section On Brads Discord Click "Read About & Info" for more.', color=0x54ec0e)
        embed.set_author(name="About & Info", url="https://www.twitch.tv/brad_04_", icon_url="https://cdn.discordapp.com/avatars/867713807291908137/30924e309d80df585dd5b8368c02c6d6.webp?size=128")
        embed.add_field(name="What is this link?", value="This Link will take you to a page which tells you all about Brads Discord Server such as: How to get onto the Minecraft Server, The Server Roles...", inline=True)
        embed.set_footer(text="Thank You for Joining The Server <3")
        await ctx.channel.purge(limit=1)
        await asyncio.sleep(1)
        await ctx.send('@everyone')
        await ctx.send(embed=embed)

    @commands.command(
        name='mod-app'
    )
    @commands.is_owner()
    async def mod_app(self, ctx):
        embed = discord.Embed(title='Moderator and Admin Application', url='https://forms.gle/N8qdmHmadhfxU2C87', description='^ Click Here to Apply for staff Role on Brads Server ^', colour=0x11ff00)
        embed.set_author(name='Click Below for Mod and Admin Applications', url='https://www.twitch.tv/brad_04_', icon_url='https://cdn.discordapp.com/avatars/867713807291908137/30924e309d80df585dd5b8368c02c6d6.webp?size=128')
        embed.add_field(name='Click the blue text to apply for:', value='Admin or Moderator', inline=True)
        embed.set_footer(text='Please Note: You can only apply to become an Admin or Mod if you have The "Active Members" role, This doesn\'t guarantee you get the role but is required. also applying for Admin you have to have been a Moderator first.')
        await ctx.channel.purge(limit=1)
        await asyncio.sleep(0.1)
        await ctx.send('<@&912755564755419157>')
        await ctx.send(embed=embed)

    @commands.command(
        name='socials-ping'
    )
    @commands.is_owner()
    async def socials_ping(self, ctx):
        embed = discord.Embed(title="Here are the links for all my socials", color=0x06c4f4)
        embed.add_field(name="Twitch", value="https://www.twitch.tv/brad_04_", inline=False)
        embed.add_field(name="Youtube", value="https://www.youtube.com/channel/UC0aX3Uv0MHTma2ywkGc5IHA", inline=False)
        embed.add_field(name="Tiktok", value="https://www.tiktok.com/@brad_l._.l_?lang=en", inline=False)
        embed.add_field(name="Twitter", value="https://twitter.com/BradD11058775", inline=False)
        embed.add_field(name="Instagram", value="https://www.instagram.com/brad_l._.l_/", inline=False)
        embed.set_footer(text="To Donate to me or YoungMinds do £support to donate to Brad and £Donate for YoungMinds")
        await ctx.send('@everyone', embed=embed)

    @commands.slash_command(
            name="rules-embed"
            )
    @commands.is_owner()
    async def rules_embed(self, ctx):
        embed = discord.Embed(title="The Rules of BradVibesLive <3", description="1. No inviting Raiders or Any Toxic Members, You will be banned and They will be banned. No Ban Evasion either.\n\n2. No NSFW content\n\n3. Absolutely zero hate speech, racism, DDos threats, threats, or sexist remarks.\n\n4. No Slurs of any kind will be tolerated.\n\n5. Do not attempt to impersonate myself, a member of a staff team or anyone else for that matter.\n\n6. No mass pings or mentions of users or roles\n\n7. Do not post comments that are indecent, inappropriate, or discriminatory\n\n8. Do not ear-rape, or post seizure inducing content\n\n9. Do not spam, that includes but is not limited to: spam pings, spam images, spam emotes, spam gifs, or spam stickers\n\n10. try to keep everything in the correct channel!\n\n11. Treat everyone with respect and kindness, whether that be contextual, audio, video or photo\n\n12. Keep Messages In ENGLISH ONLY.\n\n13. Follow the Discord Rules and Terms of Service! (This includes at least being 13 To join!) https://discord.com/terms\n\n14. If something is common sense (example pinging @/everyone) or threatening others Even if it's not in the rules, you clearly shouldn't be doing that.\n\n15. Leaking someone personal information or doxing/death threats will result in insta ban.\n\n16. We are not responsible for what you choose to do outside of this server. Do not bring personal matters within the server, keep this place drama free.", colour=0x00b0f4)
        await ctx.respond("ok", ephemeral=True)
        await ctx.send(embed=embed)

    # errors go Here

    @github.error
    async def github_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.')

    @socials.error
    async def socials_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry')


def setup(bot):
    bot.add_cog(Embeds(bot))
