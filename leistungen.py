import sys
import locale
import csv
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox, END, HORIZONTAL
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

class leistungen(object):
    def __init__(self, parent):

        self.TNotebook1=parent

        self.TNotebook1_t2 = ttk.Frame(self.TNotebook1, width=300, height=200)
        self.TNotebook1.add(self.TNotebook1_t2, padding=3)
        self.TNotebook1.tab(2, text="Leistungen", compound="left", underline="-1")

        self.TreeviewFrame = tk.Frame(self.TNotebook1_t2, width=1900, height=850, background="#f6f6f6")
        self.TreeviewFrame.place(anchor="c", relx=0.5, rely=0.575, relheight=0.85, relwidth=1.0)

        self.Treeview = ScrolledTreeView(self.TreeviewFrame)
        self.Treeview.place(anchor="c", relx=0.5, rely=0.55, relheight=0.9, relwidth=1.0)
        self.Treeview["columns"]=("ID", "Nummer", "Leistungname", "Wert-K", "Wert-P")
        self.Treeview['show'] = 'headings'
        self.Treeview.tag_configure('oddrow', background='#85FFB3')
        self.Treeview.tag_configure('evenrow', background='white')
        self.Treeview.bind("<Double-1>", self.double_click)


        self.Treeview.heading('ID', text='ID', command=lambda: treeview_sort_column(self.Treeview, 'ID', False))
        self.Treeview.column('ID', minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Nummer', text='Nummer', command=lambda: treeview_sort_column(self.Treeview, 'Leistungname', False))
        self.Treeview.column('Nummer',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Leistungname', text='Leistung Name', command=lambda: treeview_sort_column(self.Treeview, 'Leistungname', False))
        self.Treeview.column('Leistungname',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Wert-K', text='Wert-Kassenpatienten', command=lambda: treeview_sort_column(self.Treeview, 'Wert-K', False))
        self.Treeview.column('Wert-K',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Wert-P', text='Wert-Privatpatienten', command=lambda: treeview_sort_column(self.Treeview, 'Wert-P', False))
        self.Treeview.column('Wert-P',minwidth='20',stretch='1',anchor='w')

        self.Label0 = ttk.Label(self.TreeviewFrame)
        self.Label0.place(relx=0.0, rely=0.03, height=21, width=260)
        self.Label0.configure(anchor='w', text='''ID:''', font="Arial 12 bold")

        self.ID = ttk.Entry(self.TreeviewFrame)
        self.ID.place(relx=0.0, rely=0.06, relheight=0.035, relwidth=0.190)
        self.ID.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label1 = ttk.Label(self.TreeviewFrame)
        self.Label1.place(relx=0.200, rely=0.03, height=21, width=260)
        self.Label1.configure(anchor='w', text='''Nummer:''', font="Arial 12 bold")

        self.Nummer = ttk.Entry(self.TreeviewFrame)
        self.Nummer.place(relx=0.200, rely=0.06, relheight=0.035, relwidth=0.190)
        self.Nummer.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label2 = ttk.Label(self.TreeviewFrame)
        self.Label2.place(relx=0.400, rely=0.03, height=21, width=260)
        self.Label2.configure(anchor='w', text='''Leistung Name:''', font="Arial 12 bold")

        self.Leistungname = ttk.Entry(self.TreeviewFrame)
        self.Leistungname.place(relx=0.400, rely=0.06, relheight=0.035, relwidth=0.190)
        self.Leistungname.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label3 = ttk.Label(self.TreeviewFrame)
        self.Label3.place(relx=0.600, rely=0.03, height=21, width=260)
        self.Label3.configure(anchor='w', text='''Wert-Kassenpatienten:''', font="Arial 12 bold")

        self.WertK = ttk.Entry(self.TreeviewFrame)
        self.WertK.place(relx=0.600, rely=0.06, relheight=0.035, relwidth=0.190)
        self.WertK.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label4 = ttk.Label(self.TreeviewFrame)
        self.Label4.place(relx=0.800, rely=0.03, height=21, width=260)
        self.Label4.configure(anchor='w', text='''Wert-Privatpatienten:''', font="Arial 12 bold")

        self.WertP = ttk.Entry(self.TreeviewFrame)
        self.WertP.place(relx=0.800, rely=0.06, relheight=0.035, relwidth=0.190)
        self.WertP.configure(background="white", font="Arial 12 bold", justify='left')


        # Button widgets
        self.EinfuegenB = ttk.Button(self.TNotebook1_t2, text = "Einfügen", command = self.insert_data)
        self.EinfuegenB.place(relx=0.0, rely=0.02, height=38, width=150)
        self.EinfuegenB_Tip = CreateToolTip(self.EinfuegenB,
                'Die Taste dient zum Hinzufügen neue Leistung.\n'
                'Füllen Sie die folgenden Felder aus und drücken Sie mich.')


        self.LoeschenB = ttk.Button(self.TNotebook1_t2, text = "Löschen", command = self.delete_record)
        self.LoeschenB.place(relx=0.0, rely=0.09, height=38, width=150)
        self.LoeschenB_Tip = CreateToolTip(self.LoeschenB,
                'Die Taste dient zum Löschen ein oder mehr Leistungen.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')

        self.AuswaehlenB = ttk.Button(self.TNotebook1_t2, width = 20, text = "Auswählen", command = self.select_record)
        self.AuswaehlenB.place(relx=0.2, rely=0.02, height=38, width=150)
        self.AuswaehlenB_Tip = CreateToolTip(self.AuswaehlenB,
                'Die Taste dient zum einen Rekord zu auswählen(Doppelklick), um zu aktualisieren.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')


        self.AktualisierenB = ttk.Button(self.TNotebook1_t2, width = 20, text = "Aktualisieren", command = self.update_record)
        self.AktualisierenB.place(relx=0.2, rely=0.09, height=38, width=150)
        self.AktualisierenB_Tip = CreateToolTip(self.AktualisierenB,
                'Die Taste dient zum Aktualisieren Leistungsdaten.\n'
                'Nach der Auswahl eines Leistungen. Ändern Sie, was Sie wollen, dann drücken Sie mich.')


        self.SuchenB = ttk.Button(self.TNotebook1_t2, width = 20, text = "Suchen", command = self.search_record)
        self.SuchenB.place(relx=0.4, rely=0.02, height=38, width=150)
        self.SuchenB_Tip = CreateToolTip(self.SuchenB,
                'Die Taste dient zum Suchen eine Leistung.\n'
                'Sie können mit ein oder mehr Eingaben Suchen. Füllen Sie die Eingebe bzw Eingaben, dann drücken Sie mich.')

        self.RefreshB = ttk.Button(self.TNotebook1_t2, width = 20, text = "Refresh", command = self.display_data)
        self.RefreshB.place(relx=0.4, rely=0.09, height=38, width=150)
        self.RefreshB_Tip = CreateToolTip(self.RefreshB,
                'Die Taste dient zur Suche abbrechen, oder Daten Aktualisieren.\n'
                'Nach Ihre Suche drücken Sie mich.')

        self.ExportierenB = ttk.Button(self.TNotebook1_t2, width = 20, text = "Daten Exportieren", command = self.write_to_csv)
        self.ExportierenB.place(relx=0.6, rely=0.02, height=38, width=150)
        self.ExportierenB_Tip = CreateToolTip(self.ExportierenB,
                'Die Taste dient zum Exportieren Daten (Backup).')

        self.ImportierenB = ttk.Button(self.TNotebook1_t2, width = 20,text='Daten Importieren', command=self.load_from_csv)
        self.ImportierenB.place(relx=0.6, rely=0.09, height=38, width=150)
        self.ImportierenB_Tip = CreateToolTip(self.ImportierenB,
                'Die Taste dient zum Importieren Daten (Recovery).')

        self.ResetB = ttk.Button(self.TNotebook1_t2, width = 20, text = "Reset!", command = self.delete_all)
        self.ResetB.place(relx=0.8, rely=0.045, height=38, width=150)
        self.ResetB_Tip = CreateToolTip(self.ResetB,
                'Die Taste dient zum Löchen Alle Daten .')

        refresh=self.display_data()


    def Validate(self, Nummer, Leistungname, WertK, WertP):
        if not (Nummer.isdigit()) or len(Nummer) < 4:
            return "Nummer kleiner als 999"
        #elif not (Leistungname.isalpha()):
        #    return "Leistungname"
        elif not (WertK.isdigit()):
            return "WertK"
        elif not (WertP.isdigit()):
            return "WertP"
        else:
            return "SUCCESS"

    def insert_data(self):
        if (Database().get_last_nummer()):
            nummer =list(Database().get_last_nummer())
            nummer = [x[0] for x in nummer][0]
            Nummer=str(int(nummer)+1)
        else:
            Nummer='1000'
        validata_data = self.Validate(
                #self.Nummer.get(),
                Nummer,
                self.Leistungname.get(),
                self.WertK.get().replace(' €', ''),
                self.WertP.get().replace(' €', ''),
                )
        if (validata_data == "SUCCESS"):
            data = (
                    Nummer,
                    #self.Nummer.get(),
                    self.Leistungname.get(),
                    self.WertK.get().replace(' €', '')+' €',
                    self.WertP.get().replace(' €', '')+' €',
                    )
            Database().insert_leistung(data)
            refresh=self.display_data()
        else:
            self.valueErrorMessage = "Invalid input in field " + validata_data
            messagebox.showerror("Value Error", self.valueErrorMessage)
        self.ID.delete(0, END)
        self.Nummer.delete(0, END)
        self.Leistungname.delete(0, END)
        self.WertK.delete(0, END)
        self.WertP.delete(0, END)

    def delete_record(self):
        selection = self.Treeview.selection()
        for selected in selection:
            values = self.Treeview.item(selected, 'values')
            data = (values[0],)
            Database().delete_leistung(data)
        refresh=self.display_data()

    def double_click(self, _event=None):
        self.select_record()

    def select_record(self):
        self.ID.delete(0, END)
        self.Nummer.delete(0, END)
        self.Leistungname.delete(0, END)
        self.WertK.delete(0, END)
        self.WertP.delete(0, END)
        selected= self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')
        
        if (values): 
            self.ID.insert(0, values[0])
            self.Nummer.insert(0, values[1])
            self.Leistungname.insert(0, values[2])
            self.WertK.insert(0, values[3])
            self.WertP.insert(0, values[4])
        else:
            self.valueErrorMessage = "Bitte, ein Record wählen"
            messagebox.showerror("Value Error", self.valueErrorMessage)

    def update_record(self):
        selected = self.Treeview.focus()
        validata_data = self.Validate(
                self.Nummer.get(),
                self.Leistungname.get(),
                self.WertK.get().replace(' €', ''),
                self.WertP.get().replace(' €', ''),
                )
        if (validata_data == "SUCCESS"):
            data = (
                    self.Nummer.get(),
                    self.Leistungname.get(),
                    self.WertK.get().replace(' €', '')+' €',
                    self.WertP.get().replace(' €', '')+' €',
                    self.Treeview.set(selected, '#1')
                    )
            self.Treeview.item(selected, text='', values=(data))
            Database().update_leistung(data)
            refresh=self.display_data()

        else:
            self.valueErrorMessage = "Invalid input in field " + validata_data
            self.messagebox = messagebox.showerror("Value Error", self.valueErrorMessage)
        self.ID.delete(0, END)
        self.Nummer.delete(0, END)
        self.Leistungname.delete(0, END)
        self.WertK.delete(0, END)
        self.WertP.delete(0, END)


    def search_record(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        if (self.WertK.get()):
            WertK = self.WertK.get().replace(' €', '')+' €'
        else:
            WertK = self.WertK.get()
        if (self.WertP.get()):
            WertP = self.WertP.get().replace(' €', '')+' €'
        else:
            WertP = self.WertP.get()
        data = (
                self.ID.get(),
                self.Nummer.get(),
                self.Leistungname.get(),
                WertK,
                WertP,
                )
        lst = list(data)
        empty = list(filter(None, lst))
        if len(empty) == 0:
           refresh=self.display_data()
        else:
            i = 0
            for record in (Database().search_leistung(lst)):
                i=i+1
                if (i % 2):
                    self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
                else:
                    self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

        self.ID.delete(0, END)
        self.Nummer.delete(0, END)
        self.Leistungname.delete(0, END)
        self.WertK.delete(0, END)
        self.WertP.delete(0, END)


    def display_data(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        i=0
        for record in (Database().display_leistungen()):
            i=i+1
            if (i % 2):
                self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
            else:
                self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

    def write_to_csv(self):
        header=['ID', 'Nummer', 'Leistungname', 'Geschlecht','Geburtdatum', 'Adresse', 'Krankenversicherung']
        fname = asksaveasfilename(parent=self.TNotebook1, initialdir = default_path, title = "Select file", filetypes=(
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")), 
            confirmoverwrite=True, defaultextension=".csv" ) #,initialdir = (str(Path.home())) )
        if (fname):
            with open(fname, 'a') as leistungen:
                self.write = csv.writer(leistungen, dialect='excel')
                #self.write.writerow(header)
                for record in (Database().display_leistungen()):
                    self.write.writerow(record)


    def load_from_csv(self):
        import time
        Database().createTable()
        name = askopenfilename(parent=self.TNotebook1, initialdir = default_path, title = "Import File", filetypes=(
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")),
            defaultextension=".csv" ) #,initialdir = (str(Path.home())) )
        if name:
            with open(name, 'r', encoding='utf-8') as leistungen:
                self.row = sum(1 for row in leistungen)
                self.progress = ttk.Progressbar(self.TNotebook1_t2, orient = HORIZONTAL, length=150, value=0, mode = 'determinate')
                self.progress.grid(padx=(1148, 130), pady=(130, 1148))
                self.progress['maximum'] = self.row
            with open(name, 'r',encoding='utf-8') as leistungen:
                bar = 0
                self.reader = csv.reader(leistungen, dialect='excel')
                for line in self.reader:
                    bar = bar + 1
                    #data = tuple(line.rstrip('\n').split(","))
                    data = tuple(line)
                    if not all(data):
                        pass
                    else:
                        validata_data = self.Validate(
                                data[1],
                                data[2],
                                data[3].replace(' €', ''),
                                data[4].replace(' €', ''),
                        )
                        if (validata_data == "SUCCESS"):
                            data = (
                                    data[0],
                                    data[1],
                                    data[2],
                                    data[3],
                                    data[4],
                            )
                            lst = list(data)
                            if len(lst) == 0:
                                pass
                            else:
                                lst[0]=''
                                if (Database().search_leistung(lst)):
                                    pass
                                else:
                                    del lst[0]
                                    Database().insert_leistung(lst)
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
                    Database().delete_leistungen_table()
                    refresh=self.display_data()
    
