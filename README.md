# face-detect

Python base
Using open-cv and face_recognition to check student info such as class schedules.

Install:
pip install -r requirements.txt

Take sample pictures:
 python3 take-picture.py
 #this will take picture from your webcam and put your picture in faces directory.
 
Detect faces:
 python3 face-detect.py
 #This pre-load all picture in faces directory and check against new faces in webcam
 #muli-thread functionality implement to automatically detect new pictures take.
 #faces are check against json server : Example data [{"teacherName":"Frits","studentList":["邓姝婷","周曦彤","刘军妮","刘燕","王亮"],"className":"16.getting a job","time":"2019-05-08 10:00:00"},]
 
 
 

