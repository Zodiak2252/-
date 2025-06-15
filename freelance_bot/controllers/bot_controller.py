from telebot import TeleBot, types
from views.telegram_view import TelegramView
from models.service import Service
from models.order import Order
import traceback

class BotController:
    def __init__(self, token):
        self.bot = TeleBot(token)
        self.view = TelegramView(self.bot)
        self.services = self._init_services()
        self.user_state = {}
        self._register_handlers()

    def _init_services(self):
        return [
            Service("design", "Дизайн", 3000, "Логотипы, баннеры", {"simple": 1.0, "medium": 1.5}),
            Service("programming", "Программирование", 5000, "Сайты, боты", {"simple": 1.0, "hard": 2.0})
        ]

    def _register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.view.show_main_menu(message.chat.id)

        @self.bot.message_handler(func=lambda msg: msg.text == "📋 Каталог услуг")
        def show_services(message):
            try:
                self.view.show_services(message.chat.id, self.services)
            except Exception as e:
                self._handle_error(message.chat.id, "show_services", e)

        @self.bot.message_handler(func=lambda msg: msg.text == "📂 Портфолио")
        def show_portfolio(message):
            try:
                examples = [
                    "• Логотип для кафе (пример: example.com/logo1)",
                    "• Дизайн сайта (пример: example.com/site1)"
                ]
                self.view.show_portfolio(message.chat.id, examples)
            except Exception as e:
                self._handle_error(message.chat.id, "show_portfolio", e)

        @self.bot.message_handler(func=lambda msg: msg.text == "❓ FAQ")
        def show_faq(message):
            try:
                faq_items = [
                    "1. Как заказать? - Через каталог услуг",
                    "2. Цены? - От 3000 руб. за простые задачи"
                ]
                self.view.show_faq(message.chat.id, faq_items)
            except Exception as e:
                self._handle_error(message.chat.id, "show_faq", e)

        @self.bot.message_handler(func=lambda msg: msg.text == "🎁 Реферальная программа")
        def show_referral(message):
            try:
                ref_link = f"https://t.me/{self.bot.get_me().username}?start=ref_{message.chat.id}"
                self.view.show_referral(message.chat.id, ref_link)
            except Exception as e:
                self._handle_error(message.chat.id, "show_referral", e)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(("service_", "complexity_", "urgency_")))
        def handle_callback(call):
            try:
                if call.data.startswith("service_"):
                    self._handle_service_selection(call)
                elif call.data.startswith("complexity_"):
                    self._handle_complexity(call)
                elif call.data.startswith("urgency_"):
                    self._handle_urgency(call)
            except Exception as e:
                self._handle_error(call.message.chat.id, "callback", e)

    def _handle_service_selection(self, call):
        service_id = call.data.split("_")[1]
        self.user_state[call.from_user.id] = {"service_id": service_id}
        self.view.show_complexity_levels(call.message.chat.id, call.message.message_id)

    def _handle_complexity(self, call):
        self.user_state[call.from_user.id]["complexity"] = call.data.split("_")[1]
        self.view.show_urgency_options(call.message.chat.id, call.message.message_id)

    def _handle_urgency(self, call):
        user_id = call.from_user.id
        self.user_state[user_id]["urgency"] = float(call.data.split("_")[1])
        
        service = next(s for s in self.services if s.id == self.user_state[user_id]["service_id"])
        complexity = self.user_state[user_id]["complexity"]
        urgency = self.user_state[user_id]["urgency"]
        
        price = int(service.base_price * service.complexity_levels[complexity] * urgency)
        
        self.bot.send_message(
            call.message.chat.id,
            f"💼 Вы выбрали:\n\n"
            f"Услуга: {service.name}\n"
            f"Сложность: {complexity}\n"
            f"Срочность: {urgency}x\n"
            f"Примерная цена: {price} руб.\n\n"
            "✍️ Теперь опишите детали заказа:"
        )
        
        self.bot.register_next_step_handler_by_chat_id(
            call.message.chat.id,
            lambda m: self._finalize_order(m, user_id, service, complexity, urgency)
        )

    def _finalize_order(self, message, user_id, service, complexity, urgency):
        try:
            price = int(service.base_price * service.complexity_levels[complexity] * urgency)
            
            self.bot.send_message(
                message.chat.id,
                f"✅ Заказ оформлен!\n\n"
                f"Услуга: {service.name}\n"
                f"Цена: {price} руб.\n"
                f"Ваши пожелания:\n{message.text}\n\n"
                "Спасибо за заказ!",
                reply_markup=self.view.create_main_menu()
            )
            
            # Здесь можно сохранить заказ в базу данных
            self.user_state.pop(user_id, None)
            
        except Exception as e:
            self._handle_error(message.chat.id, "finalize_order", e)
            self.view.show_main_menu(message.chat.id)

    def _handle_error(self, chat_id, handler_name, error):
        print(f"Ошибка в {handler_name}: {traceback.format_exc()}")
        self.bot.send_message(chat_id, "🔧 Произошла техническая ошибка. Попробуйте позже.")
        self.view.show_main_menu(chat_id)

    def run(self):
        print("Бот работает")
        while True:
            try:
                self.bot.polling(none_stop=True, interval=1, timeout=30)
            except Exception as e:
                print(f"Ошибка polling: {traceback.format_exc()}")
                continue