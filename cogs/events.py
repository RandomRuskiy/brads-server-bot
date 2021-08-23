import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from lib.colours import BasicColours as colour

# self.spam_control = commands.CooldownMapping.from_cooldown()

client = commands.Bot(command_prefix='£')

# owner_id = [645647583141822466, 683733441728217098]
# owner_id = 683733441728217098
admin_ids = [835960034331590666, 842689593052889098, 868107974655238185, 879381563740147763]


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user or message.author != discord.User.bot:  # only respond if user is not self or another bot

            admin_role = None
            for int in admin_ids:
                admin_role = discord.utils.get(message.author.roles, id=admin_ids)

            if message.channel.name == 'general' or message.channel.name != 'general':
                if message.content == '.test respond':
                    await message.channel.send(f'this message was sent in {message.channel} and admin_roles = {admin_role}')
                    return

                elif message.content == 'yo im saying something':
                    await message.channel.send('yo im responding')
                    return

                elif message.content == 'meaning of O_O':
                    await message.channel.send('Brad is shocked or ran out of things to say lmao')
                    return

                elif message.content == 'yo':
                    ctx = await self.bot.get_context(message)
                    await message.channel.send(f'yo {ctx.author.mention}')
                    return

                elif message.content == 'Yo':
                    ctx = await self.bot.get_context(message)
                    await message.channel.send(f'yo {ctx.author.mention}')
                    return

                elif message.content == 'L':
                    await message.channel.send('L')
                    return

                elif admin_role is not None:
                    if message.content == 'am i admin':
                        await message.channel.send('yo you are admin')
                        return

                elif admin_role is None:
                    if message.content == 'am i admin':
                        await message.channel.send('L you are not admin')
                        return
                else:
                    return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="Welcome!", url="https://discord.com/channels/834037980883582996/835126673921409024/851815264064372747",
                              description=f"Welcome to Brads server, {member}! Dont be afraid to send a couple memes, an image of your pet or even a bad pun :)", color=colour["green"])
        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/867713807291908137/02e63019fc51f3ea2735f2e2d7acc49b.png?size=256")
        embed.add_field(name="Please make sure to read the rules (you can go to the channel by clicking the link above)", value="\nApart from all that, make sure to also enjoy yourself!", inline=False)
        embed.add_field(name="If you have any questions, you can ask any admin and they should be of help.", value="\uFEFF", inline=True)
        await member.send(embed=embed)

        # list events as empty commands so people can see what auto-responses exist which will be shown in the help page
    @commands.command(
        name='Auto-Responses',
        description='Everything listed within the `Events` section are the words that the bot will respond to.'
    )
    @commands.is_owner()
    async def responseplaceholder(self, ctx):
        return

    @commands.command(
        name='meaning of O_O',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def meaningplaceholder(self, ctx):
        return

    @commands.command(
        name='yo',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def yo1placeholder(self, ctx):
        return

    @commands.command(
        name='Yo',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def yo2placeholder(self, ctx):
        return

    @commands.command(
        name='L',
        description='\uFEFF'
    )
    @commands.is_owner()
    async def lplaceholder(self, ctx):
        return


def setup(bot):
    bot.add_cog(Events(bot))
