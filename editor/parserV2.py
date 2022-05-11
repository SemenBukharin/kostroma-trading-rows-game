# -*- coding: utf-8 -*-
from code_analyzer import *
from bot_message import *
import os.path

class Scene:
    """Класс сцены Telegram-бота"""

    def __init__(self, name, messages, waitingElements):
        self.sceneMessages = messages
        self.name = name
        self.trash = waitingElements

    def getName(self):
        return self.name

    def getSceneMessages(self):
        return self.sceneMessages

def getScenery(words, resPath):    
    elements = []
    token = ""
    text = ""

    # для сцен
    currentSceneName = ""
    scenes = []
    currentScene = None
    
    waitSomething = []

    def getSceneByName(sceneName):
        for sc in scenes:
            if sc.getName()==sceneName:
                return sc

    # для группы
    groupMessageFlag = False
    textFound = False
    groupMessage = []
    
    ind = 0 # индекс текущего кортежа
    while True:
        if words[ind][0]==CodeAnalyzer.BOT and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            if words[ind][2]==CodeAnalyzer.STRING:
                token = words[ind][0][1:len(words[ind][0])-1]
                print(token) 
                ind += 1
                if not words[ind][0]==CodeAnalyzer.COLON:
                    raise Exception(f'Ожидилось ключевое слово {CodeAnalyzer.COLON} . Строка {words[ind-1][1]}')
                else:
                    ind +=1
            else:
                raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.BOT}. Строка {words[ind-1][1]}')
        elif words[ind][0]==CodeAnalyzer.BOT_END and words[ind][2]==CodeAnalyzer.KEYWORD:
            break
        elif words[ind][0]==CodeAnalyzer.SCENE and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            if words[ind][2]==CodeAnalyzer.STRING:
               currentSceneName =  words[ind][0][1:len(words[ind][0])-1]
               print(currentSceneName)
               ind += 1
               if not words[ind][0]==CodeAnalyzer.COLON:
                   raise Exception(f'Ожидилось ключевое слово {CodeAnalyzer.COLON} . Строка {words[ind-1][1]}')
               else:
                   ind +=1
            else:
                 raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.SCENE}. Строка {words[ind-1][1]}')
        elif words[ind][0]==CodeAnalyzer.SCENE_END and words[ind][2]==CodeAnalyzer.KEYWORD:
            scenes.append(Scene(currentSceneName, elements, waitSomething))
            elements = []
            print (waitSomething)
            waitSomething = []
            currentName = ""
            ind += 1
        elif words[ind][0]==CodeAnalyzer.TEXT and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            if words[ind][2]==CodeAnalyzer.STRING:
                el = TextPost(words[ind][0][1:len(words[ind][0])-1])               
                if groupMessageFlag:
                   if not textFound:
                       groupMessage.append(el)
                       textFound = True
                   else:
                       raise Exception(f'В текущей группе уже есть текст! Строка {words[ind-1][1]}')
                else:
                   elements.append(el)
                print("текст "+words[ind][0][1:len(words[ind][0])-1])
                ind += 1
            else:
                 raise Exception(f'Ожидилась строка(и) в кавычках после ключевого слова {CodeAnalyzer.TEXT}. Строка {words[ind-1][1]}')
        elif words[ind][0]==CodeAnalyzer.PHOTO and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            try:
                el = ImagePost(resPath+words[ind][0][1:len(words[ind][0])-1])
            except Exception as e:
                raise Exception (str(e)+f" Строка {words[ind][1]}")
            if groupMessageFlag:
                groupMessage.append(el)
            else:
                elements.append(el)
            print(words[ind][0][1:len(words[ind][0])-1])
            ind += 1                
            #if words[ind][2]==CodeAnalyzer.KEYWORD:
            #        raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.PHOTO}. Строка {words[ind-1][1]}')                
        elif words[ind][0]==CodeAnalyzer.VOICE and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            try:
                elements.append(VoicePost(resPath+words[ind][0][1:len(words[ind][0])-1]))
            except Exception as e:
                raise Exception (str(e)+f" Строка {words[ind][1]}")
            print(words[ind][0][1:len(words[ind][0])-1])
            ind += 1
            #if words[ind][2]==CodeAnalyzer.KEYWORD:
            #    raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.VOICE}. Строка {words[ind-1][1]}')                
        elif words[ind][0]==CodeAnalyzer.AUDIO and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1 
            try:
                el = AudioPost(resPath+words[ind][0][1:len(words[ind][0])-1])                    
            except Exception as e:
                raise Exception (str(e)+f" Строка {words[ind][1]}")
            if groupMessageFlag:
                groupMessage.append(el)
            else:
                elements.append(el)
            print(words[ind][0][1:len(words[ind][0])-1])
            ind += 1
            #if words[ind][2]==CodeAnalyzer.KEYWORD:
            #   raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.AUDIO}. Строка {words[ind-1][1]}')                
        elif words[ind][0]==CodeAnalyzer.VIDEO and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1 
            try:
                el = VideoPost(resPath+words[ind][0][1:len(words[ind][0])-1])
            except Exceprion as e:
                raise Exception (str(e)+f" Строка {words[ind][1]}")
            if groupMessageFlag:
                groupMessage.append(el)
            else:
                elements.append(el)
            print(words[ind][0][1:len(words[ind][0])-1])
            ind += 1        
            #if words[ind][2]==CodeAnalyzer.KEYWORD:
            #    raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.VIDEO}. Строка {words[ind-1][1]}')            
        elif words[ind][0]==CodeAnalyzer.ROUND and words[ind][2]==CodeAnalyzer.KEYWORD:
             ind += 1   
             try:
                 el = RoundPost(resPath+words[ind][0][1:len(words[ind][0])-1])
             except Exception as e:
                 raise Exception (str(e)+f" Строка {words[ind][1]}")
             elements.append(el)
             print("Круг "+words[ind][0][1:len(words[ind][0])-1])
             ind += 1
             #if words[ind][2]==CodeAnalyzer.KEYWORD:
             #   raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.ROUND}. Строка {words[ind-1][1]}')             
        elif words[ind][0]==CodeAnalyzer.GIF and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1  
            try:
                elements.append(GifPost(resPath+words[ind][0][1:len(words[ind][0])-1]))
            except Exception as e:
                raise Exception (str(e)+f" Строка {words[ind][1]}")
            print(words[ind][0][1:len(words[ind][0])-1])
            ind += 1
            #if words[ind][2]==CodeAnalyzer.KEYWORD:
            #    raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.GIF}. Строка {words[ind-1][1]}')            
        elif words[ind][0]==CodeAnalyzer.DOC and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            try:
                el = DocPost(resPath+words[ind][0][1:len(words[ind][0])-1])
            except Exception as e:
                raise Exception (str(e)+f" Строка {words[ind][1]}")
            if groupMessageFlag:
                groupMessage.append(el)
            else:
                elements.append(el)
            print(words[ind][0][1:len(words[ind][0])-1])
            ind += 1
            #if words[ind][2]==CodeAnalyzer.KEYWORD:
            #    raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.DOC}. Строка {words[ind-1][1]}')            
        elif words[ind][0]==CodeAnalyzer.STICKER and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1  
            try:
                elements.append(StickerPost(resPath+words[ind][0][1:len(words[ind][0])-1]))
            except Exception as e:
                raise Exception (str(e)+f" Строка {words[ind][1]}")
            print(words[ind][0][1:len(words[ind][0])-1])
            ind += 1
            #if words[ind][2]==CodeAnalyzer.KEYWORD:
            #    raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.STICKER}. Строка {words[ind-1][1]}')            
        elif words[ind][0]==CodeAnalyzer.GROUP and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            groupMessageFlag = True
            print("Группа найдена!")
            if words[ind][0]!=CodeAnalyzer.COLON:
                raise Exception(f'Ожидилось ключевое слово {CodeAnalyzer.COLON} . Строка {words[ind-1][1]}')
            else:
                ind += 1
        elif words[ind][0]==CodeAnalyzer.GROUP_END and words[ind][2]==CodeAnalyzer.KEYWORD:
            ind += 1
            groupMessageFlag = False
            elements.append(GroupPost(groupMessage))
            textFound = False
            groupMessage = []
        elif words[ind][0]==CodeAnalyzer.BUTTONS and words[ind][2]==CodeAnalyzer.KEYWORD:
            buttons = []
            waitSomething.append(words[ind])
            ind += 1
            if words[ind][2]==CodeAnalyzer.STRING:
                buttonsDescription = words[ind][0][1:len(words[ind][0])-1]
                if groupMessageFlag:
                   raise Exception(f'Кнопки не могут входить в группу! Строка {words[ind-1][1]}')
                else:
                   print(buttonsDescription)
                ind += 1
                if not words[ind][0]==CodeAnalyzer.COLON:
                    raise Exception(f'Ожидилось ключевое слово {CodeAnalyzer.COLON} . Строка {words[ind-1][1]}')
                else:
                    ind +=1
                    while words[ind][0]!=CodeAnalyzer.BUTTONS_END:
                        if words[ind][2]==CodeAnalyzer.STRING:
                            buttons.append(Button(words[ind][0][1:len(words[ind][0])-1]))
                            print(words[ind][0][1:len(words[ind][0])-1])
                            ind += 1                            
                            if words[ind][0]!=CodeAnalyzer.DOUBLE_DASH:
                                raise Exception(f"Ожидалось ключевое слово {CodeAnalyzer.DOUBLE_DASH}. Строка {words[ind-1][1]}")
                            else:
                                ind += 1
                                if words[ind-1][1]!=words[ind][1]:
                                    raise Exception(f"Отсутствует действие у кнопки. Строка {words[ind-1][1]}")
                            print(f'Действие: {words[ind][0]}')
                            ind += 1
                    waitSomething.append(words[ind])
                    #if words[ind][2]==CodeAnalyzer.KEYWORD and words[ind][1]!=words[ind-1][1]:
                    #   raise Exception(f'Ожидилось ключевое слово {CodeAnalyzer.BUTTONS_END}. Строка {words[ind][1]}')
                    #print(f'Действие: {words[ind-1][0]}')                    
                    elements.append(ButtonsPost(buttonsDescription, buttons))
            else:
                 raise Exception(f'Ожидилась строка(и) в кавычках после ключевого слова {CodeAnalyzer.BUTTONS}. Строка {words[ind-1][1]}')
        elif words[ind][0]==CodeAnalyzer.WAIT_AUDIO and words[ind][2]==CodeAnalyzer.KEYWORD:
            waitSomething.append(words[ind])
            ind += 1
            while words[ind][0]!=CodeAnalyzer.WAIT_END:
                waitSomething.append(words[ind])
                ind += 1
            waitSomething.append(words[ind])
        elif words[ind][0]==CodeAnalyzer.WAIT_TEXT and words[ind][2]==CodeAnalyzer.KEYWORD:
            waitSomething.append(words[ind])
            ind += 1            
            while words[ind][0]!=CodeAnalyzer.WAIT_END:
                waitSomething.append(words[ind])
                ind += 1
            waitSomething.append(words[ind])
        elif words[ind][0]==CodeAnalyzer.TRANSITION and words[ind][2]==CodeAnalyzer.KEYWORD:
            waitSomething.append(words[ind])
            ind += 1
            if words[ind][2]==CodeAnalyzer.KEYWORD:
                raise Exception(f'Ожидилась строка в кавычках после ключевого слова {CodeAnalyzer.PHOTO}. Строка {words[ind-1][1]}')
            waitSomething.append(words[ind])                    
        else:
            ind += 1
            if ind>len(words)-1:
                break        
    for sc in scenes:
        allMessages += sc.getSceneMessages()
        
    
        
    return allMessages
           
