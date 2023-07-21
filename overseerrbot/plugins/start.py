from pyrogram import filters
from pyrogram.types import Message

from overseerrbot import OverseerrBot


@OverseerrBot.on_message(filters.command('start'))
async def start(_, message: Message):
    await message.reply('Hello!')
