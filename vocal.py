from playsound import playsound
from gtts import gTTS
import os
class Vocal:

	def __init__(self):
		self.nom = 'Welcome to the password management software ,STOCK'

	def synthese(self):
            tts = gTTS(self.nom,'en')
            tts.save('hello.mp3')
            playsound('hello.mp3')
            os.remove("hello.mp3")
