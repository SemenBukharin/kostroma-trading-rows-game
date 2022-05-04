import telebot  # pip install pyTelegramBotAPI
from telebot import types
from bot_message import *
from config import TOKEN


class Bot:
    """Класс Telegram-бота с игрой."""
    def __init__(self, token, start_post):
        """Создаёт Telegram-бота с указанным токеном и сценарием.

        Параметры:
        token - токен бота
        start_post - первый пост игры
        """
        self.tgbot = telebot.TeleBot(token)
        self.user_table = []  # таблица с записями вида "userid - post - last_message_id"
        self.start_post = start_post

        @self.tgbot.message_handler(commands=['start'])
        def register_new_user(message):
            """Записывает нового игрока в таблицу при нажатии им кнопки "Старт"."""
            if any([user_id == message.from_user.id for user_id, _, _ in self.user_table]):
                return  # данный игрок уже начал игру
            # делаем запись о новом игроке
            self.user_table.append([message.from_user.id, self.start_post, message.id])
            print(f'Пользователь {message.from_user.id} начал игру.')
            self.send(message, self.start_post)  # отправляем первое сообщение


        @self.tgbot.message_handler(content_types=['text'])
        def handle_text(message):
            """Обрабатывает текстовые сообщения от игрока."""
            # TODO: в одну функцию
            post = None
            for user_id, last_post, _ in self.user_table:
                if user_id == message.from_user.id:
                    post = last_post
                    break
            if post is None:
                # игрок ещё не начал игру (не нажал на "Старт")
                return
            while True:
                post = post.get_next(message.text)  # получаем новые сообщения для отправки
                if post is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(received=message, new_post=post)
                message.text = None


        @self.tgbot.message_handler(content_types=['voice'])
        def handle_voice(message):
            """Обрабатывает голосовые сообщения от игрока."""
            post = None
            for user_id, last_post, _ in self.user_table:
                if user_id == message.from_user.id:
                    post = last_post
                    break
            if post is None:
                # игрок ещё не начал игру (не нажал на "Старт")
                return
            while True:
                post = post.get_next(message.voice)  # получаем новые сообщения для отправки
                if post is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(received=message, new_post=post)
                message.voice = None

        @self.tgbot.callback_query_handler(func=lambda call: True)
        def handle_buttons(call):
            """Обрабатывает нажатия на кнопки."""
            post = None
            for user_id, last_post, last_message_id in self.user_table:
                if user_id == call.from_user.id and last_message_id == call.message.id:
                    post = last_post
                    break
            if post is None:
                # игрок ещё не начал игру (не нажал на "Старт") или нажал на старые кнопки
                return
            while True:
                post = post.get_next(call.data)  # получаем новые сообщения для отправки
                if post is None:
                    # сообщения кончились либо ожидается ответ от пользователя
                    break
                self.send(received=call.message, new_post=post)
                call.data = None

        self.tgbot.infinity_polling()  # начинаем слушать бота

    def send(self, received, new_post):
        """Отправляет пост в чат.

        Параметры:
        received - полученнное сообщение (тип telebot.Message)
        new_post - пост для отправки (тип bot_message.Post)
        """
        if isinstance(new_post, TextPost):
            sent = self.tgbot.send_message(received.chat.id, new_post.content)
        elif isinstance(new_post, ImagePost):
            sent = self.tgbot.send_photo(received.chat.id, new_post.content)
        elif isinstance(new_post, VideoPost):
            sent = self.tgbot.send_video(received.chat.id, new_post.content)
        elif isinstance(new_post, VoicePost):
            sent = self.tgbot.send_voice(received.chat.id, new_post.content)
        elif isinstance(new_post, GifPost):
            sent = self.tgbot.send_animation(received.chat.id, new_post.content)
        elif isinstance(new_post, RoundPost):
            sent = self.tgbot.send_video_note(received.chat.id, new_post.content, length=240)
        elif isinstance(new_post, ModelPost):
            pass  # TODO: реализовать
        elif isinstance(new_post, DocPost):
            sent = self.tgbot.send_document(received.chat.id, new_post.content)
        elif isinstance(new_post, AudioPost):
            sent = self.tgbot.send_audio(received.chat.id, new_post.content)
        elif isinstance(new_post, StickerPost):
            sent = self.tgbot.send_sticker(received.chat.id, new_post.content)
        elif isinstance(new_post, ButtonsPost):
            markup_inline = types.InlineKeyboardMarkup()
            for button in new_post.content:
                new_item = types.InlineKeyboardButton(text=button.text,
                                                      callback_data=button.callback_data)
                markup_inline.add(new_item)
            sent = self.tgbot.send_message(received.chat.id, new_post.caption, reply_markup=markup_inline)
        elif isinstance(new_post, GroupPost):
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
