import sys
import locale
import csv
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox, END
from database import Database
from datetime import datetime
from tooltip import CreateToolTip
from scrollbar_treeview import ScrolledTreeView
import global_module

key = ("default_path",)
if (Database().get_setting(key)):
    default_path = Database().get_setting(key)[0][2]+'/'
else:
    default_path = global_module.default_path


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

class patienten(object):
    def __init__(self, parent):

        self.TNotebook1=parent

        self.TNotebook1_t1 = ttk.Frame(self.TNotebook1, width=300, height=200)
        self.TNotebook1.add(self.TNotebook1_t1, padding=3)
        self.TNotebook1.tab(1, text="Patienten", compound="left", underline="-1")

        self.TreeviewFrame = tk.Frame(self.TNotebook1_t1, width=1900, height=850, background="#f6f6f6")
        self.TreeviewFrame.place(anchor="c", relx=0.5, rely=0.575, relheight=0.85, relwidth=1.0)

        self.Treeview = ScrolledTreeView(self.TreeviewFrame)
        self.Treeview.place(anchor="c", relx=0.5, rely=0.55, relheight=0.9, relwidth=1.0)
        self.Treeview["columns"]=("ID", "Vorname", "Nachname", "Geschlecht", "Geburtdatum", "Adresse", "Krankenversicherung")
        self.Treeview['show'] = 'headings'
        self.Treeview.tag_configure('oddrow', background='#b3e7f4')
        self.Treeview.tag_configure('evenrow', background='white')
        self.Treeview.bind("<Double-1>", self.double_click)

        self.Treeview.heading('ID', text='ID', command=lambda: treeview_sort_column(self.Treeview, 'ID', False))
        self.Treeview.column('ID',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Vorname', text='Vorname', command=lambda: treeview_sort_column(self.Treeview, 'Vorname', False))
        self.Treeview.column('Vorname',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Nachname', text='Nachname', command=lambda: treeview_sort_column(self.Treeview, 'Nachname', False))
        self.Treeview.column('Nachname',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Geschlecht', text='Geschlecht', command=lambda: treeview_sort_column(self.Treeview, 'Geschlecht', False))
        self.Treeview.column('Geschlecht',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Geburtdatum', text='Geburtdatum', command=lambda: treeview_sort_column(self.Treeview, 'Geburtdatum', False))
        self.Treeview.column('Geburtdatum',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Adresse', text='Adresse', command=lambda: treeview_sort_column(self.Treeview, 'Adresse', False))
        self.Treeview.column('Adresse',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Krankenversicherung', text='Krankenversicherung', command=lambda: \
                treeview_sort_column(self.Treeview, 'Krankenversicherung', False))
        self.Treeview.column('Krankenversicherung',minwidth='20',stretch='1',anchor='w')

        self.GeschlechtList = ["Weiblich", "Männlich"]
        self.KrankenversicherungList = ["Privat", "Pflichtversichert"]
        self.TagList = ["%02d" % x for x in range(1, 32)]

        self.MonatList = [
                'Januar',
                'Februar',
                'März',
                'April',
                'Mai',
                'Juni',
                'Juli',
                'August',
                'September',
                'Oktober',
                'November',
                'Dezember',
                ]
        self.JahrList = list(range(2021, 1899, -1))

        self.Label0 = ttk.Label(self.TreeviewFrame)
        self.Label0.place(relx=0.0, rely=0.03, height=21, width=260)
        self.Label0.configure(anchor='w', text='''ID:''', font="Arial 12 bold")

        self.ID = ttk.Entry(self.TreeviewFrame)
        self.ID.place(relx=0.0, rely=0.06, relheight=0.035, relwidth=0.138)
        self.ID.configure(background="white", font="Arial 16 bold", justify='left')

        self.Label1 = ttk.Label(self.TreeviewFrame)
        self.Label1.place(relx=0.141, rely=0.03, height=21, width=260)
        self.Label1.configure(anchor='w', text='''Vorname:''', font="Arial 12 bold")

        self.Vorname = ttk.Entry(self.TreeviewFrame)
        self.Vorname.place(relx=0.141, rely=0.06, relheight=0.035, relwidth=0.138)
        self.Vorname.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label2 = ttk.Label(self.TreeviewFrame)
        self.Label2.place(relx=0.283, rely=0.03, height=21, width=260)
        self.Label2.configure(anchor='w', text='''Nachname:''', font="Arial 12 bold")

        self.Nachname = ttk.Entry(self.TreeviewFrame)
        self.Nachname.place(relx=0.283, rely=0.06, relheight=0.035, relwidth=0.138)
        self.Nachname.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label3 = ttk.Label(self.TreeviewFrame)
        self.Label3.place(relx=0.425, rely=0.03, height=21, width=260)
        self.Label3.configure(anchor='w',text='''Geschlecht:''', font="Arial 12 bold")

        self.Geschlecht_Box = ttk.Combobox(self.TreeviewFrame, values = self.GeschlechtList)
        self.Geschlecht_Box.place(relx=0.425, rely=0.06, relheight=0.035, relwidth=0.138)
        self.Geschlecht_Box.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label4 = ttk.Label(self.TreeviewFrame)
        self.Label4.place(relx=0.567, rely=0.03, height=21, width=260)
        self.Label4.configure(anchor='w',text='''Geburtdatum: T.M.Y''',font="Arial 12 bold")

        self.Geb_T_Box = ttk.Combobox(self.TreeviewFrame, values = self.TagList)
        self.Geb_M_Box = ttk.Combobox(self.TreeviewFrame, values = self.MonatList)
        self.Geb_Y_Box = ttk.Combobox(self.TreeviewFrame, values = self.JahrList)

        self.Geb_T_Box.place(relx=0.567, rely=0.06, relheight=0.035, relwidth=0.03)
        self.Geb_T_Box.configure(background="white", font="Arial 12 bold", justify='left')
        self.Geb_M_Box.place(relx=0.5975, rely=0.06, relheight=0.035, relwidth=0.065)
        self.Geb_M_Box.configure(background="white", font="Arial 12 bold", justify='left')
        self.Geb_Y_Box.place(relx=0.663, rely=0.06, relheight=0.035, relwidth=0.04)
        self.Geb_Y_Box.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label5 = ttk.Label(self.TreeviewFrame)
        self.Label5.place(relx=0.7075, rely=0.03, height=21, width=260)
        self.Label5.configure(anchor='w',text='''Adresse:''', font="Arial 12 bold")

        self.Adresse = ttk.Entry(self.TreeviewFrame)
        self.Adresse.place(relx=0.7075, rely=0.06, relheight=0.035, relwidth=0.138)
        self.Adresse.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label6 = ttk.Label(self.TreeviewFrame)
        self.Label6.place(relx=0.849, rely=0.03, height=21, width=260)
        self.Label6.configure(anchor='w',text='''Krankenversicherung:''', font="Arial 12 bold")

        self.Krankenversicherung_Box = ttk.Combobox(self.TreeviewFrame, values = self.KrankenversicherungList)
        self.Krankenversicherung_Box.place(relx=0.849, rely=0.06, relheight=0.035, relwidth=0.138)
        self.Krankenversicherung_Box.configure(background="white", font="Arial 12 bold", justify='left')
    
        # Button widgets
        self.EinfuegenB = ttk.Button(self.TNotebook1_t1, text = "Einfügen", command = self.insert_patient)
        self.EinfuegenB.place(relx=0.0, rely=0.02, height=38, width=150)
        self.EinfuegenB_Tip = CreateToolTip(self.EinfuegenB,
                'Die Taste dient zum Hinzufügen eines neuen Patient.\n'
                'Füllen Sie die folgenden Felder aus und drücken Sie mich.')


        self.LoeschenB = ttk.Button(self.TNotebook1_t1, text = "Löschen", command = self.delete_record)
        self.LoeschenB.place(relx=0.0, rely=0.09, height=38, width=150)
        self.LoeschenB_Tip = CreateToolTip(self.LoeschenB,
                'Die Taste dient zum Löschen ein oder mehr Patienten.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')

        self.AuswaehlenB = ttk.Button(self.TNotebook1_t1, width = 20, text = "Auswählen", command = self.select_record)
        self.AuswaehlenB.place(relx=0.2, rely=0.02, height=38, width=150)
        self.AuswaehlenB_Tip = CreateToolTip(self.AuswaehlenB,
                'Die Taste dient zum einen Rekord zu auswählen(Doppelklick), um zu aktualisieren.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')


        self.AktualisierenB = ttk.Button(self.TNotebook1_t1, width = 20, text = "Aktualisieren", command = self.update_record)
        self.AktualisierenB.place(relx=0.2, rely=0.09, height=38, width=150)
        self.AktualisierenB_Tip = CreateToolTip(self.AktualisierenB,
                'Die Taste dient zum Aktualisieren Patientdaten.\n'
                'Nach der Auswahl eines Patienten. Ändern Sie, was Sie wollen, dann drücken Sie mich.')


        self.SuchenB = ttk.Button(self.TNotebook1_t1, width = 20, text = "Suchen", command = self.search_record)
        self.SuchenB.place(relx=0.4, rely=0.02, height=38, width=150)
        self.SuchenB_Tip = CreateToolTip(self.SuchenB,
                'Die Taste dient zum Suchen eines Patient.\n'
                'Sie können mit ein oder mehr Eingaben Suchen. Füllen Sie die Eingebe bzw. Eingaben, dann drücken Sie mich.')

        self.RefreshB = ttk.Button(self.TNotebook1_t1, width = 20, text = "Refresh", command = self.display_data)
        self.RefreshB.place(relx=0.4, rely=0.09, height=38, width=150)
        self.RefreshB_Tip = CreateToolTip(self.RefreshB,
                'Die Taste dient zur Suche abbrechen, oder Daten Aktualisieren.\n'
                'Nach Ihre Suche drücken Sie mich.')

        self.ExportierenB = ttk.Button(self.TNotebook1_t1, width = 20, text = "Daten Exportieren", command = self.write_to_csv)
        self.ExportierenB.place(relx=0.6, rely=0.02, height=38, width=150)
        self.ExportierenB_Tip = CreateToolTip(self.ExportierenB,
                'Die Taste dient zum Exportieren Daten (Backup).')

        self.ImportierenB = ttk.Button(self.TNotebook1_t1, width = 20,text='Daten Importieren', command=self.load_from_csv)
        self.ImportierenB.place(relx=0.6, rely=0.09, height=38, width=150)
        self.ImportierenB_Tip = CreateToolTip(self.ImportierenB,
                'Die Taste dient zum Importieren Daten (Recovery).')

        self.ResetB = ttk.Button(self.TNotebook1_t1, width = 20, text = "Reset!", command = self.delete_all)
        self.ResetB.place(relx=0.8, rely=0.045, height=38, width=150)
        self.ResetB_Tip = CreateToolTip(self.ResetB,
                'Die Taste dient zum Löchen Alle Daten .')

        refresh=self.display_data()


    def Validate(self, Vorname, Nachname, Geschlecht, Geb_T_Box, Geb_M_Box, Geb_Y_Box, Adresse,Krankenversicherung):
        if not (Vorname.isalpha()):
            return "Vorname"
        elif not (Nachname.isalpha()):
            return "Nachname"
        elif not (Geschlecht.isalpha()):
            return "Geschlecht"
        elif not (Geb_T_Box.isdigit()) or len(Geb_T_Box) > 2 or int(Geb_T_Box) >= 32:
            return "Geb_T_Box"
        elif not (Geb_M_Box.isalpha()) or len(Geb_M_Box) > 9:
            return "Geb_M_Box"
        elif not (Geb_Y_Box.isdigit()) or len(Geb_Y_Box) > 4:
            return "Geb_Y_Box"
        elif not "," not in Adresse:
            return "Adresse"
        elif not (Krankenversicherung.isalpha()):
            return "Krankenversicherung"
        else:
            return "SUCCESS"

    def insert_patient(self):
        validata_data = self.Validate(
                self.Vorname.get(),
                self.Nachname.get(),
                self.Geschlecht_Box.get(),
                self.Geb_T_Box.get(),
                self.Geb_M_Box.get(),
                self.Geb_Y_Box.get(),
                self.Adresse.get(),
                self.Krankenversicherung_Box.get(),
                )
        if (validata_data == "SUCCESS"):
            self.Geb_T=str(self.Geb_T_Box.get())
            self.Geb_M=str(self.Geb_M_Box.get())
            self.Geb_Y=str(self.Geb_Y_Box.get())
            self.Geb_Datum=str(self.Geb_T + "." + self.Geb_M + "." + self.Geb_Y)
            data = (
                    self.Vorname.get(),
                    self.Nachname.get(),
                    self.Geschlecht_Box.get(),
                    self.Geb_Datum,
                    self.Adresse.get(),
                    self.Krankenversicherung_Box.get(),
                    )
            Database().insert_patient(data)
            refresh=self.display_data()
        else:
            self.valueErrorMessage = "Invalid input in field " + validata_data
            messagebox.showerror("Value Error", self.valueErrorMessage)
        self.ID.delete(0, END)
        self.Vorname.delete(0, END)
        self.Nachname.delete(0, END)
        self.Geschlecht_Box.delete(0, END)
        self.Geb_T_Box.delete(0, END)
        self.Geb_M_Box.delete(0, END)
        self.Geb_Y_Box.delete(0, END)
        self.Adresse.delete(0, END)
        self.Krankenversicherung_Box.delete(0, END)

    def delete_record(self):
        selection = self.Treeview.selection()
        for selected in selection:
            values = self.Treeview.item(selected, 'values')
            data = (values[0],)
            Database().delete_patient(data)
        refresh=self.display_data()

    def double_click(self, _event=None):
        self.select_record()

    def Convert(self, string):
        lst = list(string.split(" "))
        return lst

    def select_record(self):
        self.ID.delete(0, END)
        self.Vorname.delete(0, END)
        self.Nachname.delete(0, END)
        self.Geschlecht_Box.delete(0, END)
        self.Geb_T_Box.delete(0, END)
        self.Geb_M_Box.delete(0, END)
        self.Geb_Y_Box.delete(0, END)
        self.Adresse.delete(0, END)
        self.Krankenversicherung_Box.delete(0, END)
        selected= self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')

        if (values):
            Geb_Datum = datetime.strptime(values[4], "%d.%B.%Y")
            Geb_Datum = Geb_Datum.strftime('%d %B %Y')
            Geb_Datum = self.Convert(Geb_Datum)

            self.ID.insert(0, values[0])
            self.Vorname.insert(0, values[1])
            self.Nachname.insert(0, values[2])
            self.Geschlecht_Box.insert(0, values[3])
            self.Geb_T_Box.insert(0, Geb_Datum[0])
            self.Geb_M_Box.insert(0, Geb_Datum[1])
            self.Geb_Y_Box.insert(0, Geb_Datum[2])
            self.Adresse.insert(0, values[5])
            self.Krankenversicherung_Box.insert(0, values[6])
        else:
            self.valueErrorMessage = "Bitte, ein Record wählen"
            messagebox.showerror("Value Error", self.valueErrorMessage)

    def update_record(self):
        selected = self.Treeview.focus()
        validata_data = self.Validate(
                self.Vorname.get(),
                self.Nachname.get(),
                self.Geschlecht_Box.get(),
                self.Geb_T_Box.get(),
                self.Geb_M_Box.get(),
                self.Geb_Y_Box.get(),
                self.Adresse.get(),
                self.Krankenversicherung_Box.get(),
                )
        if (validata_data == "SUCCESS"):
            self.Geb_T=str(self.Geb_T_Box.get())
            self.Geb_M=str(self.Geb_M_Box.get())
            self.Geb_Y=str(self.Geb_Y_Box.get())
            self.Geb_Datum=self.Geb_T + "." + self.Geb_M + "." + self.Geb_Y
            data = (
                    self.Vorname.get(),
                    self.Nachname.get(),
                    self.Geschlecht_Box.get(),
                    self.Geb_Datum,
                    self.Adresse.get(),
                    self.Krankenversicherung_Box.get(),
                    self.Treeview.set(selected, '#1')
                    )
            self.Treeview.item(selected, text='', values=(data))
            Database().update_patient(data)
            refresh=self.display_data()

        else:
            self.valueErrorMessage = "Invalid input in field " + validata_data
            self.messagebox = messagebox.showerror("Value Error", self.valueErrorMessage)
        self.ID.delete(0, END)
        self.Vorname.delete(0, END)
        self.Nachname.delete(0, END)
        self.Geschlecht_Box.delete(0, END)
        self.Geb_T_Box.delete(0, END)
        self.Geb_M_Box.delete(0, END)
        self.Geb_Y_Box.delete(0, END)
        self.Adresse.delete(0, END)
        self.Krankenversicherung_Box.delete(0, END)


    def search_record(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        self.Geb_T=str(self.Geb_T_Box.get())
        self.Geb_M=str(self.Geb_M_Box.get())
        self.Geb_Y=str(self.Geb_Y_Box.get())
        self.Geb_Datum=str(self.Geb_T + "." + self.Geb_M + "." + self.Geb_Y)
        data = (
                self.ID.get(),
                self.Vorname.get().capitalize(),
                self.Nachname.get().capitalize(),
                self.Geschlecht_Box.get(),
                self.Geb_Datum,
                self.Adresse.get(),
                self.Krankenversicherung_Box.get(),
                )
        lst = list(data)
        if '..' in lst :
            lst[4]= ''
        empty = list(filter(None, lst))
        if len(empty) == 0:
           refresh=self.display_data()
        else:
            i = 0
            for record in (Database().search_patient(lst)):
                i=i+1
                if (i % 2):
                    self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
                else:
                    self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

        self.ID.delete(0, END)
        self.Vorname.delete(0, END)
        self.Nachname.delete(0, END)
        self.Geschlecht_Box.delete(0, END)
        self.Geb_T_Box.delete(0, END)
        self.Geb_M_Box.delete(0, END)
        self.Geb_Y_Box.delete(0, END)
        self.Adresse.delete(0, END)
        self.Krankenversicherung_Box.delete(0, END)

    def display_data(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        i=0
        for record in (Database().display_patienten()):
            i=i+1
            if (i % 2):
                self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
            else:
                self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

    def write_to_csv(self):
        header=['ID', 'Vorname', 'Nachname', 'Geschlecht','Geburtdatum', 'Adresse', 'Krankenversicherung']
        fname = asksaveasfilename(parent=self.TNotebook1, initialdir=default_path, title = "Select file", filetypes=(
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")), 
            confirmoverwrite=True, defaultextension=".csv" )
        if (fname):
            with open(fname, 'a', newline='') as patienten:
                self.write = csv.writer(patienten, dialect='excel')
                #self.write.writerow(header)
                for record in (Database().display_patienten()):
                    self.write.writerow(record)

    def load_from_csv(self):
        import time
        Database().createTable()
        name = askopenfilename(parent=self.TNotebook1, initialdir=default_path, title = "Import File", filetypes=(
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")),
            defaultextension=".csv" ) #,initialdir = (str(Path.home())) )
        if name:
            with open(name, 'r', encoding='utf-8') as patienten:
                self.reader = csv.reader(patienten, dialect='excel')
                self.row = sum(1 for row in self.reader)
                self.progress = ttk.Progressbar(self.TNotebook1_t1, orient = HORIZONTAL, length=150, value=0, mode = 'determinate')
                self.progress.grid(padx=(1148, 130), pady=(130, 1148))
                self.progress['maximum'] = self.row
            with open(name, 'r', encoding='utf-8') as patienten:
                bar = 0
                self.reader = csv.reader(patienten, dialect='excel')
                for line in self.reader:
                    bar = bar + 1
                    #data = tuple(line.rstrip('\n').split(","))
                    data = tuple(line)
                    if not all(data):
                        pass
                    else:
                        Geb_Datum = datetime.strptime(data[4], "%d.%B.%Y")
                        Geb_Datum = Geb_Datum.strftime('%d %B %Y')
                        Geb_Datum = self.Convert(Geb_Datum)
                        validata_data = self.Validate(
                                data[1],
                                data[2],
                                data[3],
                                Geb_Datum[0],
                                Geb_Datum[1],
                                Geb_Datum[2],
                                data[5],
                                data[6],
                        )
                        if (validata_data == "SUCCESS"):
                            self.Geb_T=str(Geb_Datum[0])
                            self.Geb_M=str(Geb_Datum[1])
                            self.Geb_Y=str(Geb_Datum[2])
                            self.Geb_Datum=self.Geb_T + "." + self.Geb_M + "." + self.Geb_Y
                            data = (
                                    data[0],
                                    data[1],
                                    data[2],
                                    data[3],
                                    self.Geb_Datum,
                                    data[5],
                                    data[6],
                            )
                            lst = list(data)
                            if '..' in lst :
                                lst[4]= ''
                                lst = list(filter(None, lst))
                            if len(lst) == 0:
                                pass
                            else:
                                lst[0]=''
                                if (Database().search_patient(lst)):
                                    pass
                                else:
                                    del lst[0]
                                    Database().insert_patient(lst)
                                    self.progress["value"] = bar
                                    self.progress.update()
                                    self.display_data()
                        else:
                            self.valueErrorMessage = "Invalid input in field " + validata_data
                            messagebox.showerror("Value Error", self.valueErrorMessage)
                self.progress.grid_forget()

    def delete_all(self):
        msg = messagebox.askyesno("Reset", "Sind Sie sicher, Sie werden alles löchen?!!!")
        if(msg):
            error =  messagebox.showerror("Error", "Are you Sure You want to Delete Everything!!!!")
            if(error):
                msg =  messagebox.askyesno("Error", "Es gibt keine Möglichkeit diese Daten nochmal von Datenbanken zu konstruieren.")
                if(msg):
                    Database().delete_patienten_table()
                    refresh=self.display_data()

