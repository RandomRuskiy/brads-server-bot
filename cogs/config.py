import discord
from discord.ext import commands
import os
import asyncio
import traceback
import random
from discord.ext.commands import cooldown, BucketType
import subprocess

client = commands.Bot(command_prefix='£')


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.command(
        name='reload',
        description='Reloads command modules. Either can be specified which one or all if no input'
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # if nothing specified, it reloads evrything
            async with ctx.typing():
                embed = discord.Embed(
                    title='Reloading all command modules',
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir('./cogs/'):
                    if ext.endswith('.py') and not ext.startswith('_'):
                        try:
                            self.bot.unload_extension(f'cogs.{ext[:-3]}')
                            self.bot.load_extension(f'cogs.{ext[:-3]}')
                            embed.add_field(
                                name=f'Reloaded: `{ext}`',
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f'Failed to reload: `{ext}`',
                                value=e,
                                inline=False
                            )
                    await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload specified cog
            async with ctx.typing():
                embed = discord.Embed(
                    title='Reloading all command modules',
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f'{cog.lower()}.py'
                if not os.path.exists(f'./cogs/{ext}'):
                    # if file doesnt exist
                    embed.add_field(
                        name=f'Failed to reload `{ext}`',
                        value='You must be dreaming of that files existance or something'
                    )

                elif ext.endswith('.py') and not ext.startswith('_'):
                    try:
                        self.bot.unload_extension(f'cogs.{ext[:-3]}')
                        self.bot.load_extension(f'cogs.{ext[:-3]}')
                        embed.add_field(
                            name=f'Reloaded: `{ext}`',
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name='Failed to reload: `{ext}`',
                            value=desired_trace,
                            inline=False
                        )
                    await ctx.send(embed=embed)

    @commands.command(
        name='setstatus',
        description='Set the bots playing status.'
    )
    @cooldown(rate=1, per=30)
    @commands.is_owner()
    async def setstatus(self, ctx, *, text: str):
        activity = discord.Game(name=text)
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.send(f'yo my status is now **"{text}"**')

    @commands.command(
        name='ping',
        description='Test the current latency of the bot.'
    )
    @cooldown(rate=1, per=30)
    async def ping(self, ctx):
        await ctx.send(f"There is a round time of {str(round(self.bot.latency, 2))} secconds")

    @commands.command(
        name='update',
        description='pull recently commited stuff from the repo'
    )
    @commands.is_owner()
    @cooldown(rate=1, per=30)
    async def update(self, ctx):
        run = subprocess.run(['git', 'pull', 'https://github.com/RandomRuskiy/brads-server-bot', 'master'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(run.stdout)
        await ctx.send(run.stdout)

    @commands.command(
        name='testgit',
        description='just a test to see if pushing from local works'
    )
    @commands.is_owner()
    async def testgit(self, ctx):
        await ctx.send('yo this command was made on my local pc, pushed to the repo and then pulled to the remote server to see if the whole chain worked :)')

    @commands.command(
        name='load',
        description='Load specified cog'
    )
    @commands.is_owner()
    async def load(self, ctx, cog=None):
        if not cog:
            await ctx.send('You need to specify a cog to reload!')

        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title='Loading command module',
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f'{cog.lower()}.py'
                if not os.path.exists(f'./cogs/{ext}'):
                    # if file doesnt exist
                    embed.add_field(
                        name=f'Failed to reload `{ext}`',
                        value='You must be dreaming of that files existance or something'
                    )

                elif ext.endswith('.py') and not ext.startswith('_'):
                    try:
                        self.bot.load_extension(f'cogs.{ext[:-3]}')
                        embed.add_field(
                            name=f'Loaded: `{ext}`',
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name='Failed to reload: `{ext}`',
                            value=desired_trace,
                            inline=False
                        )
                    await ctx.send(embed=embed)

    # errors go here

    @setstatus.error
    async def setstatus_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing a required argument: You might want to specify the status")

    @load.error
    async def load_error(self, ctx, error):
        embed = discord.Embed(
            title='Failed to load cog!'
        )
        embed.add_field(
            name='Reason:',
            value=error,
            inline=False
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Config(bot))
