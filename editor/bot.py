import telebot  # pip install pyTelegramBotAPI
from telebot import types
from bot_message import *
from config import TOKEN


class Bot:
    """Класс Telegram-бота с игрой."""
    def __init__(self, token, start_message):
        """Создаёт Telegram-бота с указанным токеном и сценарием.

        Параметры:
        token - токен бота
        start_message - первое сообщение игры (тип - Message)
        """
        self.tgbot = telebot.TeleBot(token)
        self.user_table = []  # таблица с записями вида "userid - script - last_message_id"
        self.start_message = start_message

        @self.tgbot.message_handler(commands=['start'])
        def register_new_user(received):
            """Записывает нового игрока в таблицу при нажатии им кнопки "Старт"."""
            if any([user_id == received.from_user.id for user_id, _, _ in self.user_table]):
                return  # данный игрок уже начал игру
            # делаем запись о новом игроке
            print('Идентификатор стартового сообщения:', received.id)
            self.user_table.append([received.from_user.id, self.start_message, received.id])
            print(f'Пользователь {received.from_user.id} начал игру.')
            self.send(received, self.start_message)  # отправляем первое сообщение


        @self.tgbot.message_handler(content_types=['text'])
        def handle_text(received):
            """Обрабатывает текстовые сообщения от игрока."""
            # TODO: в одну функцию
            message = None
            for user_id, prev_message, _ in self.user_table:
                if user_id == received.from_user.id:
                    message = prev_message
                    break
            if message is None:
                # игрок ещё не начал игру (не нажал на "Старт")
                return
            while True:
                message = message.get_next(received.text)  # получаем новые сообщения для отправки
                if message is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(received, message)
                received.text = None


        @self.tgbot.message_handler(content_types=['voice'])
        def handle_voice(received):
            """Обрабатывает голосовые сообщения от игрока."""
            message = None
            for user_id, prev_message, _ in self.user_table:
                if user_id == received.from_user.id:
                    message = prev_message
                    break
            if message is None:
                # игрок ещё не начал игру (не нажал на "Старт")
                return
            while True:
                message = message.get_next(received.voice)  # получаем новые сообщения для отправки
                if message is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(received, message)
                received.voice = None

        @self.tgbot.callback_query_handler(func=lambda call: True)
        def handle_buttons(call):
            """Обрабатывает нажатия на кнопки."""
            message = None
            for user_id, prev_message, last_message_id in self.user_table:
                if user_id == call.from_user.id and last_message_id == call.message.id:
                    message = prev_message
                    break
            if message is None:
                # игрок ещё не начал игру (не нажал на "Старт") или нажал на старые кнопки
                return
            while True:
                message = message.get_next(call.data)  # получаем новые сообщения для отправки
                if message is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(call.message, message)
                call.data = None

        self.tgbot.infinity_polling()  # начинаем слушать бота

    def send(self, received, new_message):
        """Отправляет сообщение в чат.

        Параметры:
        received - полученнное сообщение (тип telebot.Message)
        new_message - сообщение для отправки (тип bot_message.Message)
        """
        if isinstance(new_message, TextMessage):
            sent = self.tgbot.send_message(received.chat.id, new_message.content)
        elif isinstance(new_message, ImageMessage):
            sent = self.tgbot.send_photo(received.chat.id, new_message.content)
        elif isinstance(new_message, VideoMessage):
            sent = self.tgbot.send_video(received.chat.id, new_message.content)
        elif isinstance(new_message, VoiceMessage):
            sent = self.tgbot.send_voice(received.chat.id, new_message.content)
        elif isinstance(new_message, GifMessage):
            sent = self.tgbot.send_animation(received.chat.id, new_message.content)  # не отправляется
            # sent = self.tgbot.send_video_note(received.chat.id, new_message.content, length=240)
        elif isinstance(new_message, ModelMessage):
            pass  # TODO: реализовать
        elif isinstance(new_message, DocMessage):
            sent = self.tgbot.send_document(received.chat.id, new_message.content)
        elif isinstance(new_message, AudioMessage):
            sent = self.tgbot.send_audio(received.chat.id, new_message.content)
        elif isinstance(new_message, StickerMessage):
            sent = self.tgbot.send_sticker(received.chat.id, new_message.content)
        elif isinstance(new_message, ButtonsMessage):
            markup_inline = types.InlineKeyboardMarkup()
            for button in new_message.content:
                new_item = types.InlineKeyboardButton(text=button.text, 
                                                      callback_data=button.callback_data)
                markup_inline.add(new_item)
            sent = self.tgbot.send_message(received.chat.id, new_message.caption, reply_markup=markup_inline)
        elif isinstance(new_message, GroupMessage):
            pass  # TODO: реализовать
        else:
            sent = None
            print('хз')
        # сохраняем id последнего отправленного сообщения для конкретного пользователя
        for line in self.user_table:
            user_id, _, last_message_id = line
            print(user_id, received.chat.id)
            if user_id == received.chat.id:
                line[2] = sent.id
                break

    def voice_to_text(self, voice):
        pass


bot = Bot(TOKEN, get_sample_script())
