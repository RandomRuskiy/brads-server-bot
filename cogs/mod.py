import asyncio
import json

import discord
from discord.ext import commands

from .slash import guild_ids

client = commands.Bot(
    command_prefix='£',
    debug_guild=875804519605370911
)


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

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
    async def mute(self, ctx, user: discord.User, time=None, reason=None):
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
                   await ctx.send('put a correct duration smh')
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

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def banword(self, ctx, word: str):
        # [TODO]: command to add a word to the banned words list
        pass


def setup(bot):
    bot.add_cog(Mod(bot))
