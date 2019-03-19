#!/usr/bin/python
import tkinter as tk
from PIL import ImageTk, Image
import cv2

# Icon made by Freepik from www.flaticon.com 

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
    label_bw.after(10, video_stream) 

    # RECONSTRUCTED
    #TODO
    label_reconstructed.imgtk = imgtk
    label_reconstructed.configure(image=imgtk)

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

    new_img = cv2.resize(new_img, (128, 128)) #Lose precision
    return cv2.resize(new_img, (400, 400))

video_stream()
window.mainloop()