#!/usr/bin/python
import tkinter as tk
from PIL import ImageTk, Image
import cv2
import configparser
import os
import numpy as np
from keras.models import load_model

# Icon made by Freepik from www.flaticon.com 

conf = configparser.ConfigParser()
if not os.path.isfile('config.ini'):
    conf['VIDEO'] = {
    'VIDEO_FEED_SIZE' : 400,
    'VIDEO_PROCESS_SIZE' : 224,
    'VIDEO_CAPTURE_RATE' : 100,
    }

    conf['ML'] = { 
    'MODEL_NAME' : "coloRayzor.h5",
    }
    
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)
else:
    conf.read('config.ini')

try:
    VIDEO_FEED_SIZE = int(conf['VIDEO']['VIDEO_FEED_SIZE'])
    VIDEO_PROCESS_SIZE = int(conf['VIDEO']['VIDEO_PROCESS_SIZE'])
    VIDEO_CAPTURE_RATE = int(conf['VIDEO']['VIDEO_CAPTURE_RATE'])
    ML_MODEL_NAME = str(conf['ML']['MODEL_NAME'])
except:
    print("An error occured while reading the config file.")
    exit()


window = tk.Tk()
window.title("ColoRayzor")
window.bind('<Escape>', lambda e: window.quit())
window.resizable(False, False)
window.iconbitmap('icon_color.ico')
app = tk.Frame(window)
app.grid()

# CAMERA FEED
label_camera = tk.Label(app)
label_camera.grid(column = 0, row=0)

label_info_camera = tk.Label(app)
label_info_camera.grid(column = 0, row = 1)
label_info_camera['text'] = "Camera Feed"

# BLACK AND WHITE IMAGE
label_bw = tk.Label(app)
label_bw.grid(column = 1, row = 0)

label_info_bw = tk.Label(app)
label_info_bw.grid(column = 1, row = 1)
label_info_bw['text'] = "GrayScaled"

# RECONSTRUCTED
label_reconstructed = tk.Label(app)
label_reconstructed.grid(column = 2, row = 0)

label_info_reconstructed = tk.Label(app)
label_info_reconstructed.grid(column = 2, row = 1)
label_info_reconstructed['text'] = "Re-colored"

# Capture from camera
cap = cv2.VideoCapture(0)

# Keras model
model = load_model(ML_MODEL_NAME)

# function for video streaming
def video_stream():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = crop_square(frame)

    # CAMERA FEED
    image_camera = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(image_camera)
    imgtk = ImageTk.PhotoImage(image=img)
    label_camera.imgtk = imgtk
    label_camera.configure(image=imgtk)

    # BLACK AND WHITE IMAGE
    image_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img2 = Image.fromarray(image_bw)
    imgtk2 = ImageTk.PhotoImage(image=img2)
    label_bw.imgtk = imgtk2
    label_bw.configure(image=imgtk2)
    label_bw.after(VIDEO_CAPTURE_RATE, video_stream) 

    # RECONSTRUCTED
    image_scaled_bw = cv2.resize(image_bw, (VIDEO_PROCESS_SIZE, VIDEO_PROCESS_SIZE))
    image_reconstructed = np.uint8(model.predict(image_scaled_bw.reshape(1,VIDEO_PROCESS_SIZE,VIDEO_PROCESS_SIZE,1)/255)[0]*255)
    img3 = Image.fromarray(cv2.resize(image_reconstructed, (VIDEO_FEED_SIZE, VIDEO_FEED_SIZE)))
    imgtk3 = ImageTk.PhotoImage(image=img3)
    label_reconstructed.imgtk = imgtk3
    label_reconstructed.configure(image=imgtk3)

def crop_square(img):
    w = img.shape[0]
    h = img.shape[1]

    little_size = h
    big_size = w
    if w < h:
        little_size = w
        big_size = h
    offset = big_size - little_size

    if w < h:
        new_img = img[ : , offset//2 : big_size-(offset//2)]
    else:
        new_img = img[ offset//2 : big_size-(offset//2) , : ]

    new_img = cv2.resize(new_img, (VIDEO_PROCESS_SIZE, VIDEO_PROCESS_SIZE)) #Lose precision
    return cv2.resize(new_img, (VIDEO_FEED_SIZE, VIDEO_FEED_SIZE))

video_stream()
window.mainloop()