import datetime
import os
import time
import imutils
import cv2
from gtts import gTTS
from playsound import playsound
from pygame import mixer
import sqlite3

file1="result.mp3"
file2="result.txt"
if os.path.exists(file1)==True:
    os.remove(file1)
if os.path.exists(file2)==True:
    os.remove(file2)

#-------------------------
def recognize_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    connection=sqlite3.connect("Database.db")
    font = cv2.FONT_HERSHEY_SIMPLEX
    query="CREATE TABLE IF NOT EXISTS BlindDBRecognized (Time Text,ID INTEGER ,Name TEXT NOT NULL);"
    cursor=connection.cursor()
    cursor.execute(query)
    query2="SELECT * FROM Blindvision WHERE ID=?"
    query3="INSERT OR IGNORE INTO BlindDBRecognized (Time,ID,Name) VALUES (? ,? ,?)"
    query4="SELECT Name FROM BlindDBRecognized WHERE Time=?"
    q="DROP TABLE IF EXISTS temp_table;"
    cursor.execute(q)
    connection.commit()
    

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    t_end = time.time() + 5 #stay in the loop for 5 seconds
    

    while (time.time() < t_end):
        ret, im = cam.read()
        im=imutils.resize(im, width=400)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(im, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 1)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            cursor.execute(query2,(Id,))
            records=cursor.fetchall()

            if conf < 100:

                for row in records:
                    aa = row[1]
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa


            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            if (100-conf) > 10:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                for dat in records:
                    Name=dat[1]
                    Id=dat[0]
                val=(timeStamp,Id,Name)
                cursor.execute(query3,val)
                connection.commit()
                val1=(timeStamp,)
                result = cursor.execute(query4,val1)
                
                

            tt = str(tt) #[2:-2]


            if(100-conf) > 20:
                cv2.putText(im, str(tt), (x+5,y-5), font, 0.5, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 0.5, (255, 255, 255), 2)

            if (100-conf) > 17:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
            elif (100-conf) > 10:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)
            
#             for x in result:
#                 print(x)


        cv2.imshow('Recognizer', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    
    q1="CREATE TABLE temp_table as SELECT DISTINCT * FROM BlindDBRecognized;"
    q2="DELETE FROM BlindDBRecognized;" 
    q3="INSERT INTO BlindDBRecognized SELECT * FROM temp_table"
    cursor.execute(q1)
    cursor.execute(q2)
    cursor.execute(q3)
    cursor.execute(q)
    connection.commit()
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
    val1=(timeStamp,)
    result = cursor.execute(query4,val1)
    f= open("result.txt","a+")
    for x in result:
        print(x[0])
        f.write(x[0])
        f.write("\n")
    f.close()
    if os.path.exists(file2)==True:
        f= open("result.txt", "r")
        text = f.read()
        f.close()
        tts = gTTS(text)
        tts.save("result.mp3")

        with audioread.audio_open('result.mp3') as f:
            totalsec = f.duration
        
        p=vlc.MediaPlayer("result.mp3")
        p.play()
        time.sleep(totalsec)
    
    else:
        tts=gTTS("Recognision Failed Please Try Again")
        tts.save("result.mp3")
        with audioread.audio_open('result.mp3') as f:
            totalsec = f.duration
        
        p=vlc.MediaPlayer("result.mp3")
        p.play()
        time.sleep(totalsec)

    
recognize_face()
os.remove("result.mp3")
os.remove("result.txt") 
