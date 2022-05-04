from abc import ABC, abstractmethod
import random
import string
import media_converter
# TODO: аннотации типов


class Post(ABC):
    """Класс поста."""
    SEND_IMMEDIATELY = 0  # константа: отправить следующий пост сразу за текущим
    def __init__(self, content):
        """Создать пост с указанным контентом.

        Параметры:
        content: содержимое поста (текст, аудио, кнопки, документы и т.д.)
        """
        self.content = content
        self.transitions = []  # список функций, возвращающих следующий пост при выполнении
                               # некоторого условия

    def add_next(self, next_post, requiered_callback=SEND_IMMEDIATELY, is_keyword=False):
        """Добавить переход на пост.

        Параметры:
        next_post: пост, на который нужно перейти
        requiered_callback: содержание полученного от игрока сообщения (строка или запись 
                            голоса) либо константа SEND_IMMEDIATELY - пост следует 
                            отправить сразу за текущим, не проверяя условий
        is_keyword: если True, то в параметр requiered_callback передано ключевое слово,
                    которое нужно найти; иначе - ответ игрока должен точно совпадать с указанным
                    в required_callback
        """
        def transition(received):
            if requiered_callback == self.SEND_IMMEDIATELY:
                # следующий пост следует отправить сразу за текущим
                return next_post
            if received is None:
                # ответа от игрока не получено - ничего не возвращаем
                return None
            if is_keyword:
                # пост нужно отправить, если полученное от игрока сообщение содержит
                # ключевое слово
                pass  # TODO: реализовать поиск ключевых слов в строке
            if received.lower() == requiered_callback.lower():
                # полученное сообщение совпало с ожидаемым
                return next_post
        self.transitions.append(transition)

    def get_next(self, received=None):
        """Получить следующий пост.

        Параметры:
        received: полученное от пользователя сообщение (текст либо голос). Если None,
                  будет производиться поиск поста, который отправляется
                  без условий
        """
        for transition in self.transitions:
            next_post = transition(received)
            if not next_post is None:
                return next_post


class TextPost(Post):
    """Текстовый пост."""
    def __init__(self, text):
        super().__init__(text)


class ImagePost(Post):
    """Пост с картинкой."""
    def __init__(self, file_path):
        super().__init__(open(file_path, 'rb'))


class VideoPost(Post):
    """Пост с видео."""
    def __init__(self, file_path):
        super().__init__(open(file_path, 'rb'))


class VoicePost(Post):  # должен быть формат ogg
    """Пост с голосовым сообщением"""
    def __init__(self, file_path):
        super().__init__(open(file_path, 'rb'))
        self.text = self.get_text()

    def get_text(self):
        """Распознаёт текст в голосовом сообщении."""
        pass  # TODO: распознавание речи

class GifPost(Post):
    """Пост с gif-анимацией."""
    def __init__(self, file_path):
        super().__init__(open(file_path, 'rb'))


class RoundPost(Post):
    """Пост с круглым видео."""
    def __init__(self, file_path, width=240):
        """Создаёт пост с круглым видео.

        Параметры:
        file_path - путь до видео
        width - ширина (и высота) видео
        """
        media_converter.changeGIFResolution(file_path, (width, width), file_path)
        super().__init__(open(file_path, 'rb'))


class ModelPost(Post):
    """Пост со ссылкой на страницу с 3D-моделью."""
    def __init__(self, file_path):
        super().__init__(self.get_html_markup(file_path))

    def get_html_markup(self, file_path):
        """Возвращает разметку html-страницы с 3D-моделью."""
        pass  # TODO: генерация html-разметки


class DocPost(Post):
    """Пост с прикреплённым документом (произвольным файлом)."""
    def __init__(self, file_path):
        # TODO: файл должен быть не пустым - обработать
        super().__init__(open(file_path, 'rb'))


class AudioPost(Post):
    """Пост с аудиозаписью."""
    def __init__(self, file_path):
        super().__init__(open(file_path, 'rb'))


class StickerPost(Post):
    """Пост с картинкой-стикером."""
    def __init__(self, file_path):
        super().__init__(open(file_path, 'rb'))


class ButtonsPost(Post):
    """Пост с набором кнопок."""
    def __init__(self, caption, buttons):
        """Создаёт пост с набором кнопок и подписью.

        Параметры:
        buttons - массив кнопок Button
        caption - текстовая подпись к посту
        """
        super().__init__(buttons)
        self.caption = caption

    def add_next(self, next_post, requiered_button):
        def transition(callback_data):
            if callback_data == requiered_button.callback_data and requiered_button in self.content:
                # удаляем с панели кнопку, на которую нажали
                del self.content[self.content.index(requiered_button)]
                return next_post
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


class GroupPost(Post):
    """Пост, содержащий фото, видео, документы, аудио и (или) текст."""
    def __init__(self, posts):
        """Создаёт сгруппированный пост.

        Параметры:
        messages - посты, входящие в состав группы.
        """
        super().__init__(posts)


def get_sample_script():  # возвращает пример сценария
    gray_btn = Button('серенький')
    pink_btn = Button('розовый')
    green_btn = Button('зелёный')

    post1 = ButtonsPost('Какого цвета бегемот?', [gray_btn, pink_btn, green_btn])

    post2 = TextPost('Ну что вы, нет конечно')
    post3 = TextPost('Так только в мультиках бывает 😊')
    post4 = GifPost('gif.gif')
    post5 = DocPost('док.docx')

    post1.add_next(next_post=post3, requiered_button=pink_btn)
    post1.add_next(next_post=post4, requiered_button=gray_btn)
    post1.add_next(next_post=post2, requiered_button=green_btn)

    post2.add_next(next_post=post5)
    post3.add_next(next_post=post1)
    post5.add_next(next_post=post1)

    return post1


# TODO: функция для создания квадратных видео 240х240