from gtts import gTTS
import speech_recognition as sr
import webbrowser
import smtplib
from playsound import playsound
import datetime
import random2
import serial

# Function to process and provide voice
def voice(audio):

    tts = gTTS(text=audio, lang='en')
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    tts.save(filename)
    playsound(filename)
    # tts = gTTS(text=audio, lang='en')
    # tts.save('audio.mp3')
    # playsound('audio.mp3')
    os.remove(filename)


# Listens for commands
def myCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        voice('I am ready for your command')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        #print('You said: ' + command + '\n')


    # loop back to continue to listen for commands
    except sr.UnknownValueError:
        voice('Your last command could not be heard')
        command = myCommand()

    return command


# Action to be carried out
def action(command):
    ser = serial.Serial(port,baudrate=9600,timeout=0.5)

    while 1: # Infinite loop
        
        if "Go" in command: 
            Move = True
            voice('Proceeding')
           
        
        if "Stop" in command:
            Move = False
            voice('Stopping')


while True:
    action(myCommand())