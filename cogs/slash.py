import asyncio
import csv
import os
import random
import subprocess
import time
import traceback

import discord
from discord.ext import commands

client = commands.Bot(
    command_prefix='£',
    debug_guild=875804519605370911
)
guild_ids = [834037980883582996]  # << brads server id
# guild_ids = [720743461959237722, 875804519605370911]
# ^^ my test server id. change if your testing elsewhere


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def slashtest(self, ctx, *, text: str):
        await ctx.send(text)

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setstatusslash(self, ctx, *, text: str):
        activity = discord.Game(name=text)
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=activity)
        await ctx.send(f'yo my status is now **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.cooldown(rate=1, per=15)
    async def mentalhealthquote(self, ctx):
        with open('data/quotes.dat', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            random_row = random.choice(list(spamreader))
            lis_str = ' '.join(random_row)
            res_str = lis_str.replace('"', '')
            sec_str = res_str.replace('[', '')
            res_quote = sec_str.replace(']', '')
            await ctx.send(res_quote)

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def bash(self, ctx, *, input: str):
        if input != 'cat':
            cmd = subprocess.run(['bash', '-c', input], capture_output=True)
            out = cmd.stdout.decode()
            err = cmd.stderr.decode()
            if cmd.returncode == 0:
                await ctx.send(f'{input}: `{out}`')
                pass

            elif cmd.returncode != 0:
                await ctx.send(f'Error: `{err}`')
                pass

        else:
            await ctx.send(
                'The command you tried to run needs a varible otherwise it will crash the bot lmao'
            )
            pass

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def file(self, ctx, *, filename: str):
        await ctx.send(file=discord.File(rf'./{filename}'))

    # errors go here

    '''@setstatusslash.error
    async def setstatusslash_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.'
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "Missing a required argument: You might want to specify the status"
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Missing permissions: yo you arent part of the bot team to run this command"
            )

    @mentalhealthquote.error
    async def mentalhealthquote_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.'
            )'''

# keep at bottom


def setup(bot):
    bot.add_cog(Slash(bot))
