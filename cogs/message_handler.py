import asyncio
import re

import discord
from discord.ext import commands


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        elif message.channel.id not in self.bot.channel_data:
            return
        await self.handle_sharps(message)

    def shorten(self, text: str, length: int) -> str:
        if len(text) <= length - 3:
            return text
        return text[: length - 3] + "..."

    def format_md(self, text):
        return re.sub(r"<!--[\s\S]*-->", "", text).replace("\n", " ")

    async def handle_sharps(self, message: discord.Message):
        tasks = []
        for match in re.finditer(r"(?!<=<)(\d+)(?!=>)", message.content):
            issue_number = int(match.group(1))
            tasks.append(self.check_issue(message.channel, issue_number))
        result = [
            f"<{r['html_url']}>: "
            f"**{discord.utils.escape_markdown(r['title'])}** "
            f"{discord.utils.escape_markdown(self.shorten(self.format_md(r['body']), 20))}"
            for r in await asyncio.gather(*tasks)
            if r
        ]
        if result:
            await message.reply("\n".join(result))

    async def check_issue(self, channel: discord.TextChannel, issue_number: int):
        channel_data = self.bot.channel_data[channel.id]
        if data := channel_data["issues"].get(str(issue_number)):
            return data
        async with self.bot.session.get(
            f"https://api.github.com/repos/{channel_data['user']}/{channel_data['repo']}/issues/{issue_number}"
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                channel_data["issues"][str(data["number"])] = data
                return data
            else:
                return False


def setup(bot):
    bot.add_cog(MessageHandler(bot))
