import speech_recognition as sr
import keyboard
from utils.text_to_speech import text_to_speech_with_google
from config import PICOVOICE_API_KEY, DEFAULT_DEVICE_INDEX
import os
import wave
import struct
from typing import Dict
import pveagle
from pvrecorder import PvRecorder

PROFILE_FOLDER = "eagle_profiles"
audiopath = "audio.wav"

class EagleProfile(object):

    def __init__(self, data: bytes) -> None:
        self.data = data
    
def load_user_profiles() -> Dict[str, EagleProfile]:
    profiles = {}
    if os.path.exists(PROFILE_FOLDER):
        for filename in os.listdir(PROFILE_FOLDER):
            if filename.endswith(".bin"):
                profile_name = os.path.splitext(filename)[0]
                profile_path = os.path.join(PROFILE_FOLDER, filename)
                with open(profile_path, 'rb') as f:
                    profile_data = pveagle.EagleProfile.from_bytes(f.read())
                    profiles[profile_name] = EagleProfile(profile_data)
                print(f"Loaded profile: {profile_name}")
    else:
        print(f"Profile folder '{PROFILE_FOLDER}' does not exist.")
    return profiles

def speak_text(text):
    text_to_speech_with_google(text)

def get_audio_input():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Press and hold the F9 key to start listening...")
    keyboard.wait('F9')
    print("Listening...")

    with mic as source:
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results from the service.")
        return None
    
def get_audio_input_with_user_verification(eagle):
    recognizer = sr.Recognizer()

    print("Press and hold the F9 key to start listening...")
    keyboard.wait('F9')
    print("Listening...")

    recognized_user = None
    highest_scores = record_and_recognize(load_user_profiles(), eagle)

    for name, score in highest_scores.items():
        print(f"Highest score for '{name}': {score}")
        if score > 0.8:
            recognized_user = name
            break

    if recognized_user:
        print(f"User recognized: {recognized_user}")
        try:
            with sr.AudioFile(audiopath) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
            print(f"{recognized_user} said: {text}")
            return text, recognized_user
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak_text("Sorry, I did not understand that.")
            return None, None
        except sr.RequestError as e:
            print(f"Could not request results from the service; {e}")
            speak_text("Could not request results from the service.")
            return None, None
    else:
        print("Unauthorized user.")
        speak_text("Unauthorized user.")
        return None, None

def record_and_recognize(profiles, eagle):

    recognizer_recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle.frame_length)
    
    recognizer_recorder.start()

    highest_scores = {}
    audio = []
    try:
        while True:
            if not keyboard.is_pressed('F9'):  # Check if F9 key is released
                break
            audio_frame = recognizer_recorder.read()
            scores = eagle.process(audio_frame)
            audio.extend(audio_frame)
            for i, score in enumerate(scores):
                name = list(profiles.keys())[i]
                if name not in highest_scores or score > highest_scores[name]:
                    highest_scores[name] = score
            print(highest_scores)
    except KeyboardInterrupt:
        print("Recognition stopped by user.")

    recognizer_recorder.stop()

    with wave.open(audiopath, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))

    return highest_scores

