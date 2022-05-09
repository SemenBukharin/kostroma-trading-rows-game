import wx  # pip install -U --pre -f https://wxpython.org/Phoenix/snapshot-builds/ wxPython
import wx.stc
import codecs
import code_analyzer


class Editor(wx.stc.StyledTextCtrl):
    """Класс текстового поля редактора."""
    def __init__ (self, parent, id = wx.ID_ANY, \
            pos = wx.DefaultPosition, \
            size = wx.DefaultSize,\
            style = 0,\
            name = "editor"):
        wx.stc.StyledTextCtrl.__init__ (self, parent, id, pos, size, style, name)

        # задаём боковую панель с номерами строк
        # TODO: расширение панели
        self.SetMarginWidth(1, 40)
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(2, 10)

        # создаем кодировщик один раз в конструкторе,
        # чтобы не создавать его при каждой необходимости
        self.encoder = codecs.getencoder("utf-8")

        # стиль по умолчанию будет 14-ым шрифтом
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "size:%d" % 12)

        # задаём шрифты
        # if wxPlatform == '__WXMSW__':
        #     self.faces = { 'times': 'Times New Roman',
        #                    'mono' : 'Courier New',
        #                    'helv' : 'Arial',
        #                    'other': 'Comic Sans MS',
        #                    'size' : 10,
        #                    'size2': 8,
        #                  }
        # else:
        #     self.faces = { 'times': 'Times',
        #                    'mono' : 'Courier',
        #                    'helv' : 'Helvetica',
        #                    'other': 'new century schoolbook',
        #                    'size' : 12,
        #                    'size2': 10,
        #                  }

        # определение стилей подсветки
        self.style_def = 0
        self.style_gray = 1
        self.style_purple = 2
        self.style_blue = 3
        self.style_green = 4

        self.StyleSetSpec(self.style_def, "face:Consolas,size:12,fore:#000000")
        self.StyleSetSpec(self.style_gray, "face:Consolas,size:12,fore:#888888")
        self.StyleSetSpec(self.style_purple, "face:Consolas,size:12,fore:#C800C8,bold")
        self.StyleSetSpec(self.style_blue, "face:Consolas,size:12,fore:#000096,bold")
        self.StyleSetSpec(self.style_green, "face:Consolas,size:12,fore:#009600,italic")

        self.code_analyzer = code_analyzer.CodeAnalyzer()

        # подписка на событие, когда нужно изменить стиль
        self.Bind(wx.stc.EVT_STC_STYLENEEDED, self.onStyleNeed)

    def onPosChange (self, event):
        # Получим текущую позицию каретки в байтах
        pos = self.GetCurrentPos()
        text_left = self.GetTextRange(0, pos)
        self.GetParent().GetParent().GetParent().SetTitle(str (len (text_left) ) )

    def calcByteLen(self, text):
        """Посчитать длину строки в байтах, а не в символах"""
        return len(self.encoder(text)[0])

    def calcBytePos (self, text, pos):
        """Преобразовать позицию в символах в позицию в байтах"""
        return len(self.encoder(text[:pos])[0])

    def onStyleNeed(self, event):
        text = self.GetText()

        # cначала ко всему тексту применим стиль по умолчанию
        self.StartStyling(0)
        self.SetStyling(self.calcByteLen(text), self.style_def)

        # Раскрасим слова с использованием так называемых индикаторов
        self.highlightCode()
        # self.colorizeWord(u"кнопка", self.style_blue)
        # self.colorizeWord(u"бот", self.style_purple)
        # self.colorizeWord(u"строка", self.style_green)

    def highlightCode(self):
        """Подсветка синтаксиса."""
        text = self.GetText()

        analyzed = self.code_analyzer.get_words(text)

        for word, line_number, last_pos, word_type in analyzed:
            pos = last_pos-len(word)
            bytepos = self.calcBytePos(text, pos)  # находим начальную позицию в байтах
            text_byte_len = self.calcByteLen(word)  # вычисляем длину слова в байтах
            # применяем стиль
            self.StartStyling(bytepos)
            if word_type == self.code_analyzer.STRING:
                self.SetStyling(text_byte_len, self.style_green)
            elif word_type == self.code_analyzer.COMMENT:
                self.SetStyling(text_byte_len, self.style_gray)
            elif word_type == self.code_analyzer.KEYWORD:
                if word == self.code_analyzer.BOT or word == self.code_analyzer.BOT_END or\
                   word == self.code_analyzer.SCENE or word == self.code_analyzer.SCENE_END:
                    self.SetStyling(text_byte_len, self.style_purple)
                else:
                    self.SetStyling(text_byte_len, self.style_blue)

        # print(analyzed)
        print(self.code_analyzer.get_words_for_parsing(analyzed))

    def colorizeWord(self, styled_text, style):
        """Раскрасить в тексте все слова styled_text стилем style"""
        text = self.GetText()

        # Ищем все вхождения слова
        pos = text.find (styled_text)      
        while pos != -1:
            nextsym = text[pos + len (styled_text): pos + len (styled_text) + 1]
            prevsym = text[pos - 1: pos]

            if (pos == 0 or prevsym.isspace()) and (pos == len (text) - len(styled_text) or nextsym.isspace()):

                # Нас интересует позиция в байтах, а не в символах
                bytepos = self.calcBytePos(text, pos)

                # Находим длину искомой строки в байтах
                text_byte_len = self.calcByteLen(styled_text)

                # Применим стиль
                self.StartStyling(bytepos)
                self.SetStyling(text_byte_len, style)

            pos = text.find (styled_text, pos + len (styled_text) )


