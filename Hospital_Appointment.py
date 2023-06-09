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

window = tk.Tk()
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

window.configure(background='#2b2d42')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="Hospital Appointment Booking System" ,bg="#8d99ae"  ,fg="#edf2f4"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

message.place(x=200, y=20)

Patient = tk.Button(window, text="Patient Page", command=PatientUI ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
Patient.place(x=200, y=650)
Staff = tk.Button(window, text="Train Model", command=staffUI  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
Staff.place(x=500, y=650)
window.mainloop()


def PatientUI():
    window = tk.Tk()
    window.title("Face_Recogniser")

    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'

    window.configure(background='#2b2d42')

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    message = tk.Label(window, text="Hospital Appointment Booking System" ,bg="#8d99ae"  ,fg="#edf2f4"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

    message.place(x=200, y=20)

    lbl = tk.Label(window, text="Enter DOB(DDMMYY)",width=30  ,height=2  ,fg="#edf2f4"  ,bg="#ef233c" ,font=('times', 15, ' bold ') ) 
    lbl.place(x=400, y=200)

    txt = tk.Entry(window,width=20  ,bg="#8d99ae" ,fg="#edf2f4",font=('times', 15, ' bold '))
    txt.place(x=800, y=215)

    lbl2 = tk.Label(window, text="Enter Patient Name",width=30  ,fg="#edf2f4"  ,bg="#ef233c"    ,height=2 ,font=('times', 15, ' bold ')) 
    lbl2.place(x=400, y=270)

    txt2 = tk.Entry(window,width=20  ,bg="#8d99ae"  ,fg="#edf2f4",font=('times', 15, ' bold ')  )
    txt2.place(x=800, y=290)

    lbl3 = tk.Label(window, text="Enter reason of Visit",width=30  ,fg="#edf2f4"  ,bg="#ef233c"    ,height=2 ,font=('times', 15, ' bold ')) 
    lbl3.place(x=400, y=340)

    txt3 = tk.Entry(window,width=20  ,bg="#8d99ae"  ,fg="#edf2f4",font=('times', 15, ' bold ')  )
    txt3.place(x=800, y=360)

    lbl6 = tk.Label(window, text="Enter Doctor's Name : ",width=30  ,fg="#edf2f4"  ,bg="#ef233c"    ,height=2 ,font=('times', 15, ' bold ')) 
    lbl6.place(x=400, y=410)
    txt4 = tk.Entry(window,width=20  ,bg="#8d99ae"  ,fg="#edf2f4",font=('times', 15, ' bold ')  )
    txt4.place(x=800, y=430)

    lbl4 = tk.Label(window, text="Status : ",width=40  ,fg="#edf2f4"  ,bg="#ef233c"  ,height=2 ,font=('times', 15,'bold')) 
    lbl4.place(x=400, y=480)

    message = tk.Label(window, text="" ,bg="#ef233c"  ,fg="#edf2f4"  ,width=30  ,height=2, activebackground = "#d90429" ,font=('times', 15, ' bold ')) 
    message.place(x=800, y=480)

    def clear():
        txt.delete(0, 'end')    
        res = ""
        message.configure(text= res)

    def clear2():
        txt2.delete(0, 'end')    
        res = ""
        message.configure(text= res)    
        
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
    
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
    
        return False

    def TakeImages():        
        Id=(txt.get())
        name=(txt2.get())
        doctor=(txt4.get())
        reason=(txt3.get())

        if(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>59:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = " ID : " + Id +"   Name : "+ name
            row = [Id , name, doctor, reason]
            with open('PatientDetails\PatientDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)

    def TrainImages():
    
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImage\Trainner.yml")
        res = "Image Trained"
        message.configure(text= res)

    def getImagesAndLabels(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        
        faces=[]
        Ids=[]
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)        
        return faces,Ids

    takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
    takeImg.place(x=200, y=650)
    trainImg = tk.Button(window, text="Train Model", command=TrainImages  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
    trainImg.place(x=500, y=650)

    quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
    quitWindow.place(x=1100, y=650)



    window.mainloop()


def staffUI():
    window = tk.Tk()
    window.title("Face_Recogniser")

    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'

    window.configure(background='#2b2d42')

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    message = tk.Label(window, text="Face Recognition to Confirm Appointment" ,bg="#8d99ae"  ,fg="#edf2f4"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

    message.place(x=200, y=20)

    lbl5 = tk.Label(window, text="Recognition Results : ",width=30  ,fg="#edf2f4"  ,bg="#ef233c"  ,height=2 ,font=('times', 15)) 
    lbl5.place(x=400, y=200)


    message2 = tk.Label(window, text="" ,fg="#edf2f4"   ,bg="#ef233c",activeforeground = "green",width=50  ,height=5  ,font=('times', 15, ' bold ')) 
    message2.place(x=800, y=200)

    lbl6 = tk.Label(window, text="Token Generated : ",width=30  ,fg="#edf2f4"  ,bg="#ef233c"  ,height=2 ,font=('times', 15)) 
    lbl6.place(x=400, y=400)

    message3 = tk.Label(window, text="" ,fg="#edf2f4"   ,bg="#ef233c",activeforeground = "green",width=50  ,height=5  ,font=('times', 15, ' bold ')) 
    message3.place(x=800, y=400)

    def TrackImages():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        # cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainingImage\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("PatientDetails\PatientDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        # col_names =  ['Id','Name','Date','Time']
        col_names =  ['Id','Name','Doctor','Date','Time','Token']

        attendance = pd.DataFrame(columns = col_names)    
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.3,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    listdoctors={"Leslie": 101, "Francis": 102, "Pramod": 201,"Subhash":202,"Chris":301,"Myron":302}
                    print(df.loc[df.Id==Id]['Doctor Name'])
                    docname=df.loc[df.Id==Id]['Doctor Name'].to_numpy()
                    # gentoken=df.loc[df.Id==Id]['Token'].to_numpy()

                    docname=docname[0]
                    # print(df)
                    print(docname)
                    tokennumber=listdoctors.get(docname)
                    tokentime=datetime.datetime.fromtimestamp(ts).strftime('%H%M')
                    token=f"{tokennumber} : {tokentime}"
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    bb=df.loc[df['Id'] == Id]['Doctor Name'].values
                    

                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,bb,date,timeStamp,token]
                    
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\Attendance.csv"
        attendance.to_csv(fileName,index=False)
        # gentoken=attendance.loc[len(attendance)][token]
        cam.release()
        cv2.destroyAllWindows()
        #print(attendance)
        res=attendance
        res2=token
        message3.configure(text=res2)
        message2.configure(text= res)

    trackImg = tk.Button(window, text="Recognise Face", command=TrackImages  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
    trackImg.place(x=600, y=650)
    quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
    quitWindow.place(x=600, y=650)

    window.mainloop()

