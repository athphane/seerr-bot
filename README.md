# Overseerr Request Management Bot
Simple Telegram bot that will give buttons to approve or decline requests from Overseerr.

## Requirements
- Redis Server
- Python 3.10
- Telegram API details (see https://my.telegram.org)
- Telegram Bot API Token (talk to @botfather on Telegram to get one)
- Overseerr API key 

For the redis server, I created a docker container and used that. 
You can do the same, or install it on your server. 
I've provided a docker-compose file that you can use to get started.

## Installing
Once you get your config.ini file set up, you can run the bot with the following command:
```bash
python -m overseerrbot
```
I do not have a dockerfile for the bot as a whole so this is what you have to do. 

I run my bots in a screen/tmux session so that they will keep running. 

## Credits, and Thanks to
- [Me](https://t.me/athfan) for my mind.