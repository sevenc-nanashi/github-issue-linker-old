import os

from dotenv import load_dotenv
import requests

load_dotenv()
authorization = {"Authorization": "Bot " + os.getenv("TOKEN")}
application_info = requests.get(
    "https://discord.com/api/v9/oauth2/applications/@me", headers=authorization
).json()
requests.put(
    f"https://discord.com/api/v9/applications/{application_info['id']}/commands",
    headers=authorization,
    json=[
        {
            "name": "login",
            "type": 1,
            "description": "Administrator only: Register GitHub user for the server/guild.",
            "options": [
                {
                    "name": "token",
                    "type": 3,
                    "description": "Your personal GitHub token.",
                    "required": True,
                },
            ],
        },
        {
            "name": "register",
            "type": 1,
            "description": "Manage Channels: Register GitHub repository for the channel.",
            "options": [
                {
                    "name": "user",
                    "type": 3,
                    "description": "Owner of the repository. (Before /)",
                    "required": True,
                },
                {
                    "name": "repo",
                    "type": 3,
                    "description": "Name of the repository. (After /)",
                    "required": True,
                },
            ],
        },
        {
            "name": "unregister",
            "type": 1,
            "description": "Manage Channels: Unregister GitHub repository for the channel.",
        },
        {
            "name": "info",
            "type": 1,
            "description": "Show information of the guild and channel.",
        },
    ],
)
