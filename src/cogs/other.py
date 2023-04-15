import discord
from discord.ext import commands
import json


class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def load_config(self):
        with open("config/config.json") as conf_file:
            return json.load(conf_file)

    # language codes command
    @commands.command(aliases=["langcodes", "lc", "languages"])
    async def language_codes(self, ctx):
        embed = discord.Embed(
            title="Language Codes",
            description="List of available language codes:",
            color=discord.Color.og_blurple(),
        )

        for language in self.config["language_codes"]:
            embed.add_field(
                name=f"**{self.config['language_codes'][language]}**", 
                value=f"`{language}`",
                inline=True,
            )

        embed.set_footer(
            text="Note: You can use these codes to translate the transcribed text into a different language, translation powered by DeepL."
        )
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(OtherCommands(bot))
