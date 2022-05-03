from moviepy.editor import *
import cv2

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