import discord
from discord.ext import commands
import json
from cogs.slash import guild_ids, client
import time
import datetime

birthdayNotifChannel = None
birthdayList = None # json file to store dates

class BirthdayStore():
    def __init__(self, timestamp: int, user: discord.Member):
        self.timestamp = timestamp
        self.user = user

    def saveDate(self):
        return

    def removeDate(self):
        return

    def getDate(self):
        return

class BirthdayNotif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    @client.slash_command(
            name='birthday',
            description='Manage the birthday notifications.',
            guild_ids=guild_ids
            )
    @discord.option(name='next', description='View the next upcoming birthday')
    @discord.option(name='list', description='List any upcoming birthdays')
    @discord.option(name='stats', description='Show the current stats')
    async def birthday(self):
        # MAKE SURE ANY str() FORM DATES ARE IN DD/MM/YYYY (for now atleast)    
        return

def setup(bot):
    bot.add_cog(BirthdayNotif(bot))
