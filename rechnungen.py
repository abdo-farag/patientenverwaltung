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
from gen_rechnungen import *
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

class rechnungen(object):
    def __init__(self, parent):

        self.TNotebook1=parent

        self.TNotebook1_t3 = ttk.Frame(self.TNotebook1, width=300, height=200)
        self.TNotebook1.add(self.TNotebook1_t3, padding=3)
        self.TNotebook1.tab(3, text="Rechnungen", compound="left", underline="-1")

        self.TNotebook2 = ttk.Notebook(self.TNotebook1_t3)
        self.TNotebook2.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.TNotebook2.configure(takefocus="", width=300)

        self.TNotebook2_t0 = ttk.Frame(self.TNotebook2, width=300, height=200)
        self.TNotebook2.add(self.TNotebook2_t0, padding=3)
        self.TNotebook2.tab(0, text="Neue erstellen", compound="left", underline="-1")


        self.TNotebook2_t1 = ttk.Frame(self.TNotebook2, width=300, height=200)
        self.TNotebook2.add(self.TNotebook2_t1, padding=3)
        self.TNotebook2.tab(1, text="verwalten", compound="left", underline="-1")

        self.TreeviewFrame = tk.Frame(self.TNotebook2_t1, width=1900, height=850, background="#f6f6f6")
        self.TreeviewFrame.place(anchor="c", relx=0.5, rely=0.575, relheight=0.85, relwidth=1.0)
        self.Treeview = ScrolledTreeView(self.TreeviewFrame)
        self.Treeview.place(anchor="c", relx=0.5, rely=0.55, relheight=0.9, relwidth=1.0)
        self.Treeview["columns"]=("ID", "Nummer", "Patient", "Anschrift", "Leistungname", "Datum", "Gesamtbetrag")
        self.Treeview['show'] = 'headings'
        self.Treeview.tag_configure('oddrow', background='#FFA5A5')
        self.Treeview.tag_configure('evenrow', background='#FFD6D6')
        self.Treeview.tag_configure('bezhalt_odd', background='#8CFF7F')
        self.Treeview.tag_configure('bezhalt_even', background='#B5FFAD')
        self.Treeview.bind("<Double-1>", self.double_click)

        self.Treeview.heading('ID', text='ID', command=lambda: treeview_sort_column(self.Treeview, 'ID', False))
        self.Treeview.column('ID', minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Nummer', text='Nummer', command=lambda: treeview_sort_column(self.Treeview, 'Nummer', False))
        self.Treeview.column('Nummer',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Patient', text='Patient', command=lambda: treeview_sort_column(self.Treeview, 'Patient', False))
        self.Treeview.column('Patient',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Anschrift', text='Anschrift', command=lambda: treeview_sort_column(self.Treeview, 'Anschrift', False))
        self.Treeview.column('Anschrift',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Leistungname', text='Leistung Name', command=lambda: treeview_sort_column(self.Treeview, 'Leistungname', False))
        self.Treeview.column('Leistungname',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Datum', text='Datum', command=lambda: treeview_sort_column(self.Treeview, 'Datum', False))
        self.Treeview.column('Datum',minwidth='20',stretch='1',anchor='w')

        self.Treeview.heading('Gesamtbetrag', text='Gesamtbetrag', command=lambda: treeview_sort_column(self.Treeview, 'Gesamtbetrag', False))
        self.Treeview.column('Gesamtbetrag',minwidth='20',stretch='1',anchor='w')

        #gen_rechnungen(self.TNotebook2_t0, self.Treeview)
        self.gen_rech = gen_rechnungen(self.TNotebook2_t0, self.Treeview)

        self.Label0 = ttk.Label(self.TreeviewFrame)
        self.Label0.place(relx=0.0, rely=0.03, height=21, width=260)
        self.Label0.configure(anchor='w', text='''ID:''', font="Arial 12 bold")

        self.ID = ttk.Entry(self.TreeviewFrame)
        self.ID.place(relx=0.0, rely=0.06, relheight=0.035, relwidth=0.135)
        self.ID.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label1 = ttk.Label(self.TreeviewFrame)
        self.Label1.place(relx=0.142, rely=0.03, height=21, width=260)
        self.Label1.configure(anchor='w', text='''Nummer:''', font="Arial 12 bold")

        self.Nummer = ttk.Entry(self.TreeviewFrame)
        self.Nummer.place(relx=0.142, rely=0.06, relheight=0.035, relwidth=0.135)
        self.Nummer.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label2 = ttk.Label(self.TreeviewFrame)
        self.Label2.place(relx=0.285, rely=0.03, height=21, width=260)
        self.Label2.configure(anchor='w', text='''Patient:''', font="Arial 12 bold")

        self.Patient = ttk.Entry(self.TreeviewFrame)
        self.Patient.place(relx=0.285, rely=0.06, relheight=0.035, relwidth=0.135)
        self.Patient.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label3 = ttk.Label(self.TreeviewFrame)
        self.Label3.place(relx=0.428, rely=0.03, height=21, width=260)
        self.Label3.configure(anchor='w', text='''Anschrift:''', font="Arial 12 bold")

        self.Anschrift = ttk.Entry(self.TreeviewFrame)
        self.Anschrift.place(relx=0.428, rely=0.06, relheight=0.035, relwidth=0.135)
        self.Anschrift.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label4 = ttk.Label(self.TreeviewFrame)
        self.Label4.place(relx=0.571, rely=0.03, height=21, width=260)
        self.Label4.configure(anchor='w', text='''Leistungname:''', font="Arial 12 bold")

        self.Leistungname = ttk.Entry(self.TreeviewFrame)
        self.Leistungname.place(relx=0.571, rely=0.06, relheight=0.035, relwidth=0.135)
        self.Leistungname.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label5 = ttk.Label(self.TreeviewFrame)
        self.Label5.place(relx=0.714, rely=0.03, height=21, width=260)
        self.Label5.configure(anchor='w', text='''Datum:''', font="Arial 12 bold")

        self.Datum = ttk.Entry(self.TreeviewFrame)
        self.Datum.place(relx=0.714, rely=0.06, relheight=0.035, relwidth=0.135)
        self.Datum.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label6 = ttk.Label(self.TreeviewFrame)
        self.Label6.place(relx=0.857, rely=0.03, height=21, width=260)
        self.Label6.configure(anchor='w', text='''Gesamtbetrag:''', font="Arial 12 bold")

        self.Gesamtbetrag = ttk.Entry(self.TreeviewFrame)
        self.Gesamtbetrag.place(relx=0.857, rely=0.06, relheight=0.035, relwidth=0.135)
        self.Gesamtbetrag.configure(background="white", font="Arial 12 bold", justify='left')


        # Button widgets
        self.BezahltB = ttk.Button(self.TNotebook2_t1, width = 20, text = "Bezahlt!", command=lambda
                    mark=1: self.bezahlt_mark(mark))
        self.BezahltB.place(relx=0.0, rely=0.02, height=38, width=150)
        self.BezahltB_Tip = CreateToolTip(self.BezahltB,
                'Die Taste dient zum Markieren  Rechnung als Umbezahlt.')

        self.UnbezahltB = ttk.Button(self.TNotebook2_t1, width = 20, text = "Unbazahlt!", command=lambda
                    mark=0: self.bezahlt_mark(mark))
        self.UnbezahltB.place(relx=0.0, rely=0.09, height=38, width=150)
        self.UnbezahltB_Tip = CreateToolTip(self.UnbezahltB,
                'Die Taste dient zum Markieren  Rechnung als Umbezahlt.')


        self.AktualisierenB = ttk.Button(self.TNotebook2_t0, width = 20, text = "Aktualisieren", command = self.update_rechnung)
        self.AktualisierenB.place(relx=0.4, rely=0.09, height=38, width=150)
        self.AktualisierenB_Tip = CreateToolTip(self.AktualisierenB,
                'Die Taste dient zum Aktualisieren eine Rechnung.\n'
                'Nach der Auswahl eine Rechnung. Ändern Sie, was Sie wollen, dann drücken Sie mich.')


        self.LoeschenB = ttk.Button(self.TNotebook2_t1, text = "Löschen", command = self.delete_record)
        self.LoeschenB.place(relx=0.2, rely=0.02, height=38, width=150)
        self.LoeschenB_Tip = CreateToolTip(self.LoeschenB,
                'Die Taste dient zum Löschen ein oder mehr Rechnungen.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')

        self.AuswaehlenB = ttk.Button(self.TNotebook2_t1, width = 20, text = "Auswählen", command = self.select_rechnung)
        self.AuswaehlenB.place(relx=0.2, rely=0.09, height=38, width=150)
        self.AuswaehlenB_Tip = CreateToolTip(self.AuswaehlenB,
                'Die Taste dient zum einen Rekord zu auswählen (Doppelklick), um zu aktualisieren.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')


        self.SuchenB = ttk.Button(self.TNotebook2_t1, width = 20, text = "Suchen", command = self.search_record)
        self.SuchenB.place(relx=0.4, rely=0.02, height=38, width=150)
        self.SuchenB_Tip = CreateToolTip(self.SuchenB,
                'Die Taste dient zum Suchen eine Rechnung.\n'
                'Sie können mit ein oder mehr Eingaben Suchen. Füllen Sie die Eingebe bzw Eingaben, dann drücken Sie mich.')

        self.RefreshB = ttk.Button(self.TNotebook2_t1, width = 20, text = "Refresh", command = self.display_data)
        self.RefreshB.place(relx=0.4, rely=0.09, height=38, width=150)
        self.RefreshB_Tip = CreateToolTip(self.RefreshB,
                'Die Taste dient zur Suche abbrechen, oder Daten Aktualisieren.\n'
                'Nach Ihre Suche drücken Sie mich.')

        self.ExportierenB = ttk.Button(self.TNotebook2_t1, width = 20, text = "Daten Exportieren", command = self.write_to_csv)
        self.ExportierenB.place(relx=0.6, rely=0.02, height=38, width=150)
        self.ExportierenB_Tip = CreateToolTip(self.ExportierenB,
                'Die Taste dient zum Exportieren Daten (Backup).')

        self.ImportierenB = ttk.Button(self.TNotebook2_t1, width = 20,text='Daten Importieren', command=self.load_from_csv)
        self.ImportierenB.place(relx=0.6, rely=0.09, height=38, width=150)
        self.ImportierenB_Tip = CreateToolTip(self.ImportierenB,
                'Die Taste dient zum Importieren Daten (Recovery).')

        self.ResetB = ttk.Button(self.TNotebook2_t1, width = 20, text = "Reset!", command = self.delete_all)
        self.ResetB.place(relx=0.8, rely=0.045, height=38, width=150)
        self.ResetB_Tip = CreateToolTip(self.ResetB,
                'Die Taste dient zum Löchen Alle Daten .')

        self.refresh=self.display_data()
        
    def insert_data(self):
        if (Database().get_last_nummer_rechnung()):
            nummer =list(Database().get_last_nummer_rechnung())
            nummer = [x[0] for x in nummer][0]
            Nummer=str(int(nummer)+1)
        else:
            Nummer='5000'
        data = (
                Nummer,
                self.Patient.get(),
                self.Anschrift.get(),
                self.Leistungname.get(),
                self.Datum.get(),
                self.Gesamtbetrag.get(),
                )
        Database().insert_rechnung(data)
        self.display_data()
        self.Nummer.delete(0, END)
        self.Patient.delete(0, END)
        self.Anschrift.delete(0, END)
        self.Leistungname.delete(0, END)
        self.Datum.delete(0, END)
        self.Gesamtbetrag.delete(0, END)

    def delete_record(self):
        selection = self.Treeview.selection()
        for selected in selection:
            values = self.Treeview.item(selected, 'values')
            search_data=('', values[1], values[2], values[3], '', '', '', '',)
            ID = (Database().search_rechnung(search_data)[0])[0]
            data = (ID,)
            Database().delete_rechnung(data)
        refresh=self.display_data()

    def double_click(self, _event=None):
        self.select_rechnung()

    def select_rechnung(self):
        self.gen_rech.reset_rechnung()
        self.gen_rech.RechnungDatumE.delete(0, END)
        self.gen_rech.RechnungNummerE.delete(0, END)
        self.gen_rech.PatientNameE.delete(0, END)
        self.gen_rech.Geb_DataumE.delete(0, END)
        self.gen_rech.AnschriftE.delete(0, END)
        self.gen_rech.GesamtbetragE.delete(0, END)
        selected= self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')
        if all(values):
            name = list(values[2].split(" "))
            if (name):
                lst=('', name[0], name[1], '', '', values[3], '')
                get_patient=Database().search_patient(lst)
                geb_datum = list(get_patient[0])[4]

            leistungen_lst = values[4].split(",")
            for i in range(len(leistungen_lst)):
                wert=self.gen_rech.get_leistung_info(values[2], leistungen_lst[i])
                if self.gen_rech.Leistung_count > 1:
                    self.gen_rech.GesamtbetragL.grid_forget()
                    self.gen_rech.GesamtbetragE.grid_forget()
                    self.gen_rech.TextObenL.grid_forget()
                    self.gen_rech.TextOben.grid_forget()
                    self.gen_rech.TextUntenL.grid_forget()
                    self.gen_rech.TextUnten.grid_forget()
                    self.gen_rech.row +=2
                    self.gen_rech.add_lesitung_entry()
                    self.gen_rech.GesamtbetragE.delete(0, END)

                self.gen_rech.Leistung_NameE.insert(0, leistungen_lst[i])
                self.gen_rech.Leistung_WertE.insert(0, wert)
                self.gen_rech.Leistungen_list.append(leistungen_lst[i])
                self.gen_rech.Leistung_count += 1
            self.gen_rech.GesamtbetragE.insert(0, values[6])
            self.gen_rech.RechnungDatumE.insert(0, values[5])
            self.gen_rech.RechnungNummerE.insert(0, values[1])
            self.gen_rech.PatientNameE.insert(0, values[2])
            self.gen_rech.Geb_DataumE.insert(0, geb_datum)
            self.gen_rech.AnschriftE.insert(0, values[3])
            self.TNotebook2.select(0)
        else:
            self.valueErrorMessage = "Bitte, ein Record wählen"
            messagebox.showerror("Value Error", self.valueErrorMessage)

    def update_rechnung(self):
        Leistungen_list = list(filter(None, self.gen_rech.Leistungen_list))
        Leistungen = ','.join(Leistungen_list)
        selected = self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')
        search_data=('', values[1], values[2], values[3], '', '', '', '',)
        ID = (Database().search_rechnung(search_data)[0])[0]
        bezahlt = (Database().search_rechnung(search_data)[0])[7]
        data = (
                self.gen_rech.RechnungNummerE.get(),
                self.gen_rech.PatientNameE.get(),
                self.gen_rech.AnschriftE.get(),
                Leistungen,
                self.gen_rech.RechnungDatumE.get(),
                self.gen_rech.GesamtbetragE.get().replace(' €', '')+' €',
                bezahlt,
                #self.Treeview.set(selected, '#1')
                ID,
                )
        self.Treeview.item(selected, text='', values=(data))
        Database().update_rechnung(data)
        refresh=self.display_data()

    def search_record(self):
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        if (self.Gesamtbetrag.get()):
            Gesamtbetrag = self.Gesamtbetrag.get().replace(' €', '')+' €'
        else:
            Gesamtbetrag = self.Gesamtbetrag.get()
        data = (
                self.ID.get(),
                self.Nummer.get(),
                self.Patient.get(),
                self.Anschrift.get(),
                self.Leistungname.get(),
                self.Datum.get(),
                Gesamtbetrag,
                )
        lst = list(data)
        empty = list(filter(None, lst))
        if len(empty) == 0:
           refresh=self.display_data()
        else:
            i = 0
            for record in (Database().search_rechnung(lst)):
                i=i+1
                if (i % 2):
                    self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
                else:
                    self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

        self.ID.delete(0, END)
        self.Nummer.delete(0, END)
        self.Patient.delete(0, END)
        self.Anschrift.delete(0, END)
        self.Leistungname.delete(0, END)
        self.Datum.delete(0, END)
        self.Gesamtbetrag.delete(0, END)

    def display_data(self):
        nummer = Database().get_last_nummer_rechnung()
        for data in self.Treeview.get_children():
            self.Treeview.delete(data)
        i,j=0,0
        for record in (Database().display_rechnungen()):
            bezahlt = record[7]
            record = list(record)
            if bezahlt == 0:
                i=i+1
                record[0] = i
                if (i % 2):
                    self.Treeview.insert('', 'end', values=(record), tags = ('oddrow'))
                else:
                    self.Treeview.insert('', 'end', values=(record), tags = ('evenrow'))

        for record in (Database().display_rechnungen()):
            bezahlt = record[7]
            record = list(record)
            if bezahlt == 1:
                j = j+1
                record[0] = i + j
                if (j % 2):
                    self.Treeview.insert('', 'end', values=(record), tags = ('bezhalt_odd'))
                else:
                    self.Treeview.insert('', 'end', values=(record), tags = ('bezhalt_even'))

    def bezahlt_mark(self,mark):
        selected= self.Treeview.focus()
        values = self.Treeview.item(selected, 'values')
        if all(values):
            search_data=('', values[1], values[2], values[3], '', '', '', '',)
            ID = (Database().search_rechnung(search_data)[0])[0]
            data = (
                    values[1],
                    values[2],
                    values[3],
                    values[4],
                    values[5],
                    values[6],
                    mark,
                    ID,
                    #self.Treeview.set(selected, '#1')
                    )
            self.Treeview.item(selected, text='', values=(data))
            Database().update_rechnung(data)
            refresh=self.display_data()



    def write_to_csv(self):
        header=['ID', 'Nummer', 'Patient', 'Geschlecht','Geburtdatum', 'Adresse', 'Krankenversicherung']
        fname = asksaveasfilename(parent=self.TNotebook1, initialdir = default_path, title = "Select file", filetypes=(
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")), 
            confirmoverwrite=True, defaultextension=".csv" ) #,initialdir = (str(Path.home())) )
        if (fname):
            with open(fname, 'a') as rechnungen:
                self.write = csv.writer(rechnungen, dialect='excel')
                #self.write.writerow(header)
                for record in (Database().display_rechnungen()):
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
            with open(name, 'r', encoding='utf-8') as rechnungen:
                self.row = sum(1 for row in rechnungen)
                self.progress = ttk.Progressbar(self.TNotebook2_t1, orient = HORIZONTAL, length=150, value=0, mode = 'determinate')
                self.progress.grid(padx=(1148, 130), pady=(130, 1148))
                self.progress['maximum'] = self.row
            with open(name, 'r',encoding='utf-8') as rechnungen:
                bar = 0
                self.reader = csv.reader(rechnungen, dialect='excel')
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
                            if (Database().search_rechnung(lst)):
                                pass
                            else:
                                del lst[0]
                                Database().insert_rechnung(lst)
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
                    Database().delete_rechnungen_table()
                    refresh=self.display_data()
