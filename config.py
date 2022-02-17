import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

PG_DATABASE_URL = os.getenv("PG_DATABASE_URL")

REDIS_URL = os.getenv("REDIS_URL")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


