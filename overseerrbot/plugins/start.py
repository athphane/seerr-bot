from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from overseerrbot import OverseerrBot


@OverseerrBot.on_message(filters.command('start'))
async def start(_, message: Message):
    if OverseerrBot().is_admin(message):
        await message.reply(
            f"Hello {OverseerrBot().user_mentionable(message)}! I am SeerrBot. I can help you manage your "
            f"Overseerr and Jellyseerr requests.")
    else:
        await message.reply('Hello! I am useless. But check out this video.', reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click Here", url="https://youtu.be/dQw4w9WgXcQ")]]
        ))
