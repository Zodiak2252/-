from telebot import types

class TelegramView:
    def __init__(self, bot):
        self.bot = bot

    def show_main_menu(self, chat_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["📋 Каталог услуг", "📂 Портфолио", "❓ FAQ", "🎁 Реферальная программа"]
        markup.add(*buttons)
        self.bot.send_message(chat_id, "👋 Выберите действие:", reply_markup=markup)

    def show_services(self, chat_id, services):
        markup = types.InlineKeyboardMarkup()
        for service in services:
            markup.add(types.InlineKeyboardButton(
                f"{service.name} ({service.base_price} руб.)",
                callback_data=f"service_{service.id}"
            ))
        self.bot.send_message(chat_id, "🎨 Выберите услугу:", reply_markup=markup)

    def show_portfolio(self, chat_id, examples):
        text = "🖼 Примеры работ:\n\n" + "\n".join(examples)
        self.bot.send_message(chat_id, text)

    def show_faq(self, chat_id, faq_items):
        text = "❓ Частые вопросы:\n\n" + "\n".join(faq_items)
        self.bot.send_message(chat_id, text)

    def show_referral(self, chat_id, ref_link):
        text = f"🎁 Реферальная программа\n\nПригласите друзей по ссылке:\n{ref_link}\n\nЗа каждого друга - бонус 10%!"
        self.bot.send_message(chat_id, text, disable_web_page_preview=True)

    def show_complexity_levels(self, chat_id, message_id):
        markup = types.InlineKeyboardMarkup()
        for level in ["simple", "medium", "hard"]:
            markup.add(types.InlineKeyboardButton(
                level.capitalize(),
                callback_data=f"complexity_{level}"
            ))
        self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="⚙️ Выберите уровень сложности:",
            reply_markup=markup
        )

    def show_urgency_options(self, chat_id, message_id):
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("Стандарт (1x)", callback_data="urgency_1.0"),
            types.InlineKeyboardButton("Срочно (1.5x)", callback_data="urgency_1.5")
        )
        markup.add(types.InlineKeyboardButton("Очень срочно (2x)", callback_data="urgency_2.0"))
        
        self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="⏱ Выберите срочность выполнения:",
            reply_markup=markup
        )

    def create_main_menu(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📋 Каталог услуг", "📂 Портфолио", "❓ FAQ", "🎁 Реферальная программа")
        return markup