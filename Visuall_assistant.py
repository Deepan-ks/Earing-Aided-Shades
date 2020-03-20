import PIL                      # Python Imaging Library
import gtts                     # Google's text to Speech API
import cv2                      # opecv Library
import pytesseract              # used for image to text conversion using OCR
from PIL import Image           # used for handling image type file
from gtts import gTTS                    
import numpy as np
import time       
import os
import speech_recognition as sr # speech recognition python package
import imutils
import subprocess
from pydub import AudioSegment
from playsound import playsound
from googletrans import Translator
AudioSegment.ffmpeg = r"path to the FFmpeg"
ch=0
count=0
tts = gTTS(text=" device turned on", lang='en',slow=False)
tts.save("audio.mp3")
os.system("mpg123 audio.mp3")
playsound("audio.mp3")
os.remove("audio.mp3")
while ch!=4:
    print("***WELCOME***")
    print("press 1: READING MODE")
    print("press 2: SCRIBE MODE")
    print("press 3: VISION MODE")
    print("press 4: Exit")
    tts = gTTS(text="press 1 for READING MODE ,press 2 for SCRIBE MODE  press 3 for VISION MODE press 4 for Exit", lang='en',slow=False)
    tts.save("audio.mp3")
    os.system("mpg123 audio.mp3")
    playsound("audio.mp3")
    os.remove("audio.mp3")
    ch= int(input())
    
    if ch==1 :
        pytesseract.pytesseract.tesseract_cmd = r'path to the tesseract engine'
        mytext = pytesseract.image_to_string(Image.open('path to the image'))
        print(mytext)
        translator = Translator() 
        translated = translator.translate(mytext, src='en', dest='ta') # use dest & src for user desired language
        print(translated.text)
        language = 'ta' 
        myobj = gTTS(text=translated.text, lang=language, slow=False) 
        myobj.save("welcome.mp3") 
        os.system("mpg123 welcome.mp3")
        playsound('welcome.mp3')
        os.remove('welcome.mp3')
    elif ch==2 :
        f = open("MyFile.txt", "r") # name the file that contains the questions
        for x in f:
            count=0
            print("Question:"+x)
            tts = gTTS(text=x, lang='en',slow=False)
            tts.save("audio.mp3")
            os.system("mpg123 audio.mp3")
            playsound("audio.mp3")
            os.remove("audio.mp3")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    while count!=1:
                        audio = None
                        count+=1
                        audio = r.listen(source)
                        try:
                            file = open('Myfile1.txt','a+') # name of the file where answer is to be stored
                            print("Answer:"+r.recognize_google(audio))
                            file.write("ANSWER:"+r.recognize_google(audio)+"\n")
                        except sr.UnknownValueError:
                            myobj = gTTS(text="could not understand please try again", lang='en', slow=False)
                            myobj.save("wel.mp3") 
                            os.system("mpg123 wel.mp3")
                            playsound('wel.mp3')
                            os.remove('wel.mp3')
    elif ch==3:
        # load the COCO class labels our YOLO model was trained on
        LABELS = open("provide the path to the COCO Label in your pc").read().strip().split("\n")

        # load our YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO] Initializing YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet("path to the yolo.cfg", "path to the yolo weights")
        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # initialize
        cap = cv2.VideoCapture(0)
        frame_count = 0
        start = time.time()
        first = True
        frames = []

        while True:
                frame_count += 1
            # Capture frame-by-frameq
                ret, frame = cap.read()
                frame = cv2.flip(frame,1)
                frames.append(frame)

                if frame_count == 300: 
                        break
                if ret:
                        key = cv2.waitKey(1)
                        if frame_count % 60 == 0:
                                end = time.time()
                                (H, W) = frame.shape[:2]
                                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                        swapRB=True, crop=False)
                                net.setInput(blob)
                                layerOutputs = net.forward(ln)
                                boxes = []
                                confidences = []
                                classIDs = []
                                centers = []
                                for output in layerOutputs:
                                        for detection in output:
                                                scores = detection[5:]
                                                classID = np.argmax(scores)
                                                confidence = scores[classID]
                                                if confidence > 0.5:
                                                        box = detection[0:4] * np.array([W, H, W, H])
                                                        (centerX, centerY, width, height) = box.astype("int")
                                                        x = int(centerX - (width / 2))
                                                        y = int(centerY - (height / 2))
                                                        boxes.append([x, y, int(width), int(height)])
                                                        confidences.append(float(confidence))
                                                        classIDs.append(classID)
                                                        centers.append((centerX, centerY))
                                idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
                                texts = []
                                if len(idxs) > 0:
                                        for i in idxs.flatten():
                                                centerX, centerY = centers[i][0], centers[i][1]
                                                if centerX <= W/3:
                                                        W_pos = "left "
                                                elif centerX <= (W/3 * 2):
                                                        W_pos = "center "
                                                else:
                                                        W_pos = "right "
                                                
                                                if centerY <= H/3:
                                                        H_pos = "top "
                                                elif centerY <= (H/3 * 2):
                                                        H_pos = "mid "
                                                else:
                                                        H_pos = "bottom "

                                                texts.append(H_pos + W_pos + LABELS[classIDs[i]])

                                print(texts)
                                
                                if texts:
                                        description = ', '.join(texts)
                                        tts = gTTS(description, lang='en')
                                        tts.save('tts.mp3')
                                        tts = AudioSegment.from_mp3("tts.mp3")
                                        subprocess.call(["ffplay", "-nodisp", "-autoexit", "tts.mp3"])
                                
        cap.release()
        cv2.destroyAllWindows()
        os.remove("tts.mp3")
        
    elif ch!=3:
        myobj = gTTS(text="Device is turning off, good bye", lang='en', slow=False)
        myobj.save("we.mp3") 
        os.system("mpg123 we.mp3")
        print("Device is turning off, good bye")
        playsound('we.mp3')
        os.remove('we.mp3')

