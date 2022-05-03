from moviepy.editor import *
import cv2
from PIL import Image, ImageSequence

def changeVideoResolution(path, resolution, newName): 
    # путь к файлу, кортеж - разрешение (напр. (480, 480)), новое имя (с расширением файла)
    video = VideoFileClip(path)
    result = video.resize(resolution)
    result.write_videofile(newName)
    
def changeImageResolution(path, resolution, newName): 
    # путь к файлу, кортеж - разрешение (напр. (480, 480)), новое имя (с расширением файла)
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    result = cv2.resize(image, resolution)
    cv2.imwrite(newName, result)
    
def changeGIFResolution(path, resolution, newName):     
    gif = Image.open(path)
    frames = ImageSequence.Iterator(gif)
    frames = thumbnails(frames, resolution)
    om = next(frames) # Handle first frame separately
    om.info = gif.info # Copy sequence info
    om.save(newName, save_all=True, append_images=list(frames), loop=0)
    
def thumbnails(frames, resolution): # вспомогательная функция
    # Output (max) size
    #size = 320, 240
    #size = resolution
    for frame in frames:
        thumbnail = frame.copy()
        #thumbnail.thumbnail(size, Image.ANTIALIAS)
        thumbnail = thumbnail.resize(resolution)
        yield thumbnail