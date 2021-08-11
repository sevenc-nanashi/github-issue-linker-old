from discord import Interaction
from discord.ext import commands


class CommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def login(self, interaction: Interaction, token):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
        await interaction.response.defer(ephemeral=True)
        async with self.bot.session.get(
            "https://api.github.com/user",
            headers={"authorization": "Token " + token.value},
        ) as response:
            if response.status != 200:
                return await interaction.followup.send("Invalid token.", ephemeral=True)
            user = await response.json()
        self.bot.guild_data[interaction.guild.id] = {
            "token": token.value,
            "user": user,
        }
        await interaction.followup.send(
            f"Successfully logged in as [{user['name']}(`{user['login']}`)]({user['html_url']}).",
            ephemeral=True,
        )

    @commands.command()
    async def register(self, interaction: Interaction, user, repo):
        if not interaction.channel.permissions_for(interaction.user).manage_channels:
            return await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
        await interaction.response.defer(ephemeral=True)
        guild_data = self.bot.guild_data.get(interaction.guild.id)
        if not guild_data:
            return await interaction.followup.send("No token found.", ephemeral=True)
        token = guild_data["token"]
        async with self.bot.session.get(
            f"https://api.github.com/repos/{user.value}/{repo.value}",
            headers={"authorization": "Token " + token},
        ) as response:
            if response.status != 200:
                return await interaction.followup.send(
                    "Failed to fetch repository.", ephemeral=True
                )
            data = await response.json()
        self.bot.channel_data[interaction.channel.id] = {
            "user": user.value,
            "repo": repo.value,
            "issues": {},
            "data": data,
        }
        await interaction.followup.send(
            f"Successfully registered repository with [{user.value}/{repo.value}]({data['html_url']}).",
            ephemeral=True,
        )

    @commands.command()
    async def unregister(self, interaction: Interaction):
        if not interaction.channel.permissions_for(interaction.user).manage_channels:
            return await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
        if str(interaction.channel.id) not in self.bot.channel_data:
            return await interaction.response.send_message(
                "No registered repository found.", ephemeral=True
            )
        del self.bot.channel_data[str(interaction.channel.id)]
        await interaction.response.send_message(
            "Successfully unregistered repository.", ephemeral=True
        )

    @commands.command()
    async def info(self, interaction: Interaction):
        if interaction.guild.id not in self.bot.guild_data:
            return await interaction.response.send_message(
                "No data found.", ephemeral=True
            )
        guild_data = self.bot.guild_data[interaction.guild_id]
        channel_data = self.bot.channel_data.get(interaction.channel_id)
        result = ""

        token_user = guild_data["user"]
        result += (
            "**Guild Data**\n"
            f"Token: [{token_user['name']}(`{token_user['login']}`)]({token_user['html_url']})\n\n"
        )
        if channel_data:
            result += (
                "**Channel Data**\n"
                f"Repository: [{channel_data['user']}/{channel_data['repo']}]({channel_data['data']['html_url']})"
            )
        else:
            result += "**Channel Data**\nNone"

        await interaction.response.send_message(result, ephemeral=True)


def setup(bot):
    bot.add_cog(CommandsCog(bot))
