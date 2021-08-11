import os

import aiohttp
import discord
from discord.ext import commands
from motor import motor_asyncio as motor


class GitHubIssueLinker(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=" ", allowed_mentions=discord.AllowedMentions.none()
        )
        self.dbclient = motor.AsyncIOMotorClient(os.getenv("MONGO_URL"))
        self.db = self.dbclient["github_issue_linker"]
        self.guild_data = {}
        self.channel_data = {}
        self._session = aiohttp.ClientSession()

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def on_ready(self):
        print(f"Logged in as {self.user}(ID: {self.user.id})")
