class CodeAnalyzer():
    # типы слов
    COMMENT = 0  # комментарий
    KEYWORD = 1  # ключевое слово
    STRING = 2  # строка в кавычках
    UNKNOWN = 3  # тип не определён

    # слова и символы, которые могут встречаться в тексте
    BOT = 'бот'
    BOT_END = 'конецБота'
    SCENE = 'сцена'
    SCENE_END = 'конецСцены'
    TEXT = 'текст'
    PHOTO = 'фото'
    VOICE = 'гс'
    AUDIO = 'аудио'
    VIDEO = 'видео'
    GIF = 'гиф'
    DOC = 'документ'
    STICKER = 'стикер'
    GROUP = 'группа'
    GROUP_END = 'конецГруппы'
    WAIT_AUDIO = 'ждатьАудио'
    WAIT_TEXT = 'ждатьТекст'
    WAIT_END = 'хватитЖдать'
    BACK = 'назад'
    ELSE = 'иначе'
    EXIT = 'выход'
    BUTTONS = 'кнопки'
    BUTTONS_END = 'хватитКнопок'
    ASTERISK = '*'
    COLON = ':'
    DOUBLE_DASH = '--'
    EXCLAM = '!'
    QUOTE = '"'
    # CARRIAGE_RETURN = '\r'
    NEWLINE = '\r\n'
    SPACE = ' '

    # ключевые слова
    KWORDS = [BOT, BOT_END, SCENE, SCENE_END, TEXT, PHOTO, VOICE, AUDIO, VIDEO, GIF, DOC, STICKER,
              GROUP, GROUP_END, WAIT_AUDIO, WAIT_TEXT, WAIT_END, BACK, ELSE, EXIT, BUTTONS, BUTTONS_END,
              ASTERISK, COLON, DOUBLE_DASH]

    def __init__(self):
        pass

    def autocomplete(self, text):
        pass

    def get_words_for_parsing(self, analyzed):
        """Принимает на вход список кортежей, сгенерированный функцией get_words, возвращает список
        кортежей для парсинга."""
        result = []  # список кортежей вида (слово, номер_строки, тип (строка или ключевое слово))
        for word, line_number, _, word_type in analyzed:
            if word_type == self.STRING:
                # убираем символы \r\n из строки и лишнее экранирования для табов и переводов строк
                word = word.replace(self.NEWLINE, '')\
                           .replace('\\t', '\t')\
                           .replace('\\n', '\n')
            if word_type != self.COMMENT:
                result.append((word, line_number, word_type))
        return result


    def get_words(self, code):
        # # заменяем таб на 4 пробела
        # if text.endswith('\t'):
        #     text[-1] = ' '*4

        result = []  # список кортежей вида (слово, номер_строки, позиция_последнего_символа_в_тексте, тип)
        line_number = 1  # номер текущей строки
        current_word = ''  # текущее исследуемое слово
        current_type = self.UNKNOWN  # тип текущего исследуемого слова

        for i, symbol in enumerate(code):
            pos = i+1
            if symbol == '\r':
                symbol = self.NEWLINE
                pos += 1
            elif symbol == '\n':
                continue
            if symbol == self.QUOTE:
                if current_type == self.STRING:
                    # заканчиваем считывание строки в кавычках
                    result.append((current_word+symbol,
                                   line_number-current_word.count(self.NEWLINE),
                                   pos, current_type))
                    current_word = ''
                    current_type = self.UNKNOWN
                    continue
                elif current_type != self.COMMENT:
                    # начинаем считывание строки в кавычках
                    current_word = ''
                    current_type = self.STRING
            elif symbol == self.NEWLINE:
                line_number += 1
                # pos -= 1  # т.к. перед \n следует \r
                if current_type == self.COMMENT:
                    # комментарий прерывается при переходе на следующую строку
                    result.append((current_word+symbol, line_number, pos, current_type))
                    current_word = ''
                    current_type = self.UNKNOWN
                    continue
            elif symbol == self.EXCLAM:
                if current_type != self.STRING and current_type != self.COMMENT:
                    # начинается комментарий
                    current_word = ''
                    current_type = self.COMMENT
            if current_type == self.KEYWORD and symbol != self.NEWLINE and\
               symbol != self.SPACE and symbol != self.COLON:
                # если после ввода ключевого слова пользователь ввёл что-то, кроме
                # пробела или перевода строки, ключевое слово теряется
                current_word, _, _, _ = result[-1]
                del result[-1]
            if current_type == self.KEYWORD:
                current_type = self.UNKNOWN
            if current_type == self.UNKNOWN and (symbol == self.NEWLINE or symbol == self.SPACE):
                current_word = ''
            else:
                current_word += symbol
            if current_word in self.KWORDS:
                current_type = self.KEYWORD
                result.append((current_word, line_number, pos, current_type))
                current_word = ''
        if current_type == self.STRING or current_type == self.COMMENT:
            result.append((current_word, line_number-current_word.count(self.NEWLINE), pos, current_type))

        return result
