import sys
import bcrypt
import time
from tkinter import *
from ttkthemes import ThemedStyle
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from database import Database
from image_base64 import user_icon
import global_module

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

_bgcolor = '#f6f6f6'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#5dbf33' # X11 color: 'gray85'
_ana1color = '#f6f6f6' # X11 color: 'gray85'
_ana2color = '#f6f6f6' # Closest X11 color: 'gray92'

class user:
    def __init__(self, parent):

        self.TNotebook1=parent
        photo = PhotoImage(data = user_icon)
        self.menubutton = tk.Menubutton(self.TNotebook1,borderwidth=0, bg=_bgcolor, activebackground=_bgcolor, image = photo)
        self.menubutton.image = photo
        # Create pull down menu
        menu = Menu(self.menubutton,tearoff=0, bg=_bgcolor, activebackground='green', font='Arial 14')
        self.menubutton.config(menu=menu)

        # Add some commands
        self.username=global_module.active_user 
        menu.add_command(label=self.username)
        menu.add_command(label="Passwort ändern", command=self.change_user_pass)
        menu.add_command(label="Ausloggen", command=self.user_logout)
        menu.add_command(label="Beenden", command=self.Exit)

        #menubutton.pack(padx=1, pady=50)
        self.menubutton.place(relx=0.95, rely=0.005, height=80, width=80)

    def change_user_pass(self):
        self.root = tk.Tk(className='Passwort ändern')
        style = ThemedStyle(self.root)
        if sys.platform == "win32":
            pass
        else:
            style.set_theme("plastik")
            self.root.attributes ("-alpha", "0.5")
        self.root.resizable(0, 0)
        self.root.geometry("510x410")
        self.root.title("Passwort ändern")

        self.style = ttk.Style()
        self.style.configure('.',background=_bgcolor, foreground=_fgcolor, font="Arial 12 bold", relief = 'flat', borderwidth = 1)
        self.style.map('.',background=[('selected', _compcolor), ('active',_ana2color)])


        self.Change_Password_Frame = ttk.Frame(self.root, width=500, height=400)#, background="#b3e7f4")
        self.Change_Password_Frame.place(anchor="c", relx=0.5, rely=0.5)

        self.Old_Pass_Label = ttk.Label(self.Change_Password_Frame)#, bg='#b3e7f4')
        self.Old_Pass_Label.place(relx=0.121, rely=0.05, height=27, width=260, bordermode='ignore')
        self.Old_Pass_Label.configure(anchor='w', text='''Altes Passwort:''', font="Arial 16 bold")

        self.Old_Pass_Entry = ttk.Entry(self.Change_Password_Frame, show="*")#,bg='white')
        self.Old_Pass_Entry.place(relx=0.121, rely=0.13, height=40, relwidth=0.764, bordermode='ignore')
        self.Old_Pass_Entry.configure(font="Arial 16 bold")

        self.New_Pass_Label = ttk.Label(self.Change_Password_Frame)#, bg='#b3e7f4')
        self.New_Pass_Label.place(relx=0.121, rely=0.31, height=27, width=260, bordermode='ignore')
        self.New_Pass_Label.configure(anchor='w', text='''Neues Passwort:''', font="Arial 16 bold")

        self.New_Pass_Entry = ttk.Entry(self.Change_Password_Frame, show="*")#,bg='white')
        self.New_Pass_Entry.place(relx=0.121, rely=0.39, height=40, relwidth=0.764, bordermode='ignore')
        self.New_Pass_Entry.configure(font="Arial 16 bold")

        self.Confirm_Pass_Label = ttk.Label(self.Change_Password_Frame)#, bg='#b3e7f4')
        self.Confirm_Pass_Label.place(relx=0.121, rely=0.57, height=27, width=260, bordermode='ignore')
        self.Confirm_Pass_Label.configure(anchor='w', text='''Passwort bestätigen:''', font="Arial 16 bold")

        self.Confirm_Pass_Entry = ttk.Entry(self.Change_Password_Frame, show="*")#,bg='white')
        self.Confirm_Pass_Entry.place(relx=0.121, rely=0.65, height=40, relwidth=0.764, bordermode='ignore')
        self.Confirm_Pass_Entry.configure(font="Arial 16 bold")

        self.Save_Button = ttk.Button(self.Change_Password_Frame, width = 20, text = "Save", command = self.save_password)
        self.Save_Button.place(relx=0.4, rely=0.85, height=51, width=121, bordermode='ignore')
        self.showerror=None

        self.root.mainloop()

    def save_password(self):
        self.salt = bcrypt.gensalt()
        validate_data = ((self.username), (self.Old_Pass_Entry.get()),)
        username = ((self.username),)
        if all(validate_data):
            if (db.validate_user(username, validate_data)):
                if self.New_Pass_Entry.get() == self.Confirm_Pass_Entry.get():
                    self.hashed = bcrypt.hashpw(self.New_Pass_Entry.get().encode(), self.salt)
                    data = (self.hashed, self.username,)
                    db.update_user_password(data)
                    self.root.destroy()
                else:
                    self.showerror = tk.Label(self.root, text="Passwort stimmt nicht überein!", bg="#f6f6f6")
                    self.showerror.place(relx=0.0, rely=0.76, height=25, width=500, bordermode='ignore')
                    self.showerror.configure(anchor='center', font="Arial 12 bold", fg="Red")
            else:
                self.showerror = tk.Label(self.root, text="Altes Passwort ist falsch!", bg="#f6f6f6")
                self.showerror.place(relx=0.0, rely=0.76, height=25, width=500, bordermode='ignore')
                self.showerror.configure(anchor='center', font="Arial 12 bold", fg="Red")

    def user_logout(self):
        import login
        isnotActive=("False", self.username)
        db.set_user_active(isnotActive)
        for item in self.TNotebook1.winfo_children():
            item.destroy()
        self.menubutton.destroy()
        reLogin = login.login()
        reLogin.login_tab(self.TNotebook1)

    def Exit(self):
        isnotActive=("False", self.username)
        msg=tk.messagebox.askyesno("Exit", "Wollen Sie dem Programm beenden?")
        if(msg):
            sys.exit()
