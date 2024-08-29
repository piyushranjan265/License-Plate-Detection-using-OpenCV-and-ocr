import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import numpy as np
import imutils
import time
import requests
import cv2
import os
from tkinter import ttk
import serial

number_plate_list = ["MH20EE0943","MH12KY6445","GJ36L1111","TN39CK6070","GJ01MW7581","MH20BY9602","Unauthorised","num4"]
pname = 0
final_status = ''

try:
    print("[INFO] Connecting To Arduino Board")
    ser = serial.Serial('COM5', 9600, timeout=1)     #enter ur Microcontroller COM port number
    print("Sucessfully Connected")
except:
    print("[INFO] Failed To Connect To Arduino Check COM Port Number And Connection")
    pass


def get_plate_number():
    global pname
    regions = ['in'] # Change to your country
    with open('plate.jpg', 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',data=dict(regions=regions),
            files=dict(upload=fp),
            headers={'Authorization': 'Token b565a03a76bac29d2d04a1ea279bd6f69b006de5'})
    try:    
        plate_number = response.json()['results'][0]['plate']
        pname = plate_number.upper()
        print(pname)
    except:
        print("none")
        pass
	
root = tk.Tk()
root.title("Number Plate Detector")

root.geometry('1100x800')
root.configure(background ="white")

message = tk.Label(root, text="Number Plate violation detection", bg="white", fg="black", width=48,
		   height=2, font=('times', 30, 'italic bold '))
message.place(x=0, y=0)


def close():
    sc1.destroy()

def ok_screen():
    global sc1
    global final_status
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Status')
    sc1.configure(background='snow')
    Label(sc1,text=final_status,fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc1,text='OK',command=close,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)


def get_vio():
        global pname
        print(pname)
        global final_status
        if pname in number_plate_list:
                #ok_screen()
                final_status = "Authorized"
                #GPIO.output(green_led, True)
                #GPIO.output(red_led, False)
                ser.write(b'1')
                #print("Authorised vehicle")
                
        else:
            #ok_screen()
            final_status = "Unauthorized"
            #print("Un-authorised vehicle")
            ser.write(b'2')
            #GPIO.output(green_led, False)
            #GPIO.output(red_led, True) 
            
        print(final_status)
        
def clear():
	cv2.destroyAllWindows()
	rtitle.destroy()

def exit():
		root.destroy()


def on_closing():
	from tkinter import messagebox
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

def analysis():
                global rtitle
                (W, H) = (None, None)
                frame = cv2.imread(path)
                frame = imutils.resize(frame, width=400)
                ori = frame.copy()
                cv2.imwrite("plate.jpg", frame)
                get_plate_number()
                rtitle = tk.Label(text=pname.upper(), background="snow",fg="Black", font=("", 15,'bold'))
                rtitle.place(x=830,y=300)
                clrWindow = tk.Button(root, text="Clear", command=clear  ,fg="black"  ,bg="lawn green"  ,width=15  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                clrWindow.place(x=90, y=600)
                fineWindow = tk.Button(root, text="Submit", command=get_vio  ,fg="black"  ,bg="lawn green"  ,width=15  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                fineWindow.place(x=800, y=400)

def openphoto():
	global path
	
	path=askopenfilename(filetypes=[("Image File",'.jpg')])
	frame = cv2.imread(path)
	cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	cv2image = imutils.resize(cv2image, width=200)
	img = Image.fromarray(cv2image)
	tkimage = ImageTk.PhotoImage(img)
	myvar=tk.Label(root,image = tkimage, height="450", width="350")
	myvar.image = tkimage
	myvar.place(x=350,y=180)
	get_vio()
	preImg = tk.Button(root, text="Predict",fg="black",command=analysis ,bg="lawn green"  ,width=15  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
	preImg.place(x=90, y=450)
	
def capture():
	global path
	cam = cv2.VideoCapture(0)
	time.sleep(0.5)
	ret, img = cam.read()
	captured = cv2.imwrite("./Captured_images/Captured.jpg", img)
	cam.release()
	path = "./Captured_images/Captured.jpg"
	frame = cv2.imread(path)
	cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	cv2image = imutils.resize(cv2image, width=400)
	img = Image.fromarray(cv2image)
	tkimage = ImageTk.PhotoImage(img)
	myvar=tk.Label(root,image = tkimage, height="450", width="350")
	myvar.image = tkimage
	myvar.place(x=350,y=230)
	preImg = tk.Button(root, text="Predict",fg="black",command=analysis ,bg="lawn green"  ,width=15  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
	preImg.place(x=90, y=450)
 
def task():
    #capture()
    root.after(1000, task)  #reschedule event in 1 seconds
	
button1 = tk.Button(root, text="Select Photo",command=openphoto,fg="white"  ,bg="blue2"  ,width=15  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
button1.place(x=90, y=150)

capbut = tk.Button(root, text="Capture",fg="black",command=capture,bg="lawn green"  ,width=15  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
capbut.place(x=90, y=300)

quitWindow = tk.Button(root, text="Quit", command=on_closing  ,fg="white"  ,bg="Red"  ,width=15  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=800, y=530)
root.after(1000, task)
root.mainloop()
print("[INFO] Closing ALL")
print("[INFO] Closed")
