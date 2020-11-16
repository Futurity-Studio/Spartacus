from Spartacus import Spartacus
import speech_recognition as sr
import pyttsx3

s = Spartacus()


# s.go_to_link()
# s.interact_with_link()
s.query_search_engines("how much does milk cost")


#
# def speak_text(command):
#     # Initialize the engine
#     engine = pyttsx3.init()
#     # voices = engine.getProperty('voices')       #getting details of current voice
#     # engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
#     engine.say(command)
#     engine.runAndWait()
#
#
# r = sr.Recognizer()

# with sr.Microphone() as source:
#     try:
#         print("Say something!")
#         audio = r.listen(source)
#         print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
#     except sr.UnknownValueError:
#         print('error...')
#     except sr.RequestError as e:
#         print('request error')

# speak_text('what is the price of a TV')