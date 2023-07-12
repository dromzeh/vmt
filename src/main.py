import discord
from discord.ext import commands
import json
import os

with open("config/config.json") as conf_file:
    config = json.load(conf_file)
    bot_token = config["token"]
    bot_prefix = config["prefix"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=bot_prefix, intents=discord.Intents.all())
        # remove the default help command
        self.remove_command("help")

    async def setup_hook(self) -> None:
        cogsLoaded = 0
        cogsCount = 0
        for cog_file in os.listdir("cogs"):
            if cog_file.endswith(".py"):
                cogsCount += 1
                try:
                    print(f"Loading cog {cog_file}...")
                    await self.load_extension(f"cogs.{cog_file[:-3]}")
                    cogsLoaded += 1
                except Exception as e:
                    print(f"Failed to load cog {cog_file}: {e}")
        print(f"Loaded {cogsLoaded}/{cogsCount} cogs.")

    async def on_ready(self):
        print("Bot is ready.")


bot = Bot()
bot.run(bot_token)
