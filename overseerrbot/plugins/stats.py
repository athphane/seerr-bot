import json
import sys
from pprint import pprint

from pyrogram import filters
from pyrogram.types import Message

from overseerrbot import OverseerrBot
from overseerrbot.api.OverseerrApi import OverseerrApi


@OverseerrBot.on_message(filters.command('stats'))
async def stats(_, message: Message):
    api = OverseerrApi()
    status = await api.get_requests_count()

    response = []
    for x in status:
        response.append(f"{x.title()}: {status[x]}")

    await message.reply("\n".join(response))
