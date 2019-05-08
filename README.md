# face-detect

<b>Why create this app</b>: For schools or meeting halls so student/particpants can check what classroom and time they suppose to attend. This will later extend to taking attendence once backend components are implemented. This will save time and money and give more time for teachers to teach and students to learn.

Python base:
Using open-cv and face_recognition to check student info such as class schedules.

<b>Install:</b>
pip install -r requirements.txt

Take sample pictures:
 python3 take-picture.py

-This will take photo from your webcam and put your photo in faces directory.
 
<b>Detect faces:</b>
 python3 face-detect.py
 
-This pre-load all picture in faces directory and check against your face in webcam

<b>Mult-thread:</b> Detect faces functionality implemented to automatically detect new photo input to faces directory and also will poll JSON data every duration.

-Example data [{"teacherName":"Frits","studentList":["邓姝婷","周曦彤","刘军妮","刘燕","王亮"],"className":"16.getting a job","time":"2019-05-08 10:00:00"},]

-Future release: Backend database support for attendence gathering.
 
 
 

