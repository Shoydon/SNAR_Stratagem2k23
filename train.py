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

#----------------
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("database-connect\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attend-1-91780-default-rtdb.firebaseio.com/", #path to realtime db
    'storageBucket': "attend-1-91780.appspot.com"
})
#---------------

window = tk.Tk()
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
 
window.configure(background='#2b2d42')


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


message = tk.Label(window, text="Face Recognition Based Attendance System" ,bg="#8d99ae"  ,fg="#edf2f4"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="#edf2f4"  ,bg="#ef233c" ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20  ,bg="#8d99ae" ,fg="#edf2f4",font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="#edf2f4"  ,bg="#ef233c"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20  ,bg="#8d99ae"  ,fg="#edf2f4",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)

lbl3 = tk.Label(window, text="Status : ",width=20  ,fg="#edf2f4"  ,bg="#ef233c"  ,height=2 ,font=('times', 15,'bold')) 
lbl3.place(x=400, y=400)

message = tk.Label(window, text="" ,bg="#ef233c"  ,fg="#edf2f4"  ,width=30  ,height=2, activebackground = "#d90429" ,font=('times', 15, ' bold ')) 
message.place(x=700, y=400)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="#edf2f4"  ,bg="#ef233c"  ,height=2 ,font=('times', 15)) 
lbl3.place(x=400, y=650)


message2 = tk.Label(window, text="" ,fg="#edf2f4"   ,bg="#ef233c",activeforeground = "green",width=30  ,height=5  ,font=('times', 15, ' bold ')) 
message2.place(x=700, y=650)
 
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
                
                #RECONFIGURE THE CODE TO STORE DIRECTLY IN FIREBASE 
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 29
            elif sampleNum>29:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +"   Name : "+ name
        row = [Id , name]

        #RECONFIGURE THE CODE TO ACCESS DIRECTLY FROM FIREBASE 
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
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
    #-----------------------------------
    
    faces,Id = getImagesAndLabels("TrainingImage")
    # faces,Id = getImagesAndLabels("https://console.firebase.google.com/u/1/project/attend-1-91780/storage/attend-1-91780.appspot.com/files")
    
    #-----------------------------------
    recognizer.train(faces, np.array(Id))

    #RECONFIGURE THE CODE TO STORE DIRECTLY IN FIREBASE 
    recognizer.save("TrainingImage\Trainner.yml")
    #----------------------------------
    
    fileName = f'{"TrainingImage"}/{"Trainner.yml"}'
    # fileName = os.path.split(imagePath)[1]
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
    #----------------------------------
    res = "Image Trained"
    message.configure(text= res)

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        
        #RECONFIGURE THE CODE TO ACCESS DIRECTLY FROM FIREBASE 
        pilImage=Image.open(imagePath).convert('L')
        #----------------------------------

        # bucket = storage.bucket()
        # blob1 = bucket.get_blob()

        #----------------------------------        
        imageNp=np.array(pilImage,'uint8')
        
        #RECONFIGURE THE CODE TO ACCESS DIRECTLY FROM FIREBASE 
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        
        faces.append(imageNp)
        Ids.append(Id)  
#----------------------
        
        # fileName = f'{path}/{os.path.split(imagePath)[1]}'
        # # fileName = os.path.split(imagePath)[1]
        # blob = bucket.blob(fileName)
        # blob.upload_from_filename(fileName)
        # path.parent.mkdir(parents=True, exist_ok=True)
#----------------------
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # cv2.createLBPHFaceRecognizer()
    
    #RECONFIGURE THE CODE TO ACCESS DIRECTLY FROM FIREBASE 
    recognizer.read("TrainingImage\Trainner.yml")
    
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);  
    
    #RECONFIGURE THE CODE TO ACCESS DIRECTLY FROM FIREBASE 
    df=pd.read_csv("StudentDetails\StudentDetails.csv")

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                
                #RECONFIGURE THE CODE TO STORE DIRECTLY IN FIREBASE 
                noOfFile=len(os.listdir("ImagesUnknown"))+1

                #RECONFIGURE THE CODE TO STORE DIRECTLY IN FIREBASE 
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

    #RECONFIGURE THE CODE TO ACCESS DIRECTLY FROM FIREBASE 
    att_fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(att_fileName,index=False)
    
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    message2.configure(text= res)

  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="#edf2f4"  ,bg="#ef233c"  ,width=20  ,height=2 ,activebackground = "#d90429" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="#edf2f4"  ,bg="#ef233c"  ,width=20  ,height=2, activebackground = "#d90429" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Model", command=TrainImages  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Mark Attendance", command=TrackImages  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
trackImg.place(x=800, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="#edf2f4"  ,bg="#3a86ff"  ,width=20  ,height=3, activebackground = "#d90429" ,font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=500)

 
window.mainloop()


# #ACCESS IMAGE FROM FIREBASE
# bucket = storage.bucket()
# blob = bucket.get_blob(`imgpath`)
# #blob -> array of bytes
# arr = np.frombuffer(blob.download_as_string(), np.unint8)

# # array of bytes -> actual image
# img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)

# #UPLOAD IMAGE INTO FIREBASE
# fileName = `filepath`
# bucket = storage.bucket()
# blob = bucket.blob(fileName)
# blob.upload_from_filename(fileName)








