import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
import asyncio

from .slash import guild_ids

client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @cog_ext.cog_slash(
        name='ban',
        description='Ban a user.',
        guild_ids=guild_ids
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: SlashContext, user: discord.Member = None, *, reason=None):
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

    @cog_ext.cog_slash(
        name='unban',
        description='Unbans the specified user',
        guild_ids=guild_ids
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: SlashContext, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"**{user}** has been unbanned!")
            return

    @cog_ext.cog_slash(
        name='kick',
        description='Kicks a user',
        guild_ids=guild_ids
    )
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx: SlashContext, user: discord.Member, reason=None):
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

    @cog_ext.cog_slash(
        name='mute',
        description='Mutes the specified user',
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx: SlashContext, user: discord.Member, time=None, reason=None):
        mute_role = discord.utils.get(user.roles, id=879041072486035506)
        if user is None or user == ctx.author:
            await ctx.send('You cant mute yourself')
            return
        elif mute_role is true:
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
            await user.add_roles(879041072486035506, reason=reason)
            await ctx.send(f'Muted {user} for reason: {reason}')
            await asyncio.sleep(seconds)
            await user.remove_roles(879041072486035506, reason='Duration of mute over')

    @cog_ext.cog_slash(
        name='unmute',
        description='Unmutes the specified user',
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx: SlashContext, user: discord.Member, reason=None):
        mute_role = discord.utils.get(user.roles, id=879041072486035506)
        if user is None or user == ctx.author:
            await ctx.send('how')
            return
        elif reason is None:
            reason = 'No reason specified'
        elif not mute_role:
            await ctx.send('That user isnt muted smh')
        else:
            await user.remove_roles(879041072486035506, reason='Mute manually removed')
            await ctx.send(f'Unmuted {user}')


def setup(bot):
    bot.add_cog(Mod(bot))
