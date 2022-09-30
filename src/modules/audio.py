from modules.operations import *
import speech_recognition as sr
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard


def record_audio():
    freq = 44100
    duration = 20
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    write("data\\audio.wav", freq, recording)