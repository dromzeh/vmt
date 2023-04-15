import io
import json

import discord
from discord.ext import commands
import pydub
import speech_recognition as sr
import deepl


class Transcriber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def load_config(self):
        with open("config/config.json") as conf_file:
            return json.load(conf_file)

    # transcribe / translate command
    @commands.command(aliases=["t", "translate", "tr", "trans"])
    async def transcribe(self, ctx, *, translate_to=None): # takes an optional argument, translate_to, which is the language code to translate the transcribed text to.
        # check if translate_to was passed
        if translate_to is not None:
            translate_to = translate_to.upper()
            language_codes = self.config["language_codes"]
            if translate_to not in language_codes:
                valid_codes = ", ".join([f"`{code}`" for code in language_codes])
                await ctx.reply(
                    f"**Invalid language code.**\n> Valid language codes: {valid_codes}"
                )
                return

        # check if there is a replied message
        replied_message = None
        if ctx.message.reference:
            replied_message = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )

        # if there was no reply attached or if the replied message does not have an attachment, find the most recent message that fits the criteria.
        if not replied_message or (
            replied_message
            and (
                not replied_message.attachments or not replied_message.flags.value >> 13
            )
        ):
            async for message in ctx.channel.history(limit=None, oldest_first=False):
                if (
                    message.author != ctx.bot.user
                    and message.attachments
                    and message.flags.value >> 13
                ):
                    replied_message = message
                    break

        if not replied_message:
            await ctx.reply(
                "You did not reply to a voice message so the bot attempted to find the most recent voice message in the channel. However, no voice message was found."
            )
            return

        author = replied_message.author
        message = await ctx.reply(f"Transcribing the Voice Message from {author}...")

        voice_msg_bytes = await replied_message.attachments[
            0
        ].read()  # read the voice message as bytes
        voice_msg = io.BytesIO(voice_msg_bytes)

        # convert the voice message to a .wav file
        audio_segment = pydub.AudioSegment.from_file(voice_msg)
        wav_bytes = io.BytesIO()
        audio_segment.export(wav_bytes, format="wav")

        # transcribe the audio using Google Speech Recognition API
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_bytes) as source:
            audio_data = recognizer.record(source)

        try:
            transcribed_text = recognizer.recognize_google(audio_data)
            await message.delete()

            embed = discord.Embed(
                color=discord.Color.og_blurple(),
                title=f"🔊 {author.name}'s Voice Message",
            )
            embed.add_field(
                name=f"Transcription", value=f"```{transcribed_text}```", inline=False
            )

            # check if translate_to was passed
            if (
                translate_to is not None
                and transcribed_text
                and translate_to in self.config["language_codes"]
            ):
                # translate the text
                deepl_translator = deepl.Translator(
                    auth_key=self.config["deepl_api_key"]
                )
                translated_text = deepl_translator.translate_text(
                    transcribed_text, target_lang=translate_to
                )
                embed.add_field(
                    name=f"Translation (Into {translate_to.upper()})",
                    value=f"```{translated_text}```",
                    inline=False,
                )

            embed.set_footer(
                text=f"Powered by Google Speech Recognition and DeepL API - requested by {ctx.author}"
            )
            embed_message = await replied_message.reply(
                embed=embed, mention_author=False
            )

        except sr.UnknownValueError:
            await message.edit(
                content=f"Could not transcribe the Voice Message from {author} as the response was empty."
            )

        except Exception as e:
            await message.edit(
                content=f"Could not transcribe the Voice Message from {author} due to an error."
            )
            print(e)


async def setup(bot):
    await bot.add_cog(Transcriber(bot))
