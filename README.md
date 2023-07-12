# VMT - Discord Voice Message Transcriber and Translator

[![License: MIT](https://img.shields.io/badge/license-MIT-blueviolet.svg)](https://github.com/dromzeh/vmt)
[![Formatter: Black](https://img.shields.io/badge/formatter-Black-lightgrey.svg)](https://black.readthedocs.io/en/stable/)

A Discord bot that can transcribe and translate Discord Voice Messages.

- Uses the DeepL API for translation and Google's Speech Recognition API for transcription.

## Requirements

- Python 3.8+
- discord.py
- pydub
- speech recognition
- deepl

Run the following:

```bash
pip install -r requirements.txt
```

## Installation

> **Note**
> Bot requires Intents to be enabled in the developer portal & an API key for the DeepL API.

- Clone the repository: `git clone https://github.com/dromzeh/vmt.git`
- Rename the `config.example.json` file to `config.json` inside `src/config` and fill in the necessary values (See [Configuration](#configuration)) 

Once the configuration file has been filled, you may run the bot using one of the following methods:

### Native Installation

- Install the requirements `pip install -r requirements.txt`
- Run the bot inside the `/src` folder: `python main.py`

### Docker Installation (Easier)

Assuming `docker` and `docker-compose` are installed

```bash
docker-compose -f compose.yaml up
```

## Usage

- To use the bot, simply reply to a voice message with the `transcribe` command. The bot will transcribe the voice message and post the transcription as a reply, if you don't reply, the bot will find the most recent voice message in the channel and transcribe it instead.
- If you want to automatically translate the text, you can just add the language code as an argument, such as : `vmt transcribe es` for Spanish, full list is available at `vmt languages` or [here](#language-code-list).
- The bot will then automatically translate the text using the DeepL API.

### Configuration

The config.json file contains the following fields:

- `discord_token`: Your Discord bot token.
- `deepl_api_key`: Your DeepL API key.
- `language_codes`: A dictionary of language codes and their corresponding language names.

### Language Code List

<details>
<summary>Click to expand</summary>

```js
    "language_codes": {
        "BG": "Bulgarian",
        "CS": "Czech",
        "DA": "Danish",
        "DE": "German",
        "EL": "Greek",
        "EN-GB": "English (British)",
        "EN-US": "English (American)",
        "ES": "Spanish",
        "ET": "Estonian",
        "FI": "Finnish",
        "FR": "French",
        "HU": "Hungarian",
        "ID": "Indonesian",
        "IT": "Italian",
        "JA": "Japanese",
        "KO": "Korean",
        "LT": "Lithuanian",
        "LV": "Latvian",
        "NB": "Norwegian (Bokmål)",
        "NL": "Dutch",
        "PL": "Polish",
        "PT-BR": "Portuguese (Brazilian)",
        "PT-PT": "Portuguese",
        "RO": "Romanian",
        "RU": "Russian",
        "SK": "Slovak",
        "SL": "Slovenian",
        "SV": "Swedish",
        "TR": "Turkish",
        "UK": "Ukrainian",
        "ZH": "Chinese (simplified)"
    }
```

</details>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
