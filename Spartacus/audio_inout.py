import pyttsx3
import speech_recognition as sr


def audio_out(command):
    # Initialize the engine
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices')       #getting details of current voice
    # engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    engine.say(command)
    engine.runAndWait()


def audio_in():
    r = sr.Recognizer()
    recognized_audio = ''
    with sr.Microphone() as source:
        try:
            print("Mic Listening")
            audio = r.listen(source)
            recognized_audio = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + recognized_audio)
        except sr.UnknownValueError:
            print('error...')
        except sr.RequestError as e:
            print('request error')
    return recognized_audio



