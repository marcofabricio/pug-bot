import asyncio
import os
import time
from random import randint, shuffle

import discord

from .apitoken import TOKEN as TOKEN
from .config import *
from .pug import Pug
from .team import Team
from .utils import *
from .commands import commands

# Get the token from environment variables. Otherwise, get it from the config
TOKEN = os.getenv('TOKEN') if os.getenv('TOKEN') else TOKEN

################################################################
# Bot code
################################################################
# guild_list stores all pug information and is of the form
# {
#     guild: set()
# }
guild_list = {}

# Bot implementation
client = discord.Client()

# Deletes PUGs that are too old
async def check_age():
    while True:
        await asyncio.sleep(1)
        for pugs in guild_list.copy().values():
            for pug in pugs.copy():
                # If a pug has been inactive for more than 30 minutes
                if time.time() - pug.last_action > 1800 and pug.active == 0:
                    await pug.channel.send(f"`{pug.name}` was deleted for inactivity.")
                    if pug.status:
                        await pug.status.delete()
                    pugs.remove(pug)


@client.event
async def on_ready():
    print("Successfully logged in")
    print(f"Username: {client.user.name}")
    print(f"ID: {client.user.id}")
    client.loop.create_task(check_age())


@client.event
async def on_message(message):
    # Prevent the bot from reading its own messages
    if message.author == client.user:
        return

    # Parse the user input
    user_input = {"command": ""}
    if message.content.startswith(f"{prefix}"):
        print("========")
        print(f"Timestamp: {message.created_at}")
        print(f"User: {message.author}")
        print(f"Command: {message.content}")
        print()
        user_input = parse_command(message.content)

    # Add the guild to the guilds list if it's not in it already
    if not message.guild.name in guild_list.keys():
        guild_list[message.guild.name] = set()

    pugs = guild_list[message.guild.name]

    # help is a special case since it takes different parameters
    if user_input["command"] == "help":
        await commands["help"](message, client.user.name)
    elif user_input["command"] in commands.keys():
        await commands[user_input["command"]](message, pugs, user_input, client)

client.run(TOKEN)