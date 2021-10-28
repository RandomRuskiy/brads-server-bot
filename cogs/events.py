import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from lib.colours import BasicColours as colour
from cogs.slash import bot_user

# self.spam_control = commands.CooldownMapping.from_cooldown()

client = commands.Bot(
    command_prefix='£',
    debug_guild=875804519605370911
)

# owner_id = [645647583141822466, 683733441728217098]
# owner_id = 683733441728217098
admin_ids = [835960034331590666, 842689593052889098, 868107974655238185, 879381563740147763]


def is_bot(message):
    if message.author == bot_user:
        return True
    elif message.author.bot is True:
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
                    await message.channel.send(f'this message was sent in {message.channel} and admin_roles = {has_admin_role(message)} and {discord.ClientUser.id}')
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
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''embed = discord.Embed(title="Welcome!", url="https://discord.com/channels/834037980883582996/835126673921409024/851815264064372747",
                              description=f"Welcome to Brads server, {member}! Dont be afraid to send a couple memes, an image of your pet or even a bad pun :)", color=colour["green"])
        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/867713807291908137/02e63019fc51f3ea2735f2e2d7acc49b.png?size=256")
        embed.add_field(name="Please make sure to read the rules (you can go to the channel by clicking the link above)", value="\nApart from all that, make sure to also enjoy yourself!", inline=False)
        embed.add_field(name="If you have any questions, you can ask any admin and they should be of help.", value="\uFEFF", inline=True)
        await member.send(embed=embed)'''
        pass


def setup(bot):
    bot.add_cog(Events(bot))
