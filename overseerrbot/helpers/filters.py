from pyrogram.filters import *


def callback_query(arg: str, payload=True):
    """
    Accepts arg at all times.
    if payload is True, extract payload from callback and assign to callback.payload
    if payload is False, only check if callback exactly matches argument
    """

    async def func(flt, __, query: CallbackQuery):
        if payload:
            thing = r"\b{}\b\+"
            if re.search(re.compile(thing.format(flt.data)), query.data):
                search = re.search(re.compile(r"\+{1}(.*)"), query.data)
                if search:
                    query.payload = search.group(1)
                else:
                    query.payload = None

                return True

            return False
        else:
            if flt.data == query.data:
                return True

            return False

    return create(func, "CustomCallbackQueryFilter", data=arg)
