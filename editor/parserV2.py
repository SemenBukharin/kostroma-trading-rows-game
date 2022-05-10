# -*- coding: utf-8 -*-
import code_analyzer

from editor import * 
import wx  # pip install -U --pre -f https://wxpython.org/Phoenix/snapshot-builds/ wxPython
import wx.stc
import codecs
import cv2

app = wx.App()

frame = MainWindow(None, 'Редактор Telegram-ботов')
frame.Show()

app.MainLoop()

cv2.waitKey()

krtForParsing = frame.getWordsForParsing()

#allText = ""
#with open("scenery.txt", "r", encoding='utf-8') as file:
#   allText = file.read()
#   print(allText)

print(krtForParsing)
