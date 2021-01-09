import sys
import bcrypt
import global_module
from database import Database
from patienten import *
from leistungen import *
from rechnungen import *
from calender import *
from user import *
from manage_users import *

db = Database()

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

class login:
    def __init__(self, parent):
        self.TNotebook1=parent

        self.TNotebook1_t0 = ttk.Frame(self.TNotebook1, width=300, height=200)
        self.TNotebook1.add(self.TNotebook1_t0, padding=3)
        self.TNotebook1.tab(0, text="Einloggen", compound="left", underline="-1")

        self.Loginframe = ttk.Frame(self.TNotebook1_t0, width=500, height=400)#, background="#b3e7f4")
        self.Loginframe.place(anchor="c", relx=0.5, rely=0.5)

        self.UsernameLabel = ttk.Label(self.Loginframe)#, bg='#b3e7f4')
        self.UsernameLabel.place(relx=0.121, rely=0.1, height=27, width=140, bordermode='ignore')
        self.UsernameLabel.configure(anchor='w', text='''Benutzname:''', font="Arial 16 bold")

        self.PasswordLabel = ttk.Label(self.Loginframe)#, bg='#b3e7f4')
        self.PasswordLabel.place(relx=0.121, rely=0.35, height=27, width=140, bordermode='ignore')
        self.PasswordLabel.configure(anchor='w', text='''Passwort:''', font="Arial 16 bold")

        self.UsernameEntry = ttk.Entry(self.Loginframe)#, bg='white')
        self.UsernameEntry.place(relx=0.121, rely=0.18, height=40, relwidth=0.764, bordermode='ignore')
        self.UsernameEntry.configure(font="Arial 16 bold")
        self.UsernameEntry.focus()

        self.PasswordEntry = ttk.Entry(self.Loginframe, show="*")#,bg='white')
        self.PasswordEntry.place(relx=0.121, rely=0.43, height=40, relwidth=0.764, bordermode='ignore')
        self.PasswordEntry.configure(font="Arial 16 bold")


        self.entrys()

    def entrys(self):
        if (db.check_tables('users'))== 0:
            self.UsernameEntry.bind("<Return>", self.register)
            self.PasswordEntry.bind("<Return>", self.register)

            self.RegisterButton = ttk.Button(self.Loginframe, width = 20, text = "Register", command = self.register)
            self.RegisterButton.place(relx=0.139, rely=0.6, height=51, width=121, bordermode='ignore')
            self.RegisterButton.bind("<Return>", self.register)

        else:
            self.UsernameEntry.bind("<Return>", self.ValidateLogin)
            self.PasswordEntry.bind("<Return>", self.ValidateLogin)

            self.LoginButton = ttk.Button(self.Loginframe, width = 20, text = "Einloggen", command = self.ValidateLogin)
            self.LoginButton.place(relx=0.139, rely=0.6, height=51, width=121, bordermode='ignore')
            self.LoginButton.bind("<Return>", self.ValidateLogin)

        self.CancelButton = ttk.Button(self.Loginframe, width = 20, text = "Cancel", command = self.CancelLogin)
        self.CancelButton.place(relx=0.644, rely=0.6, height=51, width=121, bordermode='ignore')


    def CancelLogin(self):
        msg=tk.messagebox.askyesno("Login Page", "Möchten Sie die Anmeldung wirklich abbrechen?")
        if(msg):
            sys.exit()

        self.register=0
    def register(self, _event=None):
        self.register=1
        self.salt = global_module.salt
        self.hashed = bcrypt.hashpw(self.PasswordEntry.get().encode(), self.salt)
        data = (self.UsernameEntry.get(),self.hashed, "Administrator**", "False")
        if all(data):
            db.insert_user(data)
            self.entrys()
            self.showerror = tk.Label(self.Loginframe, text="User admin registerd successfuly!", bg="#f6f6f6")#'#b3e7f4')
            self.showerror.place(relx=0.0, rely=0.80, height=51, width=500, bordermode='ignore')
            self.showerror.configure(anchor='center', font="Arial 12 bold", fg="Green")
        else:
            self.showerror = tk.Label(self.Loginframe, text="Bitte, geben Sie Benutzname und Passwort", bg="#f6f6f6")#'#b3e7f4')
            self.showerror.place(relx=0.0, rely=0.80, height=51, width=500, bordermode='ignore')
            self.showerror.configure(anchor='center', font="Arial 12 bold", fg="Red")

    def ValidateLogin(self, _event=None):
        data = (self.UsernameEntry.get(),)
        global_module.active_user=self.UsernameEntry.get()
        inputData = ((self.UsernameEntry.get()), (self.PasswordEntry.get()),)
        if all(inputData):
            if (db.validate_user(data, inputData)):
                self.UsernameEntry.unbind("<Return>")
                self.PasswordEntry.unbind("<Return>")
                self.LoginButton.unbind("<Return>")
                if self.register == 1:
                    self.RegisterButton.unbind("<Return>")
                self.TNotebook1.hide(0)
                isActive=("True", self.UsernameEntry.get())
                db.set_user_active(isActive)
                role = db.get_user_role(data)
                patienten(self.TNotebook1)
                leistungen(self.TNotebook1)
                rechnungen(self.TNotebook1)
                termine(self.TNotebook1)
                if 'Administrator' in role[0][0]:
                    manage_users(self.TNotebook1)
                user(self.TNotebook1)

            else:
                self.showerror = tk.Label(self.Loginframe, text="Wrong Credentials!", bg='#f6f6f6')
                self.showerror.place(relx=0.0, rely=0.80, height=51, width=500, bordermode='ignore')
                self.showerror.configure(anchor='center', font="Arial 12 bold", fg="Red")
        else:
            self.showerror = tk.Label(self.Loginframe, text="Bitte, geben Sie Richtige Benutzname und Passwort", bg="#f6f6f6")#'#b3e7f4')
            self.showerror.place(relx=0.0, rely=0.80, height=51, width=500, bordermode='ignore')
            self.showerror.configure(anchor='center', font="Arial 12 bold", fg="Red")
