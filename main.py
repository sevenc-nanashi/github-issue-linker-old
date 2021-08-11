import os

# import discord
from dotenv import load_dotenv

from bot import GitHubIssueLinker

load_dotenv()
bot = GitHubIssueLinker()
channel_pairs = bot.db["channel-pairs"]

bot.load_extension("cogs.commands_handler")
bot.load_extension("cogs.db_handler")
bot.load_extension("cogs.message_handler")
bot.load_extension("cogs.slash_handler")
bot.run(os.getenv("TOKEN"))
