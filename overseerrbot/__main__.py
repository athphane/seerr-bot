import overseerrbot
from overseerrbot import OverseerrBot

if __name__ == '__main__':
    overseerrbot.client = OverseerrBot
    OverseerrBot.run()