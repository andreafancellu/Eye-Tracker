from modules.operations import *
import speech_recognition as sr
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard


def speech_to_text(stopThread):
    recognizer = sr.Recognizer()
    check = True
    global textAudio
    textAudio = ""
    file = open("data\\text.txt", "w")
    file.close()

    while check:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            if keyboard.is_pressed('q'):
                check = False
                break
            textAudio = textAudio + " " + recognizer.recognize_google(audio, language="it-IT")
        except Exception as e:
            print(e)
        if stopThread:
            check = False
            break


def record_audio():
    freq = 44100
    duration = 20
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    write("data\\audio.wav", freq, recording)