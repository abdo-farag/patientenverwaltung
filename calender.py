import csv
import calendar, datetime, sys, subprocess
from tkcalendar import Calendar, DateEntry
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox, END
from database import Database
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

class termine(object):
    def __init__(self, parent):
        self.TNotebook1=parent

        self.TNotebook1_t4 = ttk.Frame(self.TNotebook1, width=300, height=200)
        self.TNotebook1.add(self.TNotebook1_t4, padding=3)
        self.TNotebook1.tab(4, text="Termine", compound="left", underline="-1")

        self.TreeviewFrame = tk.Frame(self.TNotebook1_t4, width=1900, height=850, background="#f6f6f6")
        self.TreeviewFrame.place(anchor="c", relx=0.5, rely=0.575, relheight=0.85, relwidth=1.0)

        self.header = ['ID', 'Patient','Tel.Nr.', 'Termine', 'Tag', 'Datum', 'Zweck', 'Notizen']
        self.Treeview = ScrolledTreeView(self.TreeviewFrame)#,  style='Calendar.Treeview')
        self.Treeview.place(anchor="c", relx=0.5, rely=0.55, relheight=0.9, relwidth=1.0)
        self.Treeview["columns"]=tuple(self.header)
        self.Treeview['show'] = 'headings'
        self.Treeview.tag_configure('oddrow', background='gray85')
        self.Treeview.tag_configure('evenrow', background='white')
        self.Treeview.bind("<Double-1>", self.double_click)


        self.Treeview.heading(self.header[0], text=self.header[0], command=lambda: treeview_sort_column(self.Treeview, self.header[0], False))
        self.Treeview.column(self.header[0],minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading(self.header[1], text=self.header[1], command=lambda: treeview_sort_column(self.Treeview, self.header[1], False))
        self.Treeview.column(self.header[1],minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading(self.header[2], text=self.header[2], command=lambda: treeview_sort_column(self.Treeview, self.header[2], False))
        self.Treeview.column(self.header[2],minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading(self.header[3], text=self.header[3], command=lambda: treeview_sort_column(self.Treeview, self.header[3], False))
        self.Treeview.column(self.header[3],minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading(self.header[4], text=self.header[4], command=lambda: treeview_sort_column(self.Treeview, self.header[4], False))
        self.Treeview.column(self.header[4],minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading(self.header[5], text=self.header[5], command=lambda: treeview_sort_column(self.Treeview, self.header[5], False))
        self.Treeview.column(self.header[5],minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading(self.header[6], text=self.header[6], command=lambda: treeview_sort_column(self.Treeview, self.header[6], False))
        self.Treeview.column(self.header[6],minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading(self.header[7], text=self.header[7], command=lambda: treeview_sort_column(self.Treeview, self.header[7], False))
        self.Treeview.column(self.header[7],minwidth='20',stretch='1',anchor='w')

        self.Label0 = ttk.Label(self.TreeviewFrame)
        self.Label0.place(relx=0.0, rely=0.03, height=21, width=260)
        self.Label0.configure(anchor='w', text='''ID:''', font="Arial 12 bold")

        self.ID = ttk.Entry(self.TreeviewFrame)
        self.ID.place(relx=0.0, rely=0.06, relheight=0.035, relwidth=0.120)
        self.ID.configure(background="white", font="Arial 16 bold", justify='left')

        self.Label1 = ttk.Label(self.TreeviewFrame)
        self.Label1.place(relx=0.125, rely=0.03, height=21, width=260)
        self.Label1.configure(anchor='w', text='''Patient:''', font="Arial 12 bold")

        self.Patient = ttk.Entry(self.TreeviewFrame)
        self.Patient.place(relx=0.125, rely=0.06, relheight=0.035, relwidth=0.120)
        self.Patient.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label2 = ttk.Label(self.TreeviewFrame)
        self.Label2.place(relx=0.250, rely=0.03, height=21, width=260)
        self.Label2.configure(anchor='w', text='''Tel_Nr:''', font="Arial 12 bold")

        self.Tel_Nr = ttk.Entry(self.TreeviewFrame)
        self.Tel_Nr.place(relx=0.250, rely=0.06, relheight=0.035, relwidth=0.120)
        self.Tel_Nr.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label3 = ttk.Label(self.TreeviewFrame)
        self.Label3.place(relx=0.375, rely=0.03, height=21, width=260)
        self.Label3.configure(anchor='w',text='''Termin:''', font="Arial 12 bold")


        self.Termin_H = ttk.Spinbox(self.TreeviewFrame,from_=00,to=23,format="%02.0f",wrap=True)
        self.Termin_H.place(relx=0.375, rely=0.06, relheight=0.035, relwidth=0.06)
        self.Termin_H.configure(background="white", font="Arial 15 bold", justify='left')
        self.Termin_M = ttk.Spinbox(self.TreeviewFrame,from_=00,to=59,format="%02.0f",wrap=True)
        self.Termin_M.place(relx=0.435, rely=0.06, relheight=0.035,relwidth=0.06)
        self.Termin_M.configure(background="white", font="Arial 15 bold", justify='left')

        self.Label4 = ttk.Label(self.TreeviewFrame)
        self.Label4.place(relx=0.500, rely=0.03, height=21, width=260)
        self.Label4.configure(anchor='w', text='''Tag:''', font="Arial 12 bold")

        self.Wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        self.Tag = ttk.Combobox(self.TreeviewFrame, values = self.Wochentage)
        self.Tag.place(relx=0.500, rely=0.06, relheight=0.035, relwidth=0.120)
        self.Tag.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label5 = ttk.Label(self.TreeviewFrame)
        self.Label5.place(relx=0.625, rely=0.03, height=21, width=260)
        self.Label5.configure(anchor='w', text='''Datum:''', font="Arial 12 bold")

        self.Datum = DateEntry(self.TreeviewFrame,locale='de_DE', date_pattern='dd.mm.y', width=12, foreground='white', borderwidth=2)
        self.Datum.place(relx=0.625, rely=0.06, relheight=0.035, relwidth=0.120)
        self.Datum.configure(background="green", font="Arial 12 bold", justify='left')

        self.Label6 = ttk.Label(self.TreeviewFrame)
        self.Label6.place(relx=0.750, rely=0.03, height=21, width=260)
        self.Label6.configure(anchor='w', text='''zweck:''', font="Arial 12 bold")

        self.Zweck = ttk.Entry(self.TreeviewFrame)
        self.Zweck.place(relx=0.750, rely=0.06, relheight=0.035, relwidth=0.120)
        self.Zweck.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label7 = ttk.Label(self.TreeviewFrame)
        self.Label7.place(relx=0.875, rely=0.03, height=21, width=260)
        self.Label7.configure(anchor='w', text='''Notizen:''', font="Arial 12 bold")

        self.Notizen = ttk.Entry(self.TreeviewFrame)
        self.Notizen.place(relx=0.875, rely=0.06, relheight=0.035, relwidth=0.120)
        self.Notizen.configure(background="white", font="Arial 12 bold", justify='left')


        # Button widgets
        self.EinfuegenB = ttk.Button(self.TNotebook1_t4, text = "Einfügen", command = self.insert_data)
        self.EinfuegenB.place(relx=0.0, rely=0.02, height=38, width=150)
        self.EinfuegenB_Tip = CreateToolTip(self.EinfuegenB,
                'Die Taste dient zum Hinzufügen eines neuen Termin.\n'
                'Füllen Sie die folgenden Felder aus und drücken Sie mich.')


        self.LoeschenB = ttk.Button(self.TNotebook1_t4, text = "Löschen", command = self.delete_record)
        self.LoeschenB.place(relx=0.0, rely=0.09, height=38, width=150)
        self.LoeschenB_Tip = CreateToolTip(self.LoeschenB,
                'Die Taste dient zum Löschen ein oder mehr Termine.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')

        self.AuswaehlenB = ttk.Button(self.TNotebook1_t4, width = 20, text = "Auswählen", command = self.select_record)
        self.AuswaehlenB.place(relx=0.2, rely=0.02, height=38, width=150)
        self.AuswaehlenB_Tip = CreateToolTip(self.AuswaehlenB,
                'Die Taste dient zum einen Rekord zu auswählen, um zu aktualisieren.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')


        self.AktualisierenB = ttk.Button(self.TNotebook1_t4, width = 20, text = "Aktualisieren", command = self.update_record)
        self.AktualisierenB.place(relx=0.2, rely=0.09, height=38, width=150)
        self.AktualisierenB_Tip = CreateToolTip(self.AktualisierenB,
                'Die Taste dient zum Aktualisieren Termin.\n'
                'Nach der Auswahl eines Termin. Ändern Sie, was Sie wollen, dann drücken Sie mich.')


        self.SuchenB = ttk.Button(self.TNotebook1_t4, width = 20, text = "Suchen", command = self.search_record)
        self.SuchenB.place(relx=0.4, rely=0.02, height=38, width=150)
        self.SuchenB_Tip = CreateToolTip(self.SuchenB,
                'Die Taste dient zum Suchen eines Patient, oder Daten Aktualisieren.\n'
                'Sie können mit ein oder mehr Eingaben Suchen. Füllen Sie die Eingebe bzw Eingaben, dann drücken Sie mich.')

        self.RefreshB = ttk.Button(self.TNotebook1_t4, width = 20, text = "Refresh", command = self.display_data)
        self.RefreshB.place(relx=0.4, rely=0.09, height=38, width=150)
        self.RefreshB_Tip = CreateToolTip(self.RefreshB,
                'Die Taste dient zur Suche abbrechen.\n'
                'Nach Ihre Suche drücken Sie mich.')

        self.ExportierenB = ttk.Button(self.TNotebook1_t4, width = 20, text = "Daten Exportieren", command = self.write_to_csv)
        self.ExportierenB.place(relx=0.6, rely=0.02, height=38, width=150)
        self.ExportierenB_Tip = CreateToolTip(self.ExportierenB,
                'Die Taste dient zum Exportieren Daten (Backup).')

        self.ImportierenB = ttk.Button(self.TNotebook1_t4, width = 20,text='Daten Importieren', command=self.load_from_csv)
        self.ImportierenB.place(relx=0.6, rely=0.09, height=38, width=150)
        self.ImportierenB_Tip = CreateToolTip(self.ImportierenB,
                'Die Taste dient zum Importieren Daten (Recovery).')

        self.ResetB = ttk.Button(self.TNotebook1_t4, width = 20, text = "Reset!", command = self.delete_all)
        self.ResetB.place(relx=0.8, rely=0.045, height=38, width=150)
        self.ResetB_Tip = CreateToolTip(self.ResetB,
                'Die Taste dient zum Löchen Alle Daten .')
        refresh=self.display_data()

    def update_date_time(self):
        today = datetime.date.today()
        self.tag_name = calendar.day_name[today.weekday()]
        self.Tag.insert(0, self.tag_name)

        self.Now = datetime.datetime.now()
        self.hour = self.Now.strftime("%H")
        self.minute = self.Now.strftime("%M")
        self.Termin_H.insert(0, self.hour)
        self.Termin_M.insert(0, self.minute)


    def insert_data(self):
        Name = self.Patient.get().split(" ")
        data = (
                Name[0].capitalize()+' '+Name[1].capitalize(),
                self.Tel_Nr.get(),
                self.Termin_H.get()+':'+self.Termin_M.get(),
                self.Tag.get(),
                self.Datum.get(),
                self.Zweck.get(),
                self.Notizen.get(),
                )
        Database().insert_termin(data)
        self.display_data()
        self.Patient.delete(0, END)
        self.Tel_Nr.delete(0, END)
        self.Termin_H.delete(0, END)
        self.Termin_M.delete(0, END)
        #self.Tag.delete(0, END)
        #self.Datum.delete(0, END)
        self.Zweck.delete(0, END)
        self.Notizen.delete(0, END)

    def delete_record(self):
        selection = self.Treeview.selection()
        for selected in selection:
            values = self.Treeview.item(selected, 'values')
            data = (values[0],)
            Database().delete_termin(data)
        refresh=self.display_data()

    def double_click(self, _event=None):
        self.select_record()

    def select_record(self):
        self.ID.delete(0, END)
        self.Patient.delete(0, END)
        self.Tel_Nr.delete(0, END)
        self.Termin_H.delete(0, END)
        self.Termin_M.delete(0, END)
        self.Tag.delete(0, END)
        self.Datum.delete(0, END)
        self.Zweck.delete(0, END)
        self.Notizen.delete(0, END)
        selected= self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')
        Termin = values[3].split(":")
        if (values):
            self.ID.insert(0, values[0])
            self.Patient.insert(0, values[1])
            self.Tel_Nr.insert(0, values[2])
            self.Termin_H.insert(0, Termin[0])
            self.Termin_M.insert(0, Termin[1])
            self.Tag.insert(0, values[4])
            self.Datum.insert(0, values[5])
            self.Zweck.insert(0, values[6])
            self.Notizen.insert(0, values[7])
        else:
            self.valueErrorMessage = "Bitte, ein Record wählen"
            messagebox.showerror("Value Error", self.valueErrorMessage)

    def update_record(self):
        selected = self.Treeview.focus()
        if (selected):
            data = (
                    self.Patient.get(),
                    self.Tel_Nr.get(),
                    self.Termin_H.get()+':'+self.Termin_M.get(),
                    self.Tag.get(),
                    self.Datum.get(),
                    self.Zweck.get(),
                    self.Notizen.get(),
                    self.Treeview.set(selected, '#1')
                    )
            self.Treeview.item(selected, text='', values=(data))
            Database().update_termin(data)
            refresh=self.display_data()

        else:
            self.valueErrorMessage = "Invalid input in field " + self.test
            self.messagebox = messagebox.showerror("Value Error", self.valueErrorMessage)
        self.ID.delete(0, END)
        self.Patient.delete(0, END)
        self.Tel_Nr.delete(0, END)
        self.Termin_H.delete(0, END)
        self.Termin_M.delete(0, END)
        #self.Tag.delete(0, END)
        #self.Datum.delete(0, END)
        self.Zweck.delete(0, END)
        self.Notizen.delete(0, END)


    def search_record(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        Name = self.Patient.get().split(" ")
        if (Name):
            Name=Name[0].capitalize()+' '+Name[1].capitalize(),
        data = (
                self.ID.get(),
                Name[0].capitalize()+' '+Name[1].capitalize(),
                self.Tel_Nr.get(),
                self.Termin_H.get()+':'+self.Termin_M.get(),
                self.Tag.get(),
                self.Datum.get(),
                self.Zweck.get(),
                self.Notizen.get(),
                )
        i = 0
        for record in (Database().search_termin(data)):
            i=i+1
            if (i % 2):
                self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
            else:
                self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

        self.ID.delete(0, END)
        self.Patient.delete(0, END)
        self.Tel_Nr.delete(0, END)
        self.Termin_H.delete(0, END)
        self.Termin_M.delete(0, END)
        #self.Tag.delete(0, END)
        #self.Datum.delete(0, END)
        self.Zweck.delete(0, END)
        self.Notizen.delete(0, END)

    def display_data(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        i=0
        for record in (Database().display_termine()):
            i=i+1
            if (i % 2):
                self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
            else:
                self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))
        self.ID.delete(0, END)
        self.Patient.delete(0, END)
        self.Tel_Nr.delete(0, END)
        self.Termin_H.delete(0, END)
        self.Termin_M.delete(0, END)
        self.Tag.delete(0, END)
        self.Datum.delete(0, END)
        self.Zweck.delete(0, END)
        self.Notizen.delete(0, END)
        self.update_date_time()

    def write_to_csv(self):
        header=['ID', 'Patient', 'Tel_Nr', 'Termin','Tag', 'Datum', 'Zweck', 'Notizen']
        fname = asksaveasfilename(parent=self.TNotebook1, initialdir = global_module.default_path, title = "Select file", filetypes=(
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")),
            confirmoverwrite=True, defaultextension=".csv" ) #,initialdir = (str(Path.home())) )
        if (fname):
            with open(fname, 'a', newline='') as termine:
                self.write = csv.writer(termine, dialect='excel')
                for record in (Database().display_termine()):
                    self.write.writerow(record)

    def load_from_csv(self):
        import time
        Database().createTable()
        name = askopenfilename(parent=self.TNotebook1, initialdir = global_module.default_path, title = "Import File", filetypes=(
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")),
            defaultextension=".csv" ) #,initialdir = (str(Path.home())) )
        if name:
            with open(name, 'r', encoding='utf-8') as termine:
                self.reader = csv.reader(termine, dialect='excel')
                self.row = sum(1 for row in self.reader)
                self.progress = ttk.Progressbar(self.TNotebook1_t4, orient = HORIZONTAL, length=150, value=0, mode = 'determinate')
                self.progress.grid(padx=(1148, 130), pady=(130, 1148))
                self.progress['maximum'] = self.row
            with open(name, 'r', encoding='utf-8') as termine:
                bar = 0
                self.reader = csv.reader(termine, dialect='excel')
                for line in self.reader:
                    bar = bar + 1
                    #data = tuple(line.rstrip('\n').split(","))
                    data = tuple(line)
                    if not all(data):
                        pass
                    else:
                        data = (
                                data[0],
                                data[1],
                                data[2],
                                data[3],
                                data[4],
                                data[5],
                                data[6],
                                data[7],
                                )
                        lst = list(data)
                        if len(lst) == 0:
                            pass
                        else:
                            lst[0]=''
                            if (Database().search_termin(lst)):
                                pass
                            else:
                                del lst[0]
                                Database().insert_termin(lst)
                                self.progress["value"] = bar
                                self.progress.update()
                                self.display_data()
                self.progress.grid_forget()

    def delete_all(self):
        msg = messagebox.askyesno("Reset", "Sind Sie sicher, Sie werden alles löchen?!!!")
        if(msg):
            error =  messagebox.showerror("Error", "Are you Sure You want to Delete Everything!!!!")
            if(error):
                msg =  messagebox.askyesno("Error", "Es gibt keine Möglichkeit diese Daten nochmal von Datenbanken zu konstruieren.")
                if(msg):
                    Database().delete_termine_table()
                    refresh=self.display_data()

