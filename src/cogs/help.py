import discord
from discord.ext import commands
import json


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def load_config(self):
        with open("config/config.json") as conf_file:
            return json.load(conf_file)

    # help command
    @commands.command(aliases=["h"])
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help Menu",
            description="List of all available commands:",
            color=discord.Color.og_blurple(),
        )

        embed.add_field(
            name="**Translate / Transcribe**",
            value=f"\n> Transcribes (& Translates) a voice message into text.\n > Usage: `{self.config['prefix']}transcribe [language_code (optional)]`\n *You can either reply to the voice message running the command or the bot will find the most recent voice message in the channel.*",
            inline=False,
        )

        embed.add_field(
            name="**Language Codes**",
            value=f"> List of available language codes.\n > Usage: `{self.config['prefix']}languages`\n*Current Supported Languages: {len(self.config['language_codes'])}*",
            inline=False,
        )

        embed.add_field(
            name="**Help**",
            value=f"> Shows this help menu.\n > Usage: `{self.config['prefix']}help`",
            inline=False,
        )

        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
