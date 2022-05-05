from moviepy.editor import *
import cv2
from PIL import Image, ImageSequence
import shutil
import os

def changeVideoResolution(path, resolution): 
    # путь к файлу, кортеж - разрешение (напр. (480, 480)), новое имя (с расширением файла)
    extension = getFileExtension(path)
    supportFileName = getFilePathWithoutFname(path)+"supportFile"+extension
    shutil.copy(path, supportFileName)
    video = VideoFileClip(path)
    result = video.resize(resolution)
    result.write_videofile(supportFileName)
    os.remove(path)
    shutil.copy(supportFileName, path)
    os.remove(supportFileName)
    
def changeImageResolution(path, resolution): 
    # путь к файлу, кортеж - разрешение (напр. (480, 480)), новое имя (с расширением файла)
    extension = getFileExtension(path)
    supportFileName = getFilePathWithoutFname(path)+"supportFile"+extension
    shutil.copy(path, supportFileName)
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    result = cv2.resize(image, resolution)
    cv2.imwrite(supportFileName, result)
    os.remove(path)
    shutil.copy(supportFileName, path)
    os.remove(supportFileName)
    
    
def changeGIFResolution(path, resolution):  
    extension = getFileExtension(path)
    supportFileName = getFilePathWithoutFname(path)+"supportFile"+extension
    shutil.copy(path, supportFileName)
    gif = Image.open(path)
    frames = ImageSequence.Iterator(gif)
    frames = thumbnails(frames, resolution)
    om = next(frames) # Handle first frame separately
    om.info = gif.info # Copy sequence info
    om.save(supportFileName, save_all=True, append_images=list(frames), loop=0)
    os.remove(path)
    shutil.copy(supportFileName, path)
    os.remove(supportFileName)


def thumbnails(frames, resolution): # вспомогательная функция
    # Output (max) size
    #size = 320, 240
    #size = resolution
    for frame in frames:
        thumbnail = frame.copy()
        #thumbnail.thumbnail(size, Image.ANTIALIAS)
        thumbnail = thumbnail.resize(resolution)
        yield thumbnail

def getFileExtension(path):
    lastDotIndex = path.rindex(".")
    return path[lastDotIndex:]

def getFilePathWithoutFname(path):
    try:
        lastIndexOfSlash = path.rindex("/")
    except:
        lastIndexOfSlash = 0
    return path[:lastIndexOfSlash]

#changeVideoResolution("face.mp4", (480, 480))

