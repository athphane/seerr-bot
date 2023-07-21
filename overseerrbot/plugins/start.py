import json
import sys
from pprint import pprint

from pyrogram import filters
from pyrogram.types import Message

from overseerrbot import OverseerrBot
from overseerrbot.api.OverseerrApi import OverseerrApi


@OverseerrBot.on_message(filters.command('start'))
async def start(_, message: Message):
    # make request to overseerr api status endpount
    # if status is 200, then reply with "I'm alive!"
    # else reply with "I'm dead!"

    api = OverseerrApi()
    status = await api.get_requests()

    with open('output.json', 'w+') as file:
        file.write(json.dumps(status, indent=4))
