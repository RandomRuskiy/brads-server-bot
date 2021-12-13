import discord
from discord import commands
# add imports here

client = commands.Bot(
    command_prefix='£',
    debug_guild=875804516905370911
    )


class Lofi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # put commands here


def setup(bot):
    bot.add_cog(Lofi(bot))
