import json
import time
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from lib.colours import BasicColours as colour
from __main__ import logger

from cogs.slash import bot_user, member_channel, guild_ids

# self.spam_control = commands.CooldownMapping.from_cooldown()

client = commands.Bot(
    command_prefix='£',
    debug_guild=guild_ids
)

# owner_id = [645647583141822466, 683733441728217098]
# owner_id = 683733441728217098
admin_ids = [835960034331590666, 842689593052889098, 868107974655238185, 879381563740147763] # admin/mod etc roles
msg_ban = [426467132272934912, 603662161209982998, 475671397457461258, 587541588763213834]


def is_bot(message):
    if message.author == bot_user:
        return True
    elif message.author.bot is True:
        return True
    elif message.author.id == msg_ban:
        return True
    else:
        return False


def banned_words(message):
    with open("data/banned_words.json") as f:
        words = json.load(f)
    bad_words = words["banned_words"]
    res = [ele for ele in bad_words if(ele in message.content.lower())]
    if bool(res) is True:
        logger.warn(f'{message.author} has said a banned word! ({res})')
        return True
    else:
        return False


async def role_names(member):
    member_roles_list = member.roles
    names = []
    for x in member_roles_list:
        names.append(x.name)
    names = f'{names[1:]}'.strip('[')
    names = f'{names}'.strip(']')
    names = f'{names}'.strip("'")
    return names


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.last_timestamp = datetime.datetime.utcfromtimestamp(0)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.Cog.listener()
    async def on_message(self, message):
        time_difference = (datetime.datetime.utcnow() - self.last_timestamp).total_seconds()

        def has_admin_role(message):
            a1 = discord.utils.get(message.author.roles, id=868107974655238185)
            a2 = discord.utils.get(message.author.roles, id=842689593052889098)
            a3 = discord.utils.get(message.author.roles, id=835960034331590666)
            a4 = discord.utils.get(message.author.roles, id=879381563740147763)
            if (a1 or a2 or a3 or a4):
                return True
            else:
                return False
        admin_role = None

        def cooldown_role(message):
            admin_role = has_admin_role(message)
            if message.guild.id == 834037980883582996:
                if admin_role is True:
                    return False
                elif int(time_difference) < 10:
                    return True
                else:
                    return False
            else:
                return False

        def call_cooldown(message):
            if has_admin_role(message) is not True:
                self.last_timestamp = datetime.datetime.utcnow()

        if is_bot(message) is False and cooldown_role(message) is False:  # only respond if user is not self or another bot

            if message.channel.name == 'general' or message.channel.name != 'general' or message.author != discord.User.bot:
                if message.content == '.test respond':
                    ctx = await self.bot.get_context(message)
                    await message.channel.send(f'this message was sent in {message.channel} and admin_roles = {has_admin_role(message)} and {discord.ClientUser.id} and {ctx.guild.member_count} and roles = {ctx.author.roles} and {bool(is_bot(message))}')
                    return

                elif message.content == 'yo im saying something':
                    await message.channel.send('yo im responding')
                    return

                elif message.content == 'destiny 2':
                    if admin_role is True:
                        await message.channel.send('shit game smh brad would rather do your mother :troll:')
                        return
                    else:
                        pass

                elif message.content == 'yo':
                    ctx = await self.bot.get_context(message)
                    await message.channel.send(f'yo {ctx.author.mention}')
                    return

                elif message.content == 'Yo':
                    ctx = await self.bot.get_context(message)
                    await message.channel.send(f'yo {ctx.author.mention}')
                    return

                elif message.content == 'L' and message.author != self.bot.user:
                    await message.channel.send('L')
                    call_cooldown(message)
                    return

                elif message.content == 'am i admin':
                    if admin_role is True:
                        await message.channel.send('yo you are admin')
                    else:
                        await message.channel.send('L your are not admin')

        if is_bot(message) is False:

            if banned_words(message) is True:
                await message.delete()
                await message.channel.send(f"smh saying bad words {message.author.mention}", delete_after=5.0)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            embed = discord.Embed(title="Welcome!", url="https://discord.com/channels/834037980883582996/878418546265313310/883713010768691273",
                                  description=f"Welcome to Brads server, {member}! Please feel free to send a couple memes, cute pet photo's or intresting facts.", color=colour["green"])
            embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/867713807291908137/02e63019fc51f3ea2735f2e2d7acc49b.png?size=256")
            embed.add_field(name="Please make sure to to read and accept the rules to gain access to all other channels open to members", value="\uFEFF", inline=False)
            embed.add_field(name="Please don't promote any Other charity's or ask for us to get server members to go to any other server or website", value="Apart from all that, have fun :D", inline=True)
            await member.send(embed=embed)
        except Exception as e:
            print(e)
            channel = discord.utils.get(member.guild.channels, id=member_channel)
            await channel.send(f"Cant DM new member {member}, prob has dms off")
        u = client.get_user(member.id)

        async def join_msg(member):
            embed = discord.Embed(
                colour=colour["green"],
                description=f"{member.mention} has joined!"
            )
            embed.set_author(
                name=member,
                icon_url=member.display_avatar
            )
            embed.add_field(
                name="Name",
                value=f"{member} ({member.id}) {member.mention}",
                inline=False
            )
            embed.add_field(
                name="Server Join Date",
                value=f"<t:{int(time.time())}>",
                inline=False
            )
            embed.add_field(
                name="Creation Date",
                value=f"<t:{int(member.created_at.timestamp())}> (<t:{int(member.created_at.timestamp())}:R>)",
                inline=False
            )
            embed.add_field(
                name="Member Count",
                value=f"{member.guild.member_count}",
                inline=True
            )
            channel = discord.utils.get(member.guild.channels, id=member_channel)
            await channel.send(embed=embed)
        await join_msg(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        value = ' '

        def member_timestamp(member):
            if type(member.joined_at.timestamp) == float:
                value = f"<t:{int(member.joined_at.timestamp)}> (<t:{member.joined_at.timestamp}:R>)"
            else:
                value = "*Couldn't get member join date info*"
            return value

        async def leave_msg(member):
            member_timestamp(member)
            embed = discord.Embed(
                colour=colour["red"],
                description=f"{member} has left!"
            )
            embed.set_author(
                name=member,
                icon_url=member.display_avatar
            )
            embed.add_field(
                name="User Info",
                value=f"{member} ({member.id}) {member.mention}",
                inline=False
            )
            embed.add_field(
                name="Roles",
                value=role_names(member),
                inline=False
            )
            embed.add_field(
                name="Server Join Date",
                value=member_timestamp(member),
                inline=False
            )
            embed.add_field(
                name="Creation Date",
                value=f"<t:{int(member.created_at.timestamp())}> (<t:{int(member.created_at.timestamp())}:R>)"
            )
            channel = discord.utils.get(member.guild.channels, id=member_channel)
            await channel.send(embed=embed)
        await leave_msg(member)


def setup(bot):
    bot.add_cog(Events(bot))
