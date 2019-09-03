from colorama import init
from colorama import Fore, Back, Style
import sqlite3
init()
class Opening:

	def __init__(self):
		self.nom = 'Hash'

	def hash(self):
            liste_presentation=["","Type your password if you don't have configured this","Type 2 if you have already configured","Type 3 if you want exit this app"]
            print(Fore.YELLOW +"Setting")
            a=0
            while a<3:
               a+=1
               print(Fore.YELLOW +liste_presentation[a])
            choix=input()
            connexion = sqlite3.connect("bdd.db")
            curseur=connexion.cursor()
            if choix=="3":
               exit()
            elif choix=="2":
               return 0;
            else:
               choix_encode=choix.encode("utf-8")
               hashed = bcrypt.hashpw(choix_encode, bcrypt.gensalt())
               curseur.execute('''CREATE TABLE IF NOT EXISTS cochon(hash TEXT)''')
               curseur.execute('''INSERT INTO cochon (hash) VALUES (?)''', [hashed])
               connexion.commit()
