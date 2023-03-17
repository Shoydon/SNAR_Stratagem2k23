import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("database-connect\serviceAccountKey.json")
config = {
    'apiKey': 'AIzaSyBOFmA-iFlMR2hvmWBkIhiywO2S46BtfUo',
    'databaseURL': "https://attend-1-91780-default-rtdb.firebaseio.com/", #path to realtime db
    'storageBucket': "attend-1-91780.appspot.com"
}
firebase_admin.initialize_app(cred, config)

ref = db.reference('Students') #ref path to db
#it will create a "Students" directory and we'll store the id's of the students

data = {
    "9240":{
        "name": "Shoy",
        "dep": "comp",
        "start_year": 2020,
        "curr_year": 3,
        "total_attendance": 6,
        "last_att": "2023-01-28 14:37:52"
    },
    "9289":{
        "name": "Zeal",
        "dep": "comp",
        "start_year": 2020,
        "curr_year": 3,
        "total_attendance": 8,
        "last_att": "2023-01-28 14:37:52"
    }

}
#image url, year, section, roll_no, name, department_id

for key, value in data.items():
    ref.child(key).set(value)
