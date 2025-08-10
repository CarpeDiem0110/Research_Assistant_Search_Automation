import os 

from dotenv import load_dotenv

from TelegramBot import TelegramBot

from Scrapping import Scraping

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")



bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)


Scraper = Scraping(bot)


try:
    Scraper.scrape_and_notify(pages=2) 
finally: 
    Scraper.close_driver()