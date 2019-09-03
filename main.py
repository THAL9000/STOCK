#Script pour le logiciel de stockage de mot de passe
#presentation de l'utilisation des différentes libs:
#utilisation de la lib tkinter pour l'interface graphique
#utilisation de sqlite3 pour les bases de données
#utilisation de bcrypt pour le hashage
#utilisation de crypto pour chiffrer/déchiffrer
#utilisation de dropbox pour l'importation/exportation de bdd
#utilisation de gtts+playsound pour synthse vocale+jouer le son
from tkinter import *
from tkinter import font
import time
from opening import Opening
from vocal import Vocal
from cypher import Cypher
from bdd import Bdd
import bdd
import cypher
from colorama import Fore, Back, Style
import sqlite3
import os
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import   AES
from Crypto.Util.Padding import pad,unpad
import bcrypt
import colorama
import base64
from playsound import playsound
from gtts import gTTS
from colorama import init
#initialisation pour le programme
init()
hash_bdd="rien"
anti_brute_force=0
color_background="#2a374c"
color_resp="green"
connexion = sqlite3.connect("bdd.db")
window=Tk()
police2=font.Font(family='Arial',size=10,weight='bold')
title2 = Button(window,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
title_2_2 = Button(window,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
mail=StringVar()
identify=StringVar()
fa2_value=StringVar()
voice  = IntVar()
window_add=Toplevel(window)
add_mail=StringVar()
add_identify=StringVar()
add_password_up=StringVar()
resp=""
int_encrypt=0
nombre_error=0
color="#0b2e66"
def decrypt():
    sqlite=Bdd()
    reading=sqlite.hash_bdd()
    global mail
    global identify
    global title2
    global police2
    global anti_brute_force
    global voice
    title2.pack()
    a=0
    b=0
    mot_finale=[]
    identify_encode=identify.get().encode("utf-8")
    mail_encode1=mail.get()
    if bcrypt.checkpw(identify_encode,reading):
      liste=list(identify.get())
      while a<16:
            a+=1
            mot_finale.append(liste[b])
            b+=1
            if b==len(liste):
               b=0
            else:
              continue
      mot_finale2=''.join(mot_finale)
      crypt = Cypher(mot_finale2)
      encryption_test=crypt.encrypt(mail_encode1)
      curseur3=connexion.cursor()
      curseur3.execute("SELECT mail FROM auth")
      result = curseur3.fetchall()
      search_password=[]
      for resultat in result:
              result_decode=result[0]
              search_password.append(resultat[0])
      connexion.commit()
      curseur4 =connexion.cursor()
      a=0
      for element in search_password:
          if element==encryption_test:
           curseur4.execute("SELECT pass FROM auth WHERE mail=?",[element])
           result2 = curseur4.fetchone()
           connexion.commit()
           crypt = Cypher(mot_finale2)
           unpad_decrypt=crypt.decrypt(result2[0])
           if voice.get()==1:
              tts = gTTS('Your password is '+unpad_decrypt,'en')
              tts.save('voice.mp3')
              playsound('voice.mp3')
              os.remove("voice.mp3")
              return 0
           else:
              resp="The password is"+unpad_decrypt
              color_resp="green"
              title2.pack_forget()
              title2 = Button(window, text=resp,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
              title2.pack()
              connexion.commit()
              a=0
              anti_brute_force=0
              return 0
          else:
             a=5
      if a==5:
            resp="the email was not found"
            color_resp="red"
            title2.pack_forget()
            title2 = Button(window, text=resp,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
            title2.pack()
            connexion.commit()
            return 0
    else:
       if anti_brute_force==6:
         resp="Anti brute force activated for 30 seconds of inactivity"
         anti_brute_force=0
       else:
         resp="The ID is false"
       color_resp="red"
       title2.pack_forget()
       title2 = Button(window, text=resp,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
       title2.pack()
       return 0
       if resp=="Anti brute force activated for 30 seconds of inactivity":
         time.sleep(30)
       anti_brute_force+=1
       connexion.commit()
    global nombre_error
    nombre_error+=1
    color_resp="grey"
    resp="ok"
    if nombre_error==1:
      title2 = Button(window, text=resp,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
    else:
     title2.pack_forget()

def encrypt():
    global window_add
    global add_identify
    global add_password_up
    global add_mail
    add_police=font.Font(family='Arial',size=25,weight='bold')
    add_police2=font.Font(family='Arial',size=10,weight='bold')
    add_photo = PhotoImage(file='logo.png')
    add_title = Button(window_add,text="Adding an account",bg=color_background,fg='white',width = 1000,height=1,borderwidth=0,font=add_police)
    add_saut_ligne = Button(window_add,text="Enter the name of the account",bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=add_police2)
    add_saut_ligne1 = Button(window_add,text="..and your password",bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=add_police2)
    add_saut_ligne2 = Button(window_add,bg=color_background,fg='grey',width = 100,height=5,borderwidth=0)
    add_button_active = Button(window_add, text="Adding an account",bg="black",fg='white',width = 40,height=2,borderwidth=0,command=encrypt_test,font=add_police2)
    add_saut_ligne3 = Button(window_add,bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=add_police2)
    add_saut_ligne4 = Button(window_add,text="..and enter your ID",bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=add_police2)
    add_saut_ligne5 = Button(window_add,bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=add_police2)
    title2_2 = Button(window_add, text="",bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
    title2_2.pack()
    add_title.pack()
    add_saut_ligne.pack()
    add_mail_entry=Entry(window_add,textvariable=add_mail,width=30)
    add_mail_entry.pack()
    add_saut_ligne1.pack()
    add_password_up=Entry(window_add,show="*",textvariable=add_password_up,width=30)
    add_password_up.pack()
    add_saut_ligne4.pack()
    add_identify_entry=Entry(window_add,textvariable=add_identify,width=30)
    add_identify_entry.pack()
    add_saut_ligne2.pack()
    add_button_active.pack()
    window_add.title("STOCK|password software")
    window_add.configure(background=color_background)
    window_add.geometry('850x690+700+10')
    window_add.iconbitmap(r"nuage.ico")
    window_add.resizable(0,0)
    print(add_identify.get())
    window_add.mainloop()
    

def encrypt_test():
    global add_identify
    global add_password_up    
    global title_2_2
    global connexion
    title_2_2.pack()
    sqlite=Bdd()
    reading=sqlite.hash_bdd()
    identify_encode1=add_identify.get().encode("utf-8")
    mail_encode=add_mail.get()
    password_encode=add_password_up.get()
    a=0
    mot_finale=[]
    b=0
    if bcrypt.checkpw(identify_encode1,reading):
     liste=list(add_identify.get())
     while a<16:
         a+=1
         mot_finale.append(liste[b])
         b+=1
         if b==len(liste):
            b=0
         else:
           continue
     mot_finale2=''.join(mot_finale)
     crypt = Cypher(mot_finale2)
     id1 = crypt.encrypt(mail_encode)
     id2 = crypt.encrypt(password_encode)
     curseur_ajout=connexion.cursor()
     curseur_ajout.executescript('''
     CREATE TABLE IF NOT EXISTS auth(
       mail TEXT,
       pass TEXT)''')
     curseur_ajout.execute("SELECT mail FROM auth WHERE mail=?",[id1])
     result2 = curseur_ajout.fetchall()
     if result2 != []:
        color_resp="red"
        resp="The email already exists"
        title2_2 = Button(window_add, text=resp,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
        title2_2.pack()
        return 0
     color_resp="green"
     curseur_ajout.execute("PRAGMA table_info(auth);")
     curseur_ajout.execute('''INSERT INTO auth (mail,pass) VALUES (?,?)''', (id1,id2))
     connexion.commit()
     resp="Email and password added"
     title2_2 = Button(window_add, text=resp,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
     title2_2.pack()
     return 0
    else:
        color_resp="red"
        resp="The ID is false"
        title2_2 = Button(window_add, text=resp,bg=color_background,fg=color_resp,width = 1000,height=2,borderwidth=0,font=police2)
        title2_2.pack()
        
def main():
  open=Opening()
  open.hash()
  svocal=Vocal()
  svocal.synthese()
  sqlite=Bdd()
  global identify
  global mail
  global police2
  global voice
  police=font.Font(family='Arial',size=25,weight='bold')
  police2=font.Font(family='Arial',size=10,weight='bold')
  photo = PhotoImage(file='logo.png')
  logo = Button(window,image=photo,bg=color_background,fg='white',width = 1000,height=100,borderwidth=0,font=police)
  title = Button(window,text="STOCK",bg=color_background,fg='white',width = 1000,height=1,borderwidth=0,font=police)
  saut_ligne = Button(window,text="Your email",bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=police2)
  saut_ligne1 = Button(window,text="Your ID",bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=police2)
  button_active = Button(window, text="view your password",bg="black",fg='white',width = 40,height=2,borderwidth=0,command=decrypt,font=police2)
  saut_ligne3 = Button(window,bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=police2)
  saut_ligne4 = Button(window,bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=police2)
  saut_ligne5 = Button(window,bg=color_background,fg='white',width = 100,height=3,borderwidth=0,font=police2)
  identife=Entry(window,show="*",textvariable=identify,width=30)
  window.title("STOCK|software password")
  logo.pack()
  title.pack()
  saut_ligne.pack()
  mail_entry=Entry(window,textvariable=mail,width=30)
  mail_entry.pack()
  saut_ligne1.pack()
  identife=Entry(window,show="*",textvariable=identify,width=30)
  identife.pack()
  saut_ligne4.pack()
  button_active.pack()
  saut_ligne3.pack()
  valide_voice= Checkbutton(window, text="say the password (voice synthesis)",background=color_background,variable=voice)
  valide_voice.pack()
  window.configure(background=color_background)
  window.geometry('850x690+0+10')
  window.iconbitmap(r"nuage.ico")
  window.resizable(0,0)
  encrypt()
  window.mainloop()
  sqlite.end_program()

if __name__ == '__main__':
    main()
