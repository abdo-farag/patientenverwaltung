import sys, bcrypt
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox, END
from database import Database
from datetime import datetime
from tooltip import CreateToolTip
from scrollbar_treeview import ScrolledTreeView
import global_module

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

class manage_users(object):
    def __init__(self, parent):
        self.TNotebook1=parent

        self.TNotebook1_t5 = ttk.Frame(self.TNotebook1, width=300, height=200)
        self.TNotebook1.add(self.TNotebook1_t5, padding=3)
        self.TNotebook1.tab(5, text="Benutzerverwaltung", compound="left", underline="-1")

        self.TreeviewFrame = tk.Frame(self.TNotebook1_t5, width=1900, height=850, background="#f6f6f6")
        self.TreeviewFrame.place(anchor="c", relx=0.5, rely=0.575, relheight=0.85, relwidth=1.0)

        self.Treeview = ScrolledTreeView(self.TreeviewFrame)
        self.Treeview.place(anchor="c", relx=0.5, rely=0.55, relheight=0.9, relwidth=1.0)
        self.Treeview["columns"]=("ID", "Benutzername", "Passwort", "Rolle", "istAktiv")
        self.Treeview['show'] = 'headings'
        self.Treeview.tag_configure('oddrow', background='#b3e7f4')
        self.Treeview.tag_configure('evenrow', background='white')
        self.Treeview.bind("<Double-1>", self.double_click)

        self.Treeview.heading('ID', text='ID', command=lambda: treeview_sort_column(self.Treeview, 'ID', False))
        self.Treeview.column('ID', minwidth=99, stretch='1',anchor='w')

        self.Treeview.heading('Benutzername', text='Benutzername', command=lambda: treeview_sort_column(self.Treeview, 'Benutzername', False))
        self.Treeview.column('Benutzername',minwidth=99,stretch='1',anchor='w')

        self.Treeview.heading('Passwort', text='Passwort', command=lambda: treeview_sort_column(self.Treeview, 'Passwort', False))
        self.Treeview.column('Passwort',minwidth=99,stretch='1',anchor='w')

        self.Treeview.heading('Rolle', text='Rolle', command=lambda: treeview_sort_column(self.Treeview, 'Rolle', False))
        self.Treeview.column('Rolle',minwidth=99,stretch='1',anchor='w')

        self.Treeview.heading('istAktiv', text='Ist Aktiv', command=lambda: treeview_sort_column(self.Treeview, 'Ist Aktiv', False))
        self.Treeview.column('istAktiv',minwidth=99, stretch='1',anchor='w')

        self.RolleList = ["Administrator", "Rezeptionist"]
        self.Boolean = ["True", "False"]

        self.Label0 = ttk.Label(self.TreeviewFrame)
        self.Label0.place(relx=0.0, rely=0.03, height=21, width=260)
        self.Label0.configure(anchor='w', text='''ID:''', font="Arial 12 bold")

        self.ID = ttk.Entry(self.TreeviewFrame)
        self.ID.place(relx=0.0, rely=0.06, relheight=0.035, relwidth=0.185)
        self.ID.configure(background="white", font="Arial 16 bold", justify='left')

        self.Label1 = ttk.Label(self.TreeviewFrame)
        self.Label1.place(relx=0.200, rely=0.03, height=21, width=260)
        self.Label1.configure(anchor='w', text='''Benutzername:''', font="Arial 12 bold")

        self.Benutzername = ttk.Entry(self.TreeviewFrame)
        self.Benutzername.place(relx=0.200, rely=0.06, relheight=0.035, relwidth=0.185)
        self.Benutzername.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label2 = ttk.Label(self.TreeviewFrame)
        self.Label2.place(relx=0.400, rely=0.03, height=21, width=260)
        self.Label2.configure(anchor='w', text='''Passwort:''', font="Arial 12 bold")

        self.Passwort = ttk.Entry(self.TreeviewFrame, show="*")
        self.Passwort.place(relx=0.400, rely=0.06, relheight=0.035, relwidth=0.185)
        self.Passwort.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label3 = ttk.Label(self.TreeviewFrame)
        self.Label3.place(relx=0.600, rely=0.03, height=21, width=260)
        self.Label3.configure(anchor='w',text='''Rolle:''', font="Arial 12 bold")

        self.Rolle_Box = ttk.Combobox(self.TreeviewFrame, values = self.RolleList)
        self.Rolle_Box.place(relx=0.600, rely=0.06, relheight=0.035, relwidth=0.185)
        self.Rolle_Box.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label4 = ttk.Label(self.TreeviewFrame)
        self.Label4.place(relx=0.800, rely=0.03, height=21, width=260)
        self.Label4.configure(anchor='w',text='''Ist_Aktiv:''',font="Arial 12 bold")
        
        self.Ist_Active= ttk.Combobox(self.TreeviewFrame, values=self.Boolean)
        self.Ist_Active.place(relx=0.800, rely=0.06, relheight=0.035, relwidth=0.185)
        self.Ist_Active.configure(background="white", font="Arial 15 bold", justify='left')
    
        # Button widgets
        self.EinfuegenB = ttk.Button(self.TNotebook1_t5, text = "Einfügen", command = self.insert_user)
        self.EinfuegenB.place(relx=0.0, rely=0.02, height=38, width=150)
        self.EinfuegenB_Tip = CreateToolTip(self.EinfuegenB,
                'Die Taste dient zum Hinzufügen eines neuen User.\n'
                'Füllen Sie die folgenden Felder aus und drücken Sie mich.')


        self.LoeschenB = ttk.Button(self.TNotebook1_t5, text = "Löschen", command = self.delete_record)
        self.LoeschenB.place(relx=0.0, rely=0.09, height=38, width=150)
        self.LoeschenB_Tip = CreateToolTip(self.LoeschenB,
                'Die Taste dient zum Löschen ein oder mehr Users.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')

        self.AuswaehlenB = ttk.Button(self.TNotebook1_t5, width = 20, text = "Auswählen", command = self.select_record)
        self.AuswaehlenB.place(relx=0.2, rely=0.02, height=38, width=150)
        self.AuswaehlenB_Tip = CreateToolTip(self.AuswaehlenB,
                'Die Taste dient zum einen Rekord zu auswählen, um zu aktualisieren.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')


        self.AktualisierenB = ttk.Button(self.TNotebook1_t5, width = 20, text = "Aktualisieren", command = self.update_record)
        self.AktualisierenB.place(relx=0.2, rely=0.09, height=38, width=150)
        self.AktualisierenB_Tip = CreateToolTip(self.AktualisierenB,
                'Die Taste dient zum Aktualisieren Users.\n'
                'Nach der Auswahl ein Rekord. Ändern Sie, was Sie wollen, dann drücken Sie mich.')

        refresh=self.display_data()


    def insert_user(self):
        self.salt = bcrypt.gensalt()
        self.hashed = bcrypt.hashpw(self.Passwort.get().encode(), self.salt)
        Ist_Active = "False"
        data =(
                self.Benutzername.get(),
                self.hashed,
                self.Rolle_Box.get(),
                Ist_Active,
                )
        if all(data):
            if Database().search_user((self.Benutzername.get(),)):
                self.valueErrorMessage = "Benutzer "+ self.Benutzername.get() +" existiert bereits"
                messagebox.showerror("Error", self.valueErrorMessage)
            else:
                Database().insert_user(data)
        else:
            self.valueErrorMessage = "Fülle bitte alle Felder aus."
            messagebox.showerror("Error", self.valueErrorMessage)
        refresh=self.display_data()
        self.ID.delete(0, END)
        self.Benutzername.delete(0, END)
        self.Passwort.delete(0, END)
        self.Rolle_Box.delete(0, END)
        self.Ist_Active.delete(0, END)

    def delete_record(self):
        selection = self.Treeview.selection()
        for selected in selection:
            values = self.Treeview.item(selected, 'values')
            data = (values[0],)
            if values[3] == "Administrator**":
                self.valueErrorMessage = "Sie können den ersten Administrator nicht löschen"
                messagebox.showerror("Error", self.valueErrorMessage)
            else:
                Database().delete_user(data)
        refresh=self.display_data()

    def double_click(self, _event=None):
        self.select_record()

    def select_record(self):
        self.ID.delete(0, END)
        self.Benutzername.delete(0, END)
        self.Passwort.delete(0, END)
        self.Rolle_Box.delete(0, END)
        self.Ist_Active.delete(0, END)
        selected= self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')
        if (values):
            self.ID.insert(0, values[0])
            self.Benutzername.insert(0, values[1])
            self.Passwort.insert(0, values[2])
            self.Rolle_Box.insert(0, values[3])
            self.Ist_Active.insert(0, values[4])
        else:
            self.valueErrorMessage = "Bitte, ein Record wählen"
            messagebox.showerror("Value Error", self.valueErrorMessage)

    def update_record(self):
        selected = self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')
        self.salt = global_module.salt
        self.hashed = bcrypt.hashpw(self.Passwort.get().encode(), self.salt)
        if self.Passwort.get() == values[2]:
            password = values[2].split("'")
            password = password[1].encode()
        else:
            self.salt = global_module.salt
            password = bcrypt.hashpw(self.Passwort.get().encode(), self.salt)
        data = (
                self.Benutzername.get(),
                password,
                self.Rolle_Box.get(),
                self.Ist_Active.get(),
                self.Treeview.set(selected, '#1')
                )
        self.Treeview.item(selected, text='', values=(data))
        Database().update_user(data)
        refresh=self.display_data()
        self.ID.delete(0, END)
        self.Benutzername.delete(0, END)
        self.Passwort.delete(0, END)
        self.Rolle_Box.delete(0, END)
        self.Ist_Active.delete(0, END)

    def display_data(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        i=0
        for record in (Database().display_users()):
            i=i+1
            record = list(record)
            record[0] = i
            if (i % 2):
                self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
            else:
                self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

