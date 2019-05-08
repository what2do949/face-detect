# face-detect

Python base
Using open-cv and face_recognition to check student info such as class schedules.

<b>Install:</b>
pip install -r requirements.txt

Take sample pictures:
 python3 take-picture.py

This will take picture from your webcam and put your picture in faces directory.
 
<b>Detect faces:</b>
 python3 face-detect.py
 
This pre-load all picture in faces directory and check against new faces in webcam

<b>Mult-thread:</b> Detect faces: functionality implement to automatically detect new pictures take and will poll JSON data every duration.

-Example data [{"teacherName":"Frits","studentList":["邓姝婷","周曦彤","刘军妮","刘燕","王亮"],"className":"16.getting a job","time":"2019-05-08 10:00:00"},]
 
 
 

