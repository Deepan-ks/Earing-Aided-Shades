from gtts import gTTS
from playsound import playsound
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from googletrans import Translator  
import os
pytesseract.pytesseract.tesseract_cmd = r'path to the tesseract engine'
mytext = pytesseract.image_to_string(Image.open('path to the image to be used'))
print(mytext)
translator = Translator() 
translated = translator.translate(mytext, src='en', dest='ta') #user desired language
print(translated.text)
language = 'ta' 
myobj = gTTS(text=translated.text, lang=language, slow=False) 
myobj.save("welcome.mp3") 
os.system("mpg123 welcome.mp3")
playsound('welcome.mp3')
