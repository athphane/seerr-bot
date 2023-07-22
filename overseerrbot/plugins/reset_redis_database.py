from pyrogram import filters
from pyrogram.types import Message

from overseerrbot import OverseerrBot
from overseerrbot.redis import RedisDatabase


@OverseerrBot.on_message(filters.command('reset_redis'))
async def reset_redis_database(_, message: Message):
    command = message.command

    if len(command) == 2:
        if command[1] == 'confirm':
            await message.reply('Resetting redis database...')
            redis = RedisDatabase()
            redis.clearDatabase()
            await message.reply('Redis database reset complete!')
        else:
            await message.reply('Please confirm the reset by typing /reset_redis confirm')
    else:
        await message.reply('Please confirm the reset by typing /reset_redis confirm')
