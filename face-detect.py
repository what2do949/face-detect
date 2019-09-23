import face_recognition
import cv2
import os
import numpy as np
import requests
import json
import pyttsx3
import sys
import datetime
import time
import threading

if sys.version_info[0] >= 3:
    unicode = str
from PIL import ImageFont, ImageDraw, Image
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one
engine = pyttsx3.init()
engine.startLoop(False)
scanned = {}
toSay = ""
width, height = 720,480

class Student:

    # Class Attribute

    # Initializer / Instance Attributes
    def __init__(self, name, teacherName, className, time, ):
        self.name = name
        self.teacherName = teacherName
        self.className = className
        self.time = time

studentObjDict = {}
studentTimeDict = {}

def getStudentInfo(fStop):

    #response = requests.get("http://release.zhen-yee.com/jh/data/api/classes")
    #loaded_json = json.loads(response.text)
    global loaded_json 
    global studentObjDict
    global studentTimeDict

    with open('class.json') as f:
    	loaded_json = json.load(f)

    for x in loaded_json:
        studentList = x['studentList']
        for student in studentList:
            if((student in studentObjDict) == False):
                d = datetime.datetime.strptime(x['time'], "%Y-%m-%d %H:%M:%S")
                if( datetime.datetime.now() + datetime.timedelta(minutes = 30) < d ):
                    studentObjDict[student] =  (Student(student, x['teacherName'], x['className'], x['time']))
                    studentTimeDict[student] =  x['time']
            else:
                d = datetime.datetime.strptime(x['time'], "%Y-%m-%d %H:%M:%S")
                previousTime = studentTimeDict.get(student)
                previousTime = datetime.datetime.strptime(previousTime, "%Y-%m-%d %H:%M:%S")
                if( d > previousTime) and ( datetime.datetime.now() + datetime.timedelta(minutes = 30) < d ):
                    studentObjDict[student] =  (Student(student, x['teacherName'], x['className'], x['time']))
                    studentTimeDict[student] =  x['time']
    if not fStop.is_set():
        # call f() again in 60 seconds
        threading.Timer(60, getStudentInfo, [fStop]).start()

fStop = threading.Event()
getStudentInfo(fStop)

video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
pictureFoldersList = []
images = {} 
first = 0

known_face_encodings = []
known_face_names = []

def loadFolder(pStop):
    face_dir = "faces" 
    counter = 0
    for dir in os.listdir(face_dir):
        #print (dir)
        path =  os.path.join(face_dir, dir)
        if os.path.isdir(path): 
            counter = counter  + 1
            i = 0
            for jpg in os.listdir(face_dir + "/" + dir + "/"): 
                if(jpg.lower().endswith(".jpg") and not (jpg.startswith('.'))):
                    if not dir in pictureFoldersList:
                        image_object = face_recognition.load_image_file(face_dir + "/" + dir + "/" + jpg)
                        try:
                            images[dir]  = face_recognition.face_encodings(image_object)[i] 
                            i = i + 1
                            pictureFoldersList.append(dir)
                            global first 
                            if ( first != 0):
                                print ("Processing " +  str(counter) +  "... " + dir + "\n")
                                global known_face_encodings 
                                global known_face_names
                                known_face_encodings.append(images[dir])
                                known_face_names.append(key.replace("_" , " "))

                        except IndexError:
                            print (dir + " picture can not scan")
                        continue
    if not pStop.is_set():
        first = 1
        # call f() again in 60 seconds
        threading.Timer(60, loadFolder, [pStop]).start()

pStop = threading.Event()
loadFolder(pStop)

#biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
    

for key, value in images.items():
    known_face_encodings.append(value)
    known_face_names.append(key.replace("_" , " "))


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        #face_locations = face_recognition.face_locations(rgb_small_frame, model="knn",number_of_times_to_upsample=2)
        face_locations = face_recognition.face_locations(rgb_small_frame, model="knn")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, known_face_locations=face_locations )
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.35)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            #if matches[0] == True:
            #    first_match_index = 0
            #    name = known_face_names[0]
             
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4 
        right *= 4
        bottom *= 4 
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 2)
        #pts = np.array([[100,5],[20,30],[70,20],[50,10]], np.int32)
        #pts = pts.reshape((-1,1,2))
        #cv2.polylines(frame,[pts],True,(0,255,255))
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 0), (right, bottom), (255, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        b,g,r,a = 255,0,0,0
        toSay = False
        if name != "Unknown":
            findStudent = False
            fontpath = "./FZLTXHJW.TTF" # <== 这里是宋体路径
            font = ImageFont.truetype(fontpath, 32)
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            if name in studentObjDict:
                student = studentObjDict.get(name)  
                #print("student " + student.name)
                if(student.name == name):
                    draw.text((50, 80),  name, font = font, fill = (b, g, r, a))
                    draw.text((50, 160),  student.className, font = font, fill = (b, g, r, a))
                    img = np.array(img_pil)
                    cv2.putText(img,  student.time, (100,300), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (b,g,r), 1, cv2.LINE_AA)
                    #cv2.putText(img,  student.className, (100,320), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (b,g,r), 1, cv2.LINE_AA)
                    frame = img
                    if(name in scanned):
                        rightNow = datetime.datetime.now()
                        lastTime = scanned.get(name)
                        #print(scanned.get(name))
                        if( rightNow > lastTime):
                            toSay = True
                    else:
                        toSay = True
                    if(toSay):
                        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.ting-ting')
                        engine.say(unicode(name))
                        engine.say(unicode(student.className))
                        scanned[name] = datetime.datetime.now() + datetime.timedelta(seconds = 15)
                    #engine.say(" is in class " + student.className  );
                    engine.iterate()

                    #cv2.imshow("res", img);cv2.waitKey();cv2.destroyAllWindows()
                    #cv2.putText(frame, name  , (left + 6, bottom - 70), font, 1.0, (255, 255, 255), 1)
                    #cv2.putText(frame, student.time.str()  , (left + 6, bottom - 35), font, 1.0, (255, 255, 255), 1)
                    #cv2.putText(frame, student.className  , (left + 6, bottom - 5), font, 1.0, (255, 255, 255), 1)
                    findStudent = True
            
            else:
                draw.text((50, 80),  "Hi " + name + "You have no class now", font = font, fill = (b, g, r, a))
                cv2.putText(frame,  "No class found" , (100,300), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (b,g,r), 1, cv2.LINE_AA)
                #if(findStudent):
                    #scanned[name] =  datetime.datetime.now() + datetime.timedelta(seconds = 30)
                    #break
 
    # Display the resulting image
    frame = cv2.resize(frame, (width, height))
    cv2.imshow('Video', frame)
    if(toSay):
        time.sleep(2)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
engine.endLoop()
