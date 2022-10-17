import re
import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial
from tkinter.messagebox import RETRY



window = Tk()

#Database Code
with sqlite3.connect("passwordValut.db") as db:
    cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")    

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")    

#Create Popup
def popUp(text):
    answer = simpledialog.askstring("input string", text)
    print(answer)
    return answer


#Initiate Window
window.title("Passwor vault")

def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash

def firstScreen():
    window.geometry("250x150")

    lbl = Label(window, text="Create Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=30, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text="Re-enter Password")
    lbl1.pack()

    txt1 = Entry(window, width=30, show="*")
    txt1.pack()
    txt1.focus()

    lbl2 = Label(window)
    lbl2.pack()

    def savePassword():
        if txt.get() == txt1.get():
            hashedPassowrd = hashPassword(txt.get().encode('utf-8'))

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password, [(hashedPassowrd)])
            db.commit()

            passwordVault()
        else:
            lbl2.config(text="Password do not match")

    btn = Button(window, text="Save", command=savePassword) 
    btn.pack(pady=10)


def loginScreen():
    window.geometry("350x150")

    lbl = Label(window, text="Enter Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=30, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.pack()

    def getMasterPassword():
        checkHashedPassword = hashedPassowrd = hashPassword(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        # print(checkHashedPassword)
        return cursor.fetchall()
       

    def checkPassword():
        match = getMasterPassword()
        print(match)

        if match:
            # print("Right password")
            passwordVault()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong password")          


    btn = Button(window, text="Submit", command=checkPassword) 
    btn.pack(pady=10)


def passwordVault():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"

        website = popUp(text1)
        username = popUp(text2)
        password = popUp(text3)

        insert_fields = """INSERT INTO vault(website,username,password)
        VALUES(?, ?, ?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        passwordVault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id =?", (input,))
        db.commit()

        passwordVault()

    window.geometry("750x350")

    lbl = Label(window, text="Password Vault")
    lbl.grid(column=1)

    btn = Button(window, text="+", command=addEntry)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx=80)    

    cursor.execute("SELECT * FROM vault")
    if(cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()
            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl1.grid(column=1, row=i+3)
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl1.grid(column=2, row=i+3)   

            btn = Button(window, text="Delete", command= partial(removeEntry, array[i][0]))        
            btn.grid(column=3, row=i+3, pady=10)     

            i = i+1

            cursor.execute("SELECT * FROM vault")
            if(len(cursor.fetchall()) <= i):
                break        




# firstScreen()
# loginScreen()
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()
window.mainloop()