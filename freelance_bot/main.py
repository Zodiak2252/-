from controllers.bot_controller import BotController
from config import BOT_TOKEN

if __name__ == "__main__":
    bot = BotController(BOT_TOKEN)
    bot.run()