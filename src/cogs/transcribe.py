import io
import json
import typing

import discord
from discord.ext import commands
import pydub
import speech_recognition as sr
import deepl
import textwrap


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
        if not msg_has_voice_note(replied_message):
            async for message in ctx.channel.history(limit=None, oldest_first=False):
                if message.author != ctx.bot.user and msg_has_voice_note(message):
                    replied_message = message
                    break

        if not replied_message:
            await ctx.reply(
                "You did not reply to a voice message so the bot attempted to find the most recent voice message in the channel. However, no voice message was found."
            )
            return

        author = replied_message.author

        response = await ctx.reply(f"Transcribing the Voice Message from {author}...")
        try:
            transcribed_text = await transcribe_msg(replied_message)
            await response.delete()

        except sr.UnknownValueError as e:
            await response.edit(
                content=f"Could not transcribe the Voice Message from {author} as the response was empty."
            )
            return

        except Exception as e:
            await response.edit(
                content=f"Could not transcribe the Voice Message from {author} due to an error."
            )
            print(e)
            return

        translated_text = None
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

        embed = make_embed(transcribed_text, author, ctx.author, translate_to, translated_text)


        embed_message = await replied_message.reply(
            embed=embed, mention_author=False
        )

    @commands.Cog.listener("on_message")
    async def auto_transcribe(self, msg: discord.Message):
        if not msg_has_voice_note(msg): return

        await msg.add_reaction("\N{HOURGLASS}")
        try:
            transcribed_text = await transcribe_msg(msg)
            embed = make_embed(transcribed_text, msg.author)
            await msg.reply(embed = embed)

        except sr.UnknownValueError as e:
            await msg.reply(
                content=f"Could not transcribe the Voice Message from {msg.author} as the response was empty."
            )
        except Exception as e:
            await msg.edit(
                content=f"Could not transcribe the Voice Message from {msg.author} due to an error."
            )
            print(e)
        await msg.remove_reaction("\N{HOURGLASS}", self.bot.user)


def make_embed(transcribed_text, author, ctx_author = None, translate_to = None, translated_text = None):
        embed = discord.Embed(
            color=discord.Color.og_blurple(),
            title=f"🔊 {author.name}'s Voice Message",
        )
        embed.add_field(
            name=f"Transcription",
            value= textwrap.dedent(
            f"""
            ```
            {transcribed_text}
            ```
            [vmt bot](https://github.com/dromzeh/vmt) by [@strazto](https://instagram.com/strazto) & [@dromzeh](https://github.com/dromzeh)
            """),
            inline=False
        )

        if translate_to and translated_text:
            embed.add_field(
                name=f"Translation (Into {translate_to.upper()})",
                value=f"```{translated_text}```",
                inline=False,
            )

        if ctx_author:
            embed.set_footer(text=f"Transcribe requested by {ctx_author}")

        return embed


def msg_has_voice_note(msg: typing.Optional[discord.Message]) -> bool:
    if not msg: return False
    if not msg.attachments or not msg.flags.value >> 13: return False
    return True

async def transcribe_msg(msg: typing.Optional[discord.Message]) -> typing.Optional[typing.Union[typing.Any,list,tuple]]:
        if not msg_has_voice_note(msg): return None

        voice_msg_bytes = await msg.attachments[
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

        except sr.UnknownValueError as e:
            raise e

        except Exception as e:
            raise e

        return transcribed_text


async def setup(bot):
    await bot.add_cog(Transcriber(bot))
