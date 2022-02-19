import asyncio
import os

import discord
import pymongo
from discord.ext import commands
from pymongo import MongoClient

from __main__ import logger

cluster = MongoClient(os.getenv('MONGO_CONNECTION_URL'))

db = cluster['UserData']

collection = db['UserData']


class Db(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')

    def post(post_data: dict):
        mq = {"_id": post_data['_id']}
        if (collection.count_documents(mq) == 0):
            collection.insert_one(post_data)
        else:
            q = {"_id": post_data['_id']}
            user = collection.find(q)
            for r in user:
                score = r['score']
            score = score + 1
            test = post_data['is_admin']
            collection.update_one({"_id": post_data['_id']}, {"$set": {"score": score}})
            collection.update_one({"_id": post_data['_id']}, {"$set": {"is_admin": test}})
        logger.info(f'Posted data to DB! Data: "{post_data}"')


def setup(bot):
    bot.add_cog(Db(bot))
