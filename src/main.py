from database import feed
import asyncio
import threading
from bot import Bot

if __name__ == '__main__':
    bot = Bot()
    bot.start()
    bot.get_stats()