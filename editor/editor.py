import wx  # pip install -U --pre -f https://wxpython.org/Phoenix/snapshot-builds/ wxPython

class EditorFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
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

        edit_tc = wx.TextCtrl(edit_p, style=wx.TE_MULTILINE)
        edit_bs = wx.BoxSizer()
        edit_bs.Add(edit_tc, wx.ID_ANY, flag=wx.EXPAND)
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

frame = EditorFrame(None, 'Редактор Telegram-ботов')
frame.Show()

app.MainLoop()