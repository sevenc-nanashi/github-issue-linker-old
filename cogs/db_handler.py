# import discord
from discord.ext import commands, tasks


class DbHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fired_ready = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.fired_ready:
            return
        self.fired_ready = True
        async for data in self.bot.db.guild_data.find():
            self.bot.guild_data[data["guild_id"]] = data["data"]
        async for data in self.bot.db.channel_data.find():
            self.bot.channel_data[data["channel_id"]] = data["data"]
        self.update_db.start()
        await self.update_db()

    @tasks.loop(minutes=10)
    async def update_db(self):
        for guild, data in self.bot.guild_data.items():
            await self.bot.db.guild_data.update_one(
                {
                    "guild_id": guild,
                },
                {"$set": {"guild_id": guild, "data": data}},
                upsert=True,
            )

        for channel, data in self.bot.channel_data.items():
            await self.bot.db.channel_data.update_one(
                {
                    "channel_id": channel,
                },
                {"$set": {"channel_id": channel, "data": data}},
                upsert=True,
            )

    def cog_unload(self):
        self.update_db.stop()


def setup(bot):
    bot.add_cog(DbHandler(bot))
