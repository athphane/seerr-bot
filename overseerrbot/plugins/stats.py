import json
import sys
from pprint import pprint

from prettytable import PrettyTable
from pyrogram import filters
from pyrogram.types import Message

from overseerrbot import OverseerrBot
from overseerrbot.api.OverseerrApi import OverseerrApi


@OverseerrBot.on_message(filters.command('stats'))
@OverseerrBot.admins_only
async def stats(_, message: Message):
    api = OverseerrApi()
    status = await api.get_requests_count()

    table = PrettyTable()
    table.field_names = ["Status", "Count"]
    table.align = "l"

    for x in status:
        table.add_row([x.title(), status[x]])

    await message.reply(f"```{table}```")
