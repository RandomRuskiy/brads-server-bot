import discord
from discord import commands
from youtube_dl import YoutubeDL
from requests import get
from discord import FFmpegPCMAudio
from discord.utils import get
from cogs.slash import guild_ids
# add imports here

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
    )


class Lofi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.SlashCommand(
            name='lofijoin',
            debug_guild=875804516905370911
            )
    @commands.has_role("Members :D")
    async def lofijoin(self, ctx):
        
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        def search(query):
            with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
                info = ydl.extract_info("https://youtube.com/playlist?list=PL6NdkXsPL07IOu1AZ2Y2lGNYfjDStyT6O", download=False)
            return(info, info['formats'][0]['url'])

        async def join(self, ctx, voice):
            channel = ctx.author.voice.channel

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()


        video, source = search(query)
        voice = get(bot.voice_clients, guild=ctx.guild)

        await join(self, ctx, voice)
        await ctx.respond()



def setup(bot):
    bot.add_cog(Lofi(bot))
