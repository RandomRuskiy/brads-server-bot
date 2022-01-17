import asyncio
import json

import discord
from discord.ext import commands

from cogs.slash import guild_ids, mute_id

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
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
            await ctx.respond("lol you cant ban yourself")

        elif user == self.bot.user:
            await ctx.respond("why you try ban me :(")

        elif reason is None:
            reason = "No reson specified"
        message = f"You have been banned from **{ctx.guild.name}** for **{reason}**"
        await ctx.guild.ban(user, reason=reason)
        await ctx.respond(f"**{user}** has been banned!")

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
            await ctx.respond(f"**{user}** has been unbanned!")

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, user: discord.Member, reason=None):
        if user is None or user == ctx.author:
            await ctx.respond('You cant kick yourself lol')

        elif user == self.bot.user:
            await ctx.respond('yo im not kicking myself')

        elif reason is None:
            reason = 'No reason specified'

        await ctx.guild.kick(user, reason=reason)
        await ctx.respond(f'**{user}** has been kicked!')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, time=None, reason=None):
        mute_role = discord.utils.get(ctx.guild.roles, id=mute_id)
        if user is None or user == ctx.author:
            await ctx.respond('You cant mute yourself')
            return
        elif mute_role is True:
            await ctx.respond('That user is already muted')

        elif time is None:
            await ctx.respond('You need to specify a time. e.g. 1s, 1m, 1h, 1d')
            return

        else:
            if not reason:
                reason = f'Muted by {ctx.author}'

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
                    await ctx.respond('put a correct duration smh')

            except Exception as e:
                print(e)
                await ctx.respond('error happened, prob invalid time input or something idk')
            await user.add_roles(mute_role, reason=f'{reason} - {ctx.author}')
            await ctx.respond(f'Muted {user} for reason: {reason}')
            await asyncio.sleep(int(seconds))
            await user.remove_roles(mute_role, reason='Duration of mute over')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member, reason=None):
        mute_role = discord.utils.get(ctx.guild.roles, id=mute_id)
        if user is None or user == ctx.author:
            await ctx.respond('how')
        elif reason is None:
            reason = 'No reason specified'
        elif not mute_role:
            await ctx.respond('That user isnt muted smh')
        else:
            await user.remove_roles(mute_role, reason='Mute manually removed')
            await ctx.respond(f'Unmuted {user}')

    @client.slash_command(
        guild_ids=guild_ids
    )
    @commands.has_permissions(manage_messages=True)
    async def banword(self, ctx, word: str):
        # [TODO]: command to add a word to the banned words list
        fr = open('data/banned_words.json', 'r')
        word_list = json.load(fr)
        fr.close()
        current = word_list["banned_words"]
        current.append(word)
        new_dict = {"banned_words": current}
        nd_str = str(new_dict)
        w = nd_str.replace("\'", "\"")
        fw = open('data/banned_words.json', 'w')
        fw.write(w)
        fw.close()
        await ctx.respond(f'Added **{word}** to the banned words list.')


def setup(bot):
    bot.add_cog(Mod(bot))