class MainWindow(wx.Frame):
    """Класс окна редактора."""
    def __init__(self, parent, title):
        super().__init__(parent, title=title, style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)
        # TODO: иконка
        # TODO: отступы меню
        # иконки меню
        self.createMenuBar()
        self.createSideBar()

        main_spltr = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_LIVE_UPDATE)

        sidebar_p = wx.Panel(main_spltr)
        edit_p = wx.Panel(main_spltr)

        main_spltr.SplitVertically(sidebar_p, edit_p)
        main_spltr.SetMinimumPaneSize(200)

        scenes_p = wx.Panel(sidebar_p)
        scenes_st = wx.StaticText(scenes_p, label='Сцены')
        scenes_b = wx.Button(scenes_p, label='+', style=wx.BU_EXACTFIT)
        scenes_lb = wx.ListBox(scenes_p, choices=self.get_scenes_names())
        scenes_gbs = wx.GridBagSizer(2, 3)
        scenes_gbs.Add(scenes_st, pos=(0, 0))
        scenes_gbs.Add(scenes_b, pos=(0, 2))
        scenes_gbs.Add(scenes_lb, pos=(1, 0), span=(1, 3), flag=wx.EXPAND | wx.UP, border=5)
        scenes_gbs.AddGrowableCol(1)
        scenes_gbs.AddGrowableRow(1)
        scenes_p.SetSizer(scenes_gbs)

        res_p = wx.Panel(sidebar_p)
        res_st = wx.StaticText(res_p, label='Ресурсы')
        res_b = wx.Button(res_p, label='+', style=wx.BU_EXACTFIT)
        res_lb = wx.ListBox(res_p, choices=self.get_resources_names())
        res_gbs = wx.GridBagSizer(2, 3)
        res_gbs.Add(res_st, pos=(0, 0))
        res_gbs.Add(res_b, pos=(0, 2))
        res_gbs.Add(res_lb, pos=(1, 0), span=(1, 3), flag=wx.EXPAND | wx.UP, border=5)
        res_gbs.AddGrowableCol(1)
        res_gbs.AddGrowableRow(1)
        res_p.SetSizer(res_gbs)

        sidebar_bs = wx.BoxSizer(wx.VERTICAL)
        sidebar_bs.Add(scenes_p, wx.ID_ANY, flag=wx.EXPAND | wx.ALL, border=5)
        sidebar_bs.Add(res_p, wx.ID_ANY, flag=wx.EXPAND | wx.ALL, border=5)
        sidebar_p.SetSizer(sidebar_bs)

        editor = Editor(edit_p)
        # edit_tc = wx.TextCtrl(edit_p, style=wx.TE_MULTILINE)
        edit_bs = wx.BoxSizer()
        edit_bs.Add(editor, wx.ID_ANY, flag=wx.EXPAND)
        edit_p.SetSizer(edit_bs)
        # scenes_header_p = wx.Panel(sidebar_p)
        # scenes_header_st = wx.StaticText(scenes_header_p, label='Сцены:')
        # scenes_header_b = wx.Button(scenes_header_p, label='+', style=wx.BU_EXACTFIT)
        # scenes_header_bs = wx.BoxSizer(wx.HORIZONTAL)
        # scenes_header_bs.Add(scenes_header_st)
        # scenes_header_bs.Add(wx.StaticText(scenes_header_p), flag=wx.EXPAND)
        # scenes_header_bs.Add(scenes_header_b)

        # scenes_lb = wx.ListBox(sidebar_p, choices=self.get_scenes_names())

        # sidebar_bs = wx.BoxSizer(wx.VERTICAL)
        # sidebar_bs.Add(scenes_header_p, flag=wx.EXPAND | wx.ALL, border=10)
        # sidebar_bs.Add(wx.StaticLine(sidebar_p), flag=wx.EXPAND | wx.ALL, border=10)
        # sidebar_bs.Add(scenes_lb, flag=wx.EXPAND | wx.ALL, border=10)

        # edit_tc = wx.TextCtrl(main_p, style=wx.TE_MULTILINE)

        # sidebar_bs.Add(edit, proportion=1)
        # scenes_header_p.SetSizer(scenes_header_bs)
        # sidebar_p.SetSizer(sidebar_bs)



    def createMenuBar(self):
        menubar = wx.MenuBar()

        # TODO: свои ID
        project_menu = wx.Menu()  # вкладка "Проект"
        create_item = project_menu.Append(wx.ID_ANY, 'Создать\tCtrl+N', 'Создать новый пустой проект')
        open_item = project_menu.Append(wx.ID_ANY, 'Открыть...\tCtrl+O', 'Открыть существующий проект')
        save_item = project_menu.Append(wx.ID_ANY, 'Сохранить...\tCtrl+S', 'Сохранить изменения в текущем проекте')

        bot_menu = wx.Menu()  # подменю "Бот"
        start_item = bot_menu.Append(wx.ID_ANY, 'Запуск...\tCtrl+K', 'Запустить бота')
        stop_item = bot_menu.Append(wx.ID_ANY, 'Стоп\tCtrl+P', 'Остановить бота')

        about_menu = wx.Menu()  # вкладка "О программе"
        doc_item = about_menu.Append(wx.ID_ANY, 'Спецификация языка\tCtrl+D', 'Просмотреть команды языка разметки сценариев')
        help_item = about_menu.Append(wx.ID_ANY, 'Руководство пользователя\tCtrl+H', 'Посмотреть руководство пользователя')

        menubar.Append(project_menu, '&Проект')
        menubar.Append(bot_menu, '&Бот')
        menubar.Append(about_menu, '&Помощь')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.onCreateClick, create_item)
        self.Bind(wx.EVT_MENU, self.onOpenClick, open_item)
        self.Bind(wx.EVT_MENU, self.onSaveClick, save_item)
        self.Bind(wx.EVT_MENU, self.onStartClick, start_item)
        self.Bind(wx.EVT_MENU, self.onStopClick, stop_item)
        self.Bind(wx.EVT_MENU, self.onDocClick, doc_item)
        self.Bind(wx.EVT_MENU, self.onHelpClick, help_item)

    def createSideBar(self):
        pass

    def get_scenes_names(self):
        return ['сцена 1', 'сцена 2', 'сцена 3']*10  # TODO: реализовать

    def get_resources_names(self):
        return ['pic.jpg', 'video.mp4', 'voice.ogg']  # TODO: реализовать

    def onCreateClick(self, event):
        pass

    def onOpenClick(self, event):
        pass

    def onSaveClick(self, event):
        pass

    def onStartClick(self, event):
        pass

    def onStopClick(self, event):
        pass

    def onDocClick(self, event):
        pass

    def onHelpClick(self, event):
        pass

app = wx.App()

frame = MainWindow(None, 'Редактор Telegram-ботов')
frame.Show()

app.MainLoop()