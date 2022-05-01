import telebot
from telebot import types
from bot_message import *


class Bot:
    """Класс Telegram-бота с игрой."""
    def __init__(self, token, start_message):
        """Создаёт Telegram-бота с указанным токеном и сценарием.

        Параметры:
        token - токен бота
        start_message - первое сообщение игры (тип - Message)
        """
        self.tgbot = telebot.TeleBot(token)
        self.user_table = []  # таблица с записями вида "userid - script"
        self.start_message = start_message

        @self.tgbot.message_handler(commands=['start'])
        def registry_new_gamer(message):
            """Записывает нового игрока в таблицу при нажатии им кнопки "Старт"."""
            for user_id, message in self.user_table:
                if user_id == message.from_user.id:
                    return  # данный игрок уже начал игру
            self.user_table.append((message.from_user.id, start_message))
            print(f'Пользователь {message.from_user.id} начал игру.')
            self.send(message.chat.id, self.start_message)

        @self.tgbot.message_handler(content_types=['text'])
        def handle_text(content):
            """Обрабатывает текстовые сообщения от игрока."""
            # TODO: в одну функцию
            message = None
            for user_id, prev_message in self.user_table:
                if user_id == content.from_user.id:
                    message = prev_message
                    break
            if message is None:
                # игрок ещё не начал игру (не нажал на "Старт")
                return
            received = content.text
            while True:
                message = message.get_next(received)  # получаем новые сообщения для отправки
                if message is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(content.chat.id, message)
                received = None


        @self.tgbot.message_handler(content_types=['voice'])
        def handle_voice(content):
            """Обрабатывает голосовые сообщения от игрока."""
            message = None
            for user_id, prev_message in self.user_table:
                if user_id == content.from_user.id:
                    message = prev_message
                    break
            if message is None:
                # игрок ещё не начал игру (не нажал на "Старт")
                return
            received = content.voice
            while True:
                message = message.get_next(received)  # получаем новые сообщения для отправки
                if message is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(content.chat.id, message)
                received = None


        @self.tgbot.callback_query_handler(func=lambda call: True)
        def buttons_callback(call):
            """Обрабатывает нажатия на кнопки."""
            # TODO: нажатие ТОЛЬКО на ПОСЛЕДНЕЕ сообщение с кнопками
            message = None
            for user_id, prev_message in self.user_table:
                if user_id == call.from_user.id:
                    message = prev_message
                    break
            if message is None:
                # игрок ещё не начал игру (не нажал на "Старт")
                return
            received = call.data
            while True:
                message = message.get_next(received)  # получаем новые сообщения для отправки
                if message is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(call.message.chat.id, message)
                received = None

        self.tgbot.infinity_polling()  # начинаем слушать бота

    def send(self, chat_id, new_message):
        """Отправляет сообщение в чат."""
        if isinstance(new_message, TextMessage):
            self.tgbot.send_message(chat_id, new_message.content)
        elif isinstance(new_message, ImageMessage):
            self.tgbot.send_photo(chat_id, new_message.content)
        elif isinstance(new_message, VideoMessage):
            self.tgbot.send_video(chat_id, new_message.content)
        elif isinstance(new_message, VoiceMessage):
            self.tgbot.send_voice(chat_id, new_message.content)
        elif isinstance(new_message, GifMessage):
            self.tgbot.send_animation(chat_id, new_message.content)  # не отправляется
            # self.tgbot.send_video_note(chat_id, new_message.content)
        elif isinstance(new_message, ModelMessage):
            pass  # TODO: реализовать
        elif isinstance(new_message, DocMessage):
            self.tgbot.send_document(chat_id, new_message.content)
        elif isinstance(new_message, AudioMessage):
            self.tgbot.send_audio(chat_id, new_message.content)
        elif isinstance(new_message, StickerMessage):
            self.tgbot.send_sticker(chat_id, new_message.content)
        elif isinstance(new_message, ButtonsMessage):
            markup_inline = types.InlineKeyboardMarkup()
            for button in new_message.content:
                new_item = types.InlineKeyboardButton(text=button.text, 
                                                      callback_data=button.callback_data)
                markup_inline.add(new_item)
            self.tgbot.send_message(chat_id, new_message.caption, reply_markup=markup_inline)
        elif isinstance(new_message, GroupMessage):
            pass  # TODO: реализовать
        else:
            print('хз')


    def voice_to_text(self, voice):
        pass


bot = Bot('5233900254:AAEpFyqr0LY5PmvLAvY0GK9jJlgyDOYcAMA', get_sample_script())
