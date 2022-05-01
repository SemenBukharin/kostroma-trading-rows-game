from abc import ABC, abstractmethod
import random
import string
# TODO: аннотации типов


class Message(ABC):
    """Класс сообщения."""
    SEND_IMMEDIATELY = 0  # константа: отправить следующее сообщение сразу за текущим
    def __init__(self, content):
        """Создать сообщение с указанным контентом.

        Параметры:
        content: содержимое сообщения (текст, аудио, кнопки, документы и т.д.)
        """
        self.content = content
        self.transitions = []  # список функций, возвращающих следующее сообщение при выполнении
                               # некоторого условия

    def add_next(self, next_message, requiered_callback=SEND_IMMEDIATELY, is_keyword=False):
        """Добавить переход на сообщение.

        Параметры:
        next_message: сообщение Message, на которое нужно перейти
        requiered_callback: содержание полученного от игрока сообщения (строка или запись 
                            голоса) либо константа SEND_IMMEDIATELY - сообщение следует 
                            отправить сразу за текущим, не проверяя условий
        is_keyword: если True, то в параметр requiered_callback передано ключевое слово,
                    которое нужно найти; иначе - ответ игрока должен точно совпадать с указанным
                    в required_callback
        """
        def transition(received):
            if requiered_callback == self.SEND_IMMEDIATELY:
                # следующее сообщение следует отправить сразу за текущим
                return next_message
            if received is None:
                # ответа от игрока не получено - ничего не возвращаем
                return None
            if is_keyword:
                # сообщение нужно отправить, если полученное от игрока сообщение содержит
                # ключевое слово
                pass  # TODO: реализовать поиск ключевых слов в строке
            if received.lower() == requiered_callback.lower():
                # полученное сообщение совпало с ожидаемым
                return next_message
        self.transitions.append(transition)

    def get_next(self, received=None):
        """Получить следующее сообщение.

        Параметры:
        received: полученное от пользователя сообщение (текст либо голос). Если None,
                  будет производиться поиск сообщения, которое отправляется
                  без условия
        """
        for transition in self.transitions:
            next_message = transition(received)
            if not next_message is None:
                return next_message


class TextMessage(Message):
    """Текстовое сообщение."""
    def __init__(self, text):
        Message.__init__(self, text)


class ImageMessage(Message):
    """Сообщение с картинкой."""
    def __init__(self, file_path):
        Message.__init__(self, open(file_path, 'rb'))


class VideoMessage(Message):
    """Сообщение с видео."""
    def __init__(self, file_path):
        Message.__init__(self, open(file_path, 'rb'))


class VoiceMessage(Message):  # должен быть формат ogg
    """Голосовое сообщение."""
    def __init__(self, file_path):
        Message.__init__(self, open(file_path, 'rb'))
        self.text = self.get_text()

    def get_text(self):
        """Распознаёт текст в голосовом сообщении."""
        pass  # TODO: распознавание речи


class GifMessage(Message):
    """Сообщение с gif-анимацией."""
    def __init__(self, file_path):
        Message.__init__(self, open(file_path, 'rb'))


class ModelMessage(Message):
    """Сообщение со ссылкой на страницу с 3D-моделью."""
    def __init__(self, file_path):
        Message.__init__(self, self.get_html_markup(file_path))

    def get_html_markup(self, file_path):
        """Возвращает разметку html-страницы с 3D-моделью."""
        pass  # TODO: генерация html-разметки


class DocMessage(Message):
    """Сообщение с прикреплённым документом (произвольным файлом)."""
    def __init__(self, file_path):
        # TODO: файл должен быть не пустым - обработать
        Message.__init__(self, open(file_path, 'rb'))


class AudioMessage(Message):
    """Сообщение с аудиозаписью."""
    def __init__(self, file_path):
        Message.__init__(self, open(file_path, 'rb'))


class StickerMessage(Message):
    """Сообщение с картинкой-стикером."""
    def __init__(self, file_path):
        Message.__init__(self, open(file_path, 'rb'))


class ButtonsMessage(Message):
    """Сообщение с набором кнопок."""
    def __init__(self, caption, buttons):
        """Создаёт сообщение с набором кнопок и подписью.

        Параметры:
        buttons - массив кнопок Button
        caption - текстовая подпись к сообщению
        """
        Message.__init__(self, buttons)
        self.caption = caption

    def add_next(self, next_message, requiered_button):
        def transition(callback_data):
            if callback_data == requiered_button.callback_data:
                # удаляем с панели кнопку, на которую нажали
                del self.content[self.content.index(requiered_button)]
                return next_message
        self.transitions.append(transition)


class Button:
    """Кнопка."""
    def __init__(self, text):
        """Создаёт кнопку.

        Параметры:
        text - текст на кнопке.
        """
        self.text = text
        self.callback_data = self.generate_callback_data()  # идентификатор кнопки

    def generate_callback_data(self):
        """Генерирует случайный идентификатор для кнопки."""
        return ''.join(random.choices(string.ascii_lowercase, k=10))


class GroupMessage(Message):
    """Сообщение, содержащее фото, видео, документы, аудио и (или) текст."""
    def __init__(self, messages):
        """Создаёт сгруппированное сообщение.

        Параметры:
        messages - сообщения Message, входящие в состав группы.
        """
        Message.__init__(self, messages)


def get_sample_script():  # возвращает пример сценария
    gray_btn = Button('серенький')
    pink_btn = Button('розовый')
    green_btn = Button('зелёный')

    mes1 = ButtonsMessage('Какого цвета бегемот?', [gray_btn, pink_btn, green_btn])

    mes2 = TextMessage('Ну что вы, нет конечно')
    mes3 = TextMessage('Так только в мультиках бывает 😊')
    # mes4 = GifMessage('success.gif')  # не отправляется
    # mes4 = GifMessage('face.mp4')  # долго отправляется
    mes4 = TextMessage('Всё.')
    mes5 = DocMessage('док.docx')

    mes1.add_next(next_message=mes3, requiered_button=pink_btn)
    mes1.add_next(next_message=mes4, requiered_button=gray_btn)
    mes1.add_next(next_message=mes2, requiered_button=green_btn)

    mes2.add_next(next_message=mes5)
    mes3.add_next(next_message=mes1)
    mes5.add_next(next_message=mes1)

    return mes1
