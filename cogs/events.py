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

        elif message.author == discord.User.bot:
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

        elif message.content == 'L':
            await message.channel.send('L')

        # list events as empty commands so people can see what auto-responses exist which will be shown in the help page
    @commands.command(
        name='Auto-Responses',
        description='Everything listed within the `Events` section are the words that the bot will respond to.'
    )
    @commands.is_owner()
    async def responseplaceholder(self, ctx):
        return

    @commands.command(
        name='meaning of O_O',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def meaningplaceholder(self, ctx):
        return

    @commands.command(
        name='yo',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def yo1placeholder(self, ctx):
        return

    @commands.command(
        name='Yo',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def yo2placeholder(self, ctx):
        return

    @commands.command(
        name='L',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def lplaceholder(self, ctx):
        return


def setup(bot):
    bot.add_cog(Events(bot))
