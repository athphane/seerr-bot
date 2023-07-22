from io import BytesIO

from PIL import Image
from pyrogram import emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from overseerrbot import OverseerrBot
from overseerrbot.api.OverseerrApi import OverseerrApi
from overseerrbot.helpers import filters
from overseerrbot.redis import RedisDatabase


@OverseerrBot.on_message(filters.command('requests'))
@OverseerrBot.admins_only
async def send_requests(_, message: Message):
    api = OverseerrApi()
    redis = RedisDatabase()
    new_requests_sent = False
    media_requests = await api.get_requests()

    for media_request in media_requests['results']:
        if media_request['status'] == 1:
            request_id = media_request['id']
            media_id = media_request['media']['tmdbId']
            media_type = media_request['type'].lower()

            if not redis.checkIfSent(media_request['id']):
                media_details = await api.get_media_details(media_type, media_id)
                poster_binary = await api.get_poster(media_details['posterPath'])
                poster = BytesIO(poster_binary)

                name = ''
                if 'name' in media_details:
                    name = media_details['name']
                elif 'title' in media_details:
                    name = media_details['title']

                buttons = [
                    [
                        InlineKeyboardButton(f"{emoji.CHECK_MARK_BUTTON} Approve Request",
                                             callback_data=f"approve_request+{request_id}"),
                    ],
                    [
                        InlineKeyboardButton(f"{emoji.STOP_SIGN} Deny Request",
                                             callback_data=f"deny_request+{request_id}"),
                    ]
                ]

                caption = (
                    f"{name} is pending approval.\n\n"
                    f"Requested By: {media_request['requestedBy']['displayName']}\n"
                )

                message = await message.reply_photo(
                    photo=poster,
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )

                if message.id:
                    new_requests_sent = True
                    redis.markAsSent(media_request['id'])
            else:
                print('Already sent.')

    if not new_requests_sent:
        await message.reply('No new requests.')


@OverseerrBot.on_callback_query(filters.callback_query('approve_request'))
@OverseerrBot.admins_only
async def approve_request(bot: OverseerrBot, callback: CallbackQuery):
    request_id = callback.data.split('+')[1]
    api = OverseerrApi()
    try:
        await api.approve_request(int(request_id))
        await callback.message.edit_caption("This media request has been approved!")

    except Exception as e:
        print(e)
        await callback.answer("Error approving request.", show_alert=True)
        return

    await callback.answer("Request Approved")


@OverseerrBot.on_callback_query(filters.callback_query('deny_request'))
@OverseerrBot.admins_only
async def deny_request(bot: OverseerrBot, callback: CallbackQuery):
    request_id = callback.data.split('+')[1]
    api = OverseerrApi()
    try:
        await api.deny_request(int(request_id))
        await callback.message.edit_caption("This media request has been rejected!")

    except Exception as e:
        print(e)
        await callback.answer("Error rejecting request.", show_alert=True)
        return

    await callback.answer("Request Rejected")
