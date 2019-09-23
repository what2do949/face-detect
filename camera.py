import tkinter as tk
import os
import cv2
from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as tkMessageBox
from multiprocessing import Process, Queue



width, height = 720,480
cap = cv2.VideoCapture(0)
flag,frame=cap.read()


cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()

tk.Label(root, lmain, text="Enter Usernname", compound=tk.CENTER).pack()
entry = tk.Entry(root, width=10)
entry.pack(side=tk.TOP,padx=10,pady=10)


entry.delete(0, tk.END)
entry.insert(END, "")

def onTakePicture():
    s = entry.get()
    if not s:
        tkMessageBox.showinfo(title=s,message="Usename can not be empty")
        return
    mypath="faces" + "/" +  s
    if not os.path.exists(mypath):
        os.mkdir(mypath)
    saveImage(mypath + "/" +s + ".jpg")

def onClose():
    quit()

def saveImage(imagePath):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (width, height)) 
    cv2.imshow("test", frame)
    cv2.imwrite(imagePath, frame)

tk.Button(root, text='Take Picture', command=onTakePicture).pack()
tk.Button(root, text='CLOSE', command=onClose).pack(side= tk.RIGHT)

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (width, height)) 
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)




show_frame()
root.mainloop()
