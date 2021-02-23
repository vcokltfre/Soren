from templatebot import Bot
from datetime import datetime

from src.utils.loader import load

config = load()

bot = Bot(name="Soren", command_prefix=config.get("prefix", "~"), logging_url=config.get("logs", None))
bot.started_at = datetime.utcnow()
bot.load_initial_cogs()

bot.run(config.get("token"))