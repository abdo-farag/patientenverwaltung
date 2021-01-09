#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import locale
from tkinter import *
from ttkthemes import ThemedStyle
import root_support
import global_module
from database import Database
from toast import *

db = Database()
db.createTable()
if (db.get_last_nummer_rechnung()):
    global_module.rech_nummer = int(db.get_last_nummer_rechnung()[0][0])
notification_manager = Notification_Manager(background="white")

from login import *

if sys.platform == "win32":
    locale.setlocale(locale.LC_ALL, 'german')
else:
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

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
    

def root_start_gui():
    '''Starting point when module is the main routine.'''
    from image_base64 import app_icon
    global val, w, root
    root = tk.Tk(className='Patientenverwaltung')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    style = ThemedStyle(root)
    if sys.platform == "win32":
        root.state('zoomed')
        root.resizable(1, 1)
        root.minsize(1024, 768)
    else:
        style.set_theme("plastik")
        root.attributes ("-alpha", "0.5")
        root.attributes('-zoomed', True)
        root.resizable(1, 1)
        root.minsize(1024, 768)
    top = Root(root)
    root_support.init(root, top)
    root.title("Patientenverwaltung")
    icon = PhotoImage(data = app_icon)
    root.iconphoto(False, icon)
    root.update()

def mahnung():
    if (db.get_last_nummer_rechnung()):
        if int(db.get_last_nummer_rechnung()[0][0]) > global_module.rech_nummer:
            notification_manager.success("Neue Rechnung ist im System verfügbar!", "Arial 14", 50, 'center', None, None, 500, 5000, None, None)
            global_module.rech_nummer = int(db.get_last_nummer_rechnung()[0][0])
        root.after(2000, mahnung)

w = None
def create_login(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Root(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Root(w)
    root_support.init(w, top, *args, **kwargs)
    return (w, top)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        username=global_module.active_user
        isnotActive=("False", username)
        db.set_user_active(isnotActive)
        root.destroy()

def destroy_login():
    global w
    w.destroy()
    w = None

_bgcolor = '#f6f6f6'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#5dbf33' # X11 color: 'gray85'
_ana1color = '#f6f6f6' # X11 color: 'gray85'
_ana2color = '#f6f6f6' # Closest X11 color: 'gray92'


class Root:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        self.style = ttk.Style()
        self.style.configure('.',background=_bgcolor, foreground=_fgcolor, font="Arial 11 bold", relief = 'flat', borderwidth = 1)
        self.style.map('.',background=[('selected', _compcolor), ('active',_ana2color)])


        self.style.configure('User.TNotebook',tabposition='n')

        self.style.configure('TNotebook.Heading', background=_bgcolor, foreground=_fgcolor, font="Arial 14 bold")
        self.style.map('TNotebook.Heading', background=[('selected', _compcolor), ('active',_ana2color)])

        self.style.configure('TNotebook.Tab', background=_bgcolor, foreground=_fgcolor, font="Arial 14 bold",padding=[20, 5], tabposition='n')
        self.style.map('TNotebook.Tab', background=[('selected', _compcolor), ('active',_ana2color)])

        self.style.configure("Treeview.Heading",font="Arial 14 bold", background="white", foreground="black" ,rowheight=35)
        self.style.map('Treeview.Heading', background=[('selected', _compcolor), ('active',_ana2color)])

        self.style.configure('Treeview', font="Arial 14", background="white", foreground="black" ,rowheight=35, relief = 'flat', borderwidth = 1)
        self.style.map('Treeview', background=[('selected', "#FFA600"), ('active', "FFA600")], foreground=[("selected", "Black")])

        #self.style.configure('Treeview', font="Arial 14", background="white", foreground="black" ,rowheight=35)
        #self.style.map('Treeview', background=[('selected', _compcolor), ('active',_ana2color)], foreground=[("selected", _fgcolor)])

        self.style.configure('Frame', font="Arial 14", background="white", foreground="black")
        self.style.map('Frame', background=[('selected', _compcolor), ('active',_ana2color)], foreground=[("selected", _fgcolor)])


        self.TNotebook1 = ttk.Notebook(top)
        self.TNotebook1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.TNotebook1.configure(takefocus="", width=300)


        login(self.TNotebook1)

if __name__ == '__main__':
    try:
        root_start_gui()
        mahnung()
        root.mainloop()
    except KeyboardInterrupt:
        username=global_module.active_user
        isnotActive=("False", username)
        db.set_user_active(isnotActive)
        root.destroy()
        sys.exit(0)


