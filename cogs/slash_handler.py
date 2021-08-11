import discord
from discord.ext import commands


class CommandOption:
    def __init__(self, option):
        self.name = option["name"]
        self.type = option["type"]
        self.value = option["value"]

    def __getattr__(self, name):
        try:
            return super.__getattr__(name)
        except AttributeError:
            return getattr(self.value, name)


class CommandInteraction:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction

    @property
    def name(self):
        return self.interaction.data["name"]

    @property
    def options(self):
        return map(CommandOption, self.interaction.data.get("options", []))

    def __getattr__(self, name):
        try:
            return super.__getattr__(name)
        except AttributeError:
            return getattr(self.interaction, name)

    def __dir__(self):
        return dir(self.interaction) + super()


class CommandHandlerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, raw_interaction: discord.Interaction):
        if raw_interaction.type == discord.InteractionType.application_command:
            interaction: CommandInteraction = CommandInteraction(raw_interaction)
            command: commands.Command = self.bot.get_command(interaction.name)
            await command(interaction, *interaction.options)


def setup(bot):
    bot.add_cog(CommandHandlerCog(bot))
