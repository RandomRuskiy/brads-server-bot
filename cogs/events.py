import json
import time

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from lib.colours import BasicColours as colour

from cogs.slash import bot_user, member_channel

# self.spam_control = commands.CooldownMapping.from_cooldown()

client = commands.Bot(
    command_prefix='£',
    debug_guild=875804519605370911
)

# owner_id = [645647583141822466, 683733441728217098]
# owner_id = 683733441728217098
admin_ids = [835960034331590666, 842689593052889098, 868107974655238185, 879381563740147763]
msg_ban = [426467132272934912]


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
        print(bad_words)
        print(f"found banned word in {message.content}")
        return True
    else:
        return False


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.Cog.listener()
    async def on_message(self, message):
        if is_bot(message) is False:  # only respond if user is not self or another bot

            def has_admin_role(message):
                a1 = discord.utils.get(message.author.roles, id=879381563740147763)
                a2 = discord.utils.get(message.author.roles, id=868107974655238185)
                a3 = discord.utils.get(message.author.roles, id=835960034331590666)
                if a1 or a2 or a3 is True:
                    return True
                else:
                    return False

            admin_role = has_admin_role(message)

#            for x in admin_ids:
#                admin_role = discord.utils.get(message.author.roles, id=x)

            if message.channel.name == 'general' or message.channel.name != 'general' or message.author != discord.User.bot:
                if message.content == '.test respond':
                    ctx = await self.bot.get_context(message)
                    await message.channel.send(f'this message was sent in {message.channel} and admin_roles = {has_admin_role(message)} and {discord.ClientUser.id} and {ctx.guild.member_count}')
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
                    return

                elif message.content == 'am i admin':
                    if admin_role is True:
                        await message.channel.send('yo you are admin')
                    else:
                        await message.channel.send('L your are not admin')

                elif banned_words(message) is True:
                    await message.delete()
                    await message.channel.send(f"smh saying bad words {message.author.mention}", delete_after=5.0)
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="Welcome!", url="https://discord.com/channels/834037980883582996/878418546265313310/883713010768691273",
                              description=f"Welcome to Brads server, {member}! Please feel free to send a couple memes, cute pet photo's or intresting facts.", color=colour["green"])
        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/867713807291908137/02e63019fc51f3ea2735f2e2d7acc49b.png?size=256")
        embed.add_field(name="Please make sure to to read and accept the rules to gain access to all other channels open to members", value="\uFEFF", inline=False)
        embed.add_field(name="Please don't promote any Other charity's or ask for us to get server members to go to any other server or website", value="Apart from all that, have fun :D", inline=True)
        await member.send(embed=embed)
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



def setup(bot):
    bot.add_cog(Events(bot))
