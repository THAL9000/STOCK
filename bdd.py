import sqlite3
class Bdd:
   
    def __init__(self):
        self.connexion = sqlite3.connect("bdd.db")
    def end_program(self):
        self.connexion.close()
    def hash_bdd(self):
        curseur=self.connexion.cursor()
        curseur.execute("SELECT hash FROM cochon")
        result = curseur.fetchone()
        hash = result[0]
        self.connexion.commit()
        return hash;
