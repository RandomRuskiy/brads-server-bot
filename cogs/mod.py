import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext

from .slash import guild_ids

client = commands.Bot(command_prefix='£')
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
    @commands.is_owner()
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
    @commands.is_owner()
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
    @commands.is_owner()
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


def setup(bot):
    bot.add_cog(Mod(bot))
