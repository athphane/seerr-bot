import json
import sys
from pprint import pprint

from pyrogram import filters
from pyrogram.types import Message

from overseerrbot import OverseerrBot
from overseerrbot.api.OverseerrApi import OverseerrApi


@OverseerrBot.on_message(filters.command('requests'))
async def send_requests(_, message: Message):
    api = OverseerrApi()
    requests = await api.get_requests()

    for request in requests['results']:
        if request['status'] == 1:
            await message.reply(f"{request['title']} is pending approval.")
