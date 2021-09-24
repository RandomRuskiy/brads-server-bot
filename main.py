import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import subprocess
import time
import traceback
import random
import csv
import asyncio
from cogs.slash import guild_ids

from keep_alive import keep_alive

run = True

if run is False:
    exit()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8', mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
)
logger.addHandler(handler)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix='£', intents=intents)
TOKEN = os.getenv('TOKEN')

extentions = ['cogs.Embeds',
              'cogs.Config',
              'cogs.Help',
              'cogs.Events',
              'cogs.Slash',
              'cogs.Twitch',
              'cogs.Mod',
              'cogs.Logs'
              ]


@client.event
async def on_command_error(ctx, error):
    # dump commmand errors to console for debug
    pass

# console status event


@client.event
async def on_ready():
    # await client.change_presence(status = discord.Status.online)
    print('yo the bot is on now\n-----')

client.remove_command('help')
client.remove_command('unban')


class Commands():

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    async def slashtest(ctx, text: str):
        await ctx.send(text)

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.is_owner()
    @commands.cooldown(rate=1, per=30)
    async def setstatus(ctx, text: str):
        activity = discord.Game(name=text)
        await client.change_presence(
            status=discord.Status.online,
            activity=activity
        )
        await ctx.send(f'yo my status is now **"{text}"**')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.cooldown(rate=1, per=15)
    async def mentalhealthquote(ctx):
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
    async def bash(ctx, input: str):
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
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *, reason=None):
        if user is None or user == ctx.author:
            await ctx.send("lol you cant ban yourself")
            return

        elif user == self.bot.user:
            await ctx.send("why you try ban me :(")
            return

        elif reason is None:
            reason = "No reson specified"
        message = f"You have been banned from **{ctx.guild.name}** for **{reason}**"
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"**{user}** has been banned!")

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"**{user}** has been unbanned!")
            return

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, user: discord.Member, reason=None):
        if user is None or user == ctx.author:
            await ctx.send('You cant kick yourself lol')
            return

        elif user == self.bot.user:
            await ctx.send('yo im not kicking myself')
            return

        elif reason is None:
            reason = 'No reason specified'

        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f'**{user}** has been kicked!')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, time=None, reason=None):
        mute_role = discord.utils.get(user.roles, id=879041072486035506)
        if user is None or user == ctx.author:
            await ctx.send('You cant mute yourself')
            return
        elif mute_role is True:
            await ctx.send('That user is already muted')

        elif time is None:
            await ctx.send('You need to specify a time. e.g. 1s, 1m, 1h, 1d')
            return

        else:
            if not reason:
                'No reason specified'

            try:
                seconds = time[:-1]
                duration = time[-1]
                if duration == 's':
                    seconds = seconds * 1
                elif duration == 'm':
                    seconds = seconds * 60
                elif duration == 'h':
                    seconds = seconds * 60 * 60
                elif duration == 'd':
                    seconds = seconds * 86400

                else:
                    ctx.send('put a correct duration smh')
                    return

            except Exception as e:
                print(e)
                await ctx.send('error happened, prob invalid time input or something idk')
                return
            await user.add_roles(mute_role, reason=reason)
            await ctx.send(f'Muted {user} for reason: {reason}')
            await asyncio.sleep(seconds)
            await user.remove_roles(mute_role, reason='Duration of mute over')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member, reason=None):
        mute_role = discord.utils.get(user.roles, id=879041072486035506)
        if user is None or user == ctx.author:
            await ctx.send('how')
            return
        elif reason is None:
            reason = 'No reason specified'
        elif not mute_role:
            await ctx.send('That user isnt muted smh')
        else:
            await user.remove_roles(mute_role, reason='Mute manually removed')
            await ctx.send(f'Unmuted {user}')


# keep this at bottom

if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

keep_alive()
client.run(TOKEN)
