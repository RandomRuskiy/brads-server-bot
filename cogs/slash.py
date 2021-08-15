import asyncio
import csv
import os
import random
import subprocess
import time
import traceback

import discord
import discord_slash
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext

client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)
guild_ids = [834037980883582996]  # << brads server id
# guild_ids = [720743461959237722, 875804519605370911]
# ^^ my test server id. change if your testing elsewhere


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
    @commands.is_owner()
    async def slashtest(self, ctx: SlashContext, *, text: str):
        await ctx.send(text)

    @cog_ext.cog_slash(
        name='setstatuslash',
        description='Set the bots status but with a slash command',
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setstatusslash(self, ctx: SlashContext, *, text: str):
        activity = discord.Game(name=text)
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=activity)
        await ctx.send(f'yo my status is now **"{text}"**')

    @cog_ext.cog_slash(
        name='mentalhealthquote',
        description='Get a random quote thats on the mental health topic!',
        guild_ids=guild_ids
    )
    @commands.cooldown(rate=1, per=15)
    async def mentalhealthquote(self, ctx: SlashContext):
        with open('data/quotes.dat', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            random_row = random.choice(list(spamreader))
            lis_str = ' '.join(random_row)
            res_str = lis_str.replace('"', '')
            sec_str = res_str.replace('[', '')
            res_quote = sec_str.replace(']', '')
            await ctx.send(res_quote)

    @cog_ext.cog_slash(
        name='bash',
        description='Run a command in bash',
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def bash(self, ctx: SlashContext, *, input: str):
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

    @cog_ext.cog_slash(
        name='file',
        description='Upload a file from the bots source!',
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def file(self, ctx: SlashContext, *, filename: str):
        await ctx.send(file=discord.File(rf'./{filename}'))

    # empty commands for slash commands they appear in the help page.
    # If you know a better way of doing this go ahead and change it

    @commands.command(
        name='/setstatuslash',
        description='Set the bots status but with a slash command!'
    )
    @commands.is_owner()
    async def placeholdersetstatus(self, ctx):
        return

    @commands.command(
        name='/mentalhealthquote',
        description='Get a random quote thats on the mental health topic!'
    )
    @commands.is_owner()
    async def placeholdermhq(self, ctx):
        return

    # errors go here

    @setstatusslash.error
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
            )

# keep at bottom


def setup(bot):
    bot.add_cog(Slash(bot))
