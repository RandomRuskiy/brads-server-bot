import math
import random
import re

import discord
from discord.ext import commands
from lib.colours import BasicColours as colours


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.command(
        name='help',
        aliases=['h', 'commands', 'cmds'],
        description='The command to show commands'
    )
    @commands.cooldown(rate=1, per=30)
    async def help(self, ctx, cog='1'):
        """helpEmbed = discord.Embed(
            title='Help Command',
            color=colours["cyan"]
        )

        cogs = [c for c in self.bot.cogs.keys()]

        totalPages = math.ceil(len(cogs) / 4)

        cog = int(cog)
        if cog > totalPages or cog < 1:
            await ctx.send(f'Invalid page number: `{cog}`. Please pick from {totalPages}.\nAlternativly, just run help to see the first page')
            return

        neededCogs = []
        for i in range(4):
            x = i + (int(cog) - 1) * 4
            try:
                neededCogs.append(cogs[x])
            except IndexError:
                pass

        for cog in neededCogs:
            commandList = '\uFEFF'
            for command in self.bot.get_cog(cog).walk_commands():
                if command.hidden:
                    continue

                elif command.parent is not None:
                    continue

                commandList += f'**{command.name}** - *{command.description}*\n\n'
            commandList += '\n'

            helpEmbed.add_field(
                name=cog,
                value=commandList,
                inline=False
            )

        await ctx.send(embed=helpEmbed)"""
        await ctx.send("Text commands have been depreciated. Please use the built in way to see all available slash commands\n\n(the old way was better in some ways but oh well)")

    @help.error
    async def clear_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please wait {round(error.retry_after)} secconds until you retry.')


def setup(bot):
    bot.add_cog(Help(bot))
