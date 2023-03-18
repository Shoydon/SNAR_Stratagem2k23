from dataclasses import replace
import time
import datetime
import gspread

import tkinter as tk
from tkinter import Message ,Text
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

#doctor with their resp room number and disease
doctors = {
    "cough": "001",
    "cold": "002",
    "bodypain": "003"
}


gc = gspread.service_account(filename = "./key.json")
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1CFKt6rV5E1LIcmDMFrXSJklfpmPvtsrwvkCHp36FLac/edit#gid=0")
wks = sh.worksheet("appointments")
# counter = wks.get("F1") #number of reservations
value = wks.acell("F1").value
counter = int(0 if value is None else value) #number of reservations

sheet_id = "1089766924"
spreadsheet_id = '1CFKt6rV5E1LIcmDMFrXSJklfpmPvtsrwvkCHp36FLac'

# if(counter == 0):
#     print("F1 empty")
#     wks.update("F1",0)

wks.update("A1","NAME")
wks.update("B1","DISEASE")
wks.update("C1","TOKEN NUMBER")
wks.format("A1", {'textFormat': {'bold': True}})
wks.format("B1", {'textFormat': {'bold': True}})
wks.format("C1", {'textFormat': {'bold': True}})

window = tk.Tk()
window.title("Book appointment")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

window.geometry("2000x700")
window.configure(background='#2b2d42')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="Appointment Booking" ,bg="#8d99ae"  ,fg="#edf2f4"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 
message.place(x=200, y=20)

name_label = tk.Label(window, text="Enter your name",width=30  ,height=2  ,fg="#edf2f4"  ,bg="#ef233c" ,font=('times', 15, ' bold ') ) 
name_label.place(x=400, y=200)
name_field = tk.Entry(window,width=20  ,bg="#8d99ae" ,fg="#edf2f4",font=('times', 15, ' bold '))
name_field.place(x=800, y=215)


choice = "1"
while(choice != "0"):

    value = wks.acell("F1").value
    counter = int(0 if value is None else value)
    wks.update("F1", counter)

    choice = input("0. EXIT\n1. Book appointment\n2. Done\nChoice: ")

    if choice == "1":
        c_curr = counter+2
        curr_res = str(c_curr)

        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")

        name = input("name: ")
        disease = input("disease: ")

        dis_num = doctors.get(disease)

        wks.update(f"A{curr_res}", name)
        wks.update(f"B{curr_res}", disease)
        # tok = "00"+str(dis_num)+":"+Hour+Minute+Second
        tok = dis_num+":"+Hour+Minute+Second
        wks.update(f"C{curr_res}", tok)
        counter+=1
        wks.update("F1", counter)

    elif choice == "2":
        # request_body = {
        #     "requests": [
        #         {
        #             "deleteDimension": {
        #                 'sheetId': sheet_id,
        #                 'dimension': 'ROWS',
        #                 'startIndex': 1,
        #                 'endIndex': 1 
        #             }
        #         }
        #     ]
        # }

        # wks.batch_update(
        #     spreadsheetId = spreadsheet_id,
        #     body = request_body
        # )
        for i in range(2, counter+1):
            a2 = wks.acell(f"A{i+1}").value
            b2 = wks.acell(f"B{i+1}").value
            c2 = wks.acell(f"C{i+1}").value

            wks.update(f"A{i}", a2) 
            wks.update(f"B{i}", b2) 
            wks.update(f"C{i}", c2) 
            
        wks.update(f"A{i+1}", " ") 
        wks.update(f"B{i+1}", " ") 
        wks.update(f"C{i+1}", " ") 

        counter-=1
        wks.update("F1", counter)

wks.format("A2", {'textFormat': {'bold': False}})
wks.format("B2", {'textFormat': {'bold': False}})
wks.format("C2", {'textFormat': {'bold': False}})

# print(wks, counter)

# print(type(counter))