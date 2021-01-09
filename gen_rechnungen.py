import sys, subprocess, csv
from tkinter import PhotoImage, END, Canvas, W, E
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from tkinter import messagebox
from database import Database
from datetime import datetime, timedelta
from tooltip import CreateToolTip
from scrollbar_treeview import ScrolledTreeView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.shapes import Rect
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black
from image_base64 import button_icon
import global_module

if sys.platform == "win32":
    import win32api
    import win32print


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

class gen_rechnungen(object):
    def __init__(self, parent, rechnungen_treeview):
        self.TNotebook2_t0=parent
        self.Treeview = rechnungen_treeview

        self.RechnungFrame0 = ttk.Frame(self.TNotebook2_t0)#, width=300, height=200, background="White")
        self.RechnungFrame0.place(anchor="c", relx=0.2, rely=0.5, relheight=1.0, relwidth=0.39)

        self.ScrollbarV = ttk.Scrollbar(self.RechnungFrame0,orient=tk.VERTICAL)
        self.ScrollbarV.pack(side="right", fill="y")
        self.ScrollbarH = ttk.Scrollbar(self.RechnungFrame0,orient=tk.HORIZONTAL)
        self.ScrollbarH.pack(side="bottom", fill="x")

        self.Canvas =Canvas(self.RechnungFrame0, background="#f6f6f6", highlightthickness=0)
        self.RechnungFrame = ttk.Frame(self.Canvas)#, width=300, height=200, background="White")

        self.RechnungFrame.bind("<Configure>", lambda e: self.Canvas.configure( scrollregion=self.Canvas.bbox("all")))
        self.Canvas.create_window((0,0),window=self.RechnungFrame,anchor='nw')

        self.Canvas.configure(yscrollcommand=self.ScrollbarV.set, xscrollcommand=self.ScrollbarH.set)

        self.Canvas.pack(side="left", expand=True, fill='both')#, fill=tk.BOTH, expand=True)
        self.Canvas.bind("<Enter>", self._bind_mouse)
        self.Canvas.bind("<Leave>", self._unbind_mouse)

        self.ScrollbarV['command'] = self.Canvas.yview
        self.ScrollbarH['command'] = self.Canvas.xview


        self.PatientFrame = ttk.Frame(self.TNotebook2_t0, width=300, height=200)#, background="Black")
        self.PatientFrame.place(anchor="w", relx=0.4, rely=0.75, relheight=0.7, relwidth=0.3)

        self.LeistungFrame = ttk.Frame(self.TNotebook2_t0, width=300, height=200)#, background="Red")
        self.LeistungFrame.place(anchor="w", relx=0.7, rely=0.75, relheight=0.7, relwidth=0.3)

        self.PatientTreeview = ScrolledTreeView(self.PatientFrame)
        self.PatientTreeview.place(anchor="c", relx=0.5, rely=0.5, relheight=0.7, relwidth=0.995)
        self.PatientTreeview["columns"]=("Vorname", "Nachname", "Geburtdatum")
        self.PatientTreeview['show'] = 'headings'
        self.PatientTreeview.tag_configure('oddrow', background='#b3e7f4')
        self.PatientTreeview.tag_configure('evenrow', background='white')
        self.PatientTreeview.bind("<Double-1>", self.double_click_patient)

        self.PatientTreeview.heading('Vorname', text='Vorname', command=lambda: treeview_sort_column(self.PatientTreeview, 'Vorname', False))
        self.PatientTreeview.column('Vorname',width='180',stretch='1',anchor='w')

        self.PatientTreeview.heading('Nachname', text='Nachname', command=lambda: treeview_sort_column(self.PatientTreeview, 'Nachname', False))
        self.PatientTreeview.column('Nachname',width='180',stretch='1',anchor='w')

        self.PatientTreeview.heading('Geburtdatum', text='Geburtdatum', command=lambda:
                treeview_sort_column(self.PatientTreeview, 'Geburtdatum', False))
        self.PatientTreeview.column('Geburtdatum',width='180',stretch='1',anchor='w')

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


        self.Label1 = ttk.Label(self.PatientFrame)
        self.Label1.place(relx=0.0, rely=0.08, height=21, width=260)
        self.Label1.configure(anchor='w', text='''Vorname:''', font="Arial 12 bold")

        self.Vorname = ttk.Entry(self.PatientFrame)
        self.Vorname.place(relx=0.0, rely=0.113, relheight=0.035, relwidth=0.300)
        self.Vorname.configure(background="white", font="Arial 10 bold", justify='left')

        self.Label2 = ttk.Label(self.PatientFrame)
        self.Label2.place(relx=0.320, rely=0.08, height=21, width=260)
        self.Label2.configure(anchor='w', text='''Nachname:''', font="Arial 12 bold")

        self.Nachname = ttk.Entry(self.PatientFrame)
        self.Nachname.place(relx=0.320, rely=0.113, relheight=0.035, relwidth=0.300)
        self.Nachname.configure(background="white", font="Arial 10 bold", justify='left')

        self.Label4 = ttk.Label(self.PatientFrame)
        self.Label4.place(relx=0.645, rely=0.08, height=21, width=300)
        self.Label4.configure(anchor='w',text='''Geburtdatum: T.M.Y''',font="Arial 12 bold")

        self.Geb_T_Box = ttk.Combobox(self.PatientFrame, values = self.TagList)
        self.Geb_M_Box = ttk.Combobox(self.PatientFrame, values = self.MonatList)
        self.Geb_Y_Box = ttk.Combobox(self.PatientFrame, values = self.JahrList)

        self.Geb_T_Box.place(relx=0.645, rely=0.113, relheight=0.035, relwidth=0.07)
        self.Geb_T_Box.configure(background="white", font="Arial 10 bold", justify='left')
        self.Geb_M_Box.place(relx=0.718, rely=0.113, relheight=0.035, relwidth=0.16)
        self.Geb_M_Box.configure(background="white", font="Arial 10 bold", justify='left')
        self.Geb_Y_Box.place(relx=0.880, rely=0.113, relheight=0.035, relwidth=0.1)
        self.Geb_Y_Box.configure(background="white", font="Arial 10 bold", justify='left')


        self.SuchenB = ttk.Button(self.PatientFrame, width = 20, text = "Patient Suchen", command = self.search_patient_record)
        self.SuchenB.place(relx=0.0, rely=0.0, height=38, width=150)
        self.SuchenB_Tip = CreateToolTip(self.SuchenB,
                'Die Taste dient zum Suchen ein Patient.\n'
                'Sie können mit ein oder mehr Eingaben Suchen. Füllen Sie die Eingebe bzw Eingaben, dann drücken Sie mich.')

        self.AuswählenB = ttk.Button(self.PatientFrame, width = 20, text = "Auswählen", command = self.select_patient_record)
        self.AuswählenB.place(relx=0.5, rely=0.0, height=38, width=150)
        self.AuswählenB_Tip = CreateToolTip(self.AuswählenB,
                'Die Taste dient zum einen Rekord zu auswählen (Doppelklick).\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')

        self.LeistungTreeview = ScrolledTreeView(self.LeistungFrame)
        self.LeistungTreeview.place(anchor="c", relx=0.5, rely=0.5, relheight=0.7, relwidth=0.995)
        self.LeistungTreeview["columns"]=("Nummer", "Leistungname")
        self.LeistungTreeview['show'] = 'headings'
        self.LeistungTreeview.tag_configure('oddrow', background='#85FFB3')
        self.LeistungTreeview.tag_configure('evenrow', background='white')
        self.LeistungTreeview.bind("<Double-1>", self.double_click_leistung)

        self.LeistungTreeview.heading('Nummer', text='Nummer', command=lambda: treeview_sort_column(self.LeistungTreeview, 'Leistungname', False))
        self.LeistungTreeview.column('Nummer',minwidth='20',stretch='1',anchor='w')

        self.LeistungTreeview.heading('Leistungname', text='Leistung Name', command=lambda:
                treeview_sort_column(self.LeistungTreeview, 'Leistungname', False))
        self.LeistungTreeview.column('Leistungname',minwidth='20',stretch='1',anchor='w')

        self.Label1 = ttk.Label(self.LeistungFrame)
        self.Label1.place(relx=0.0, rely=0.08, height=21, width=260)
        self.Label1.configure(anchor='w', text='''Nummer:''', font="Arial 12 bold")

        self.Nummer = ttk.Entry(self.LeistungFrame)
        self.Nummer.place(relx=0.0, rely=0.113, relheight=0.035, relwidth=0.480)
        self.Nummer.configure(background="white", font="Arial 12 bold", justify='left')

        self.Label2 = ttk.Label(self.LeistungFrame)
        self.Label2.place(relx=0.500, rely=0.08, height=21, width=260)
        self.Label2.configure(anchor='w', text='''Leistung Name:''', font="Arial 12 bold")

        self.Leistungname = ttk.Entry(self.LeistungFrame)
        self.Leistungname.place(relx=0.500, rely=0.113, relheight=0.035, relwidth=0.480)
        self.Leistungname.configure(background="white", font="Arial 12 bold", justify='left')

        self.SuchenB = ttk.Button(self.LeistungFrame, width = 20, text = "Leistung Suchen", command = self.search_leistung_record)
        self.SuchenB.place(relx=0.0, rely=0.0, height=38, width=150)
        self.SuchenB_Tip = CreateToolTip(self.SuchenB,
                'Die Taste dient zum Suchen eine Leistung.\n'
                'Sie können mit ein oder mehr Eingaben Suchen. Füllen Sie die Eingebe bzw Eingaben, dann drücken Sie mich.')

        self.AuswaehlenB = ttk.Button(self.LeistungFrame, width = 20, text = "Auswählen", command = self.select_leistung_record)
        self.AuswaehlenB.place(relx=0.5, rely=0.0, height=38, width=150)
        self.AuswaehlenB_Tip = CreateToolTip(self.AuswaehlenB,
                'Die Taste dient zum einen Rekord zu auswählen, um zu aktualisieren.\n'
                'Drücken Sie auf einen Rekord, dann drücken Sie mich.')

        x = 2
        y = 8
        wL = 25

        self.RechnungDatumL = ttk.Label(self.RechnungFrame)#, background='White')
        self.RechnungDatumL.grid(row=2, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.RechnungDatumL.configure(anchor='w', width=wL, text='''Rechnunng Datum:''', font="Arial 12 bold")

        self.RechnungDatumE = ttk.Entry(self.RechnungFrame)
        self.RechnungDatumE.grid(row=2, column=1,sticky=W, padx=x, pady=y, columnspan=1)
        self.RechnungDatumE.configure(background="white", width=50, font="Arial 12 bold", justify='left')

        self.RechnungNummerL = ttk.Label(self.RechnungFrame)#, background='White')
        self.RechnungNummerL.grid(row=4, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.RechnungNummerL.configure(anchor='w', width=wL, text='''Rechnung Nummer:''', font="Arial 12 bold")

        self.RechnungNummerE = ttk.Entry(self.RechnungFrame)
        self.RechnungNummerE.grid(row=4, column=1,sticky=W, padx=x, pady=y, columnspan=1)
        self.RechnungNummerE.configure(background="white", width=50, font="Arial 12 bold", justify='left')

        self.BankverbindungL = ttk.Label(self.RechnungFrame)#, background='White')
        self.BankverbindungL.grid(row=6, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.BankverbindungL.configure(anchor='w', width=wL, text='''Bankverbindung:''', font="Arial 12 bold")

        self.BankverbindungE = ttk.Entry(self.RechnungFrame)
        self.BankverbindungE.grid(row=6, column=1, sticky=W, padx=x, pady=y, columnspan=1)
        self.BankverbindungE.configure(background="white", width=50, font="Arial 12 bold", justify='left')
        self.BankverbindungE.insert(0, "DE81500105178465346556")

        self.PatientNameL = ttk.Label(self.RechnungFrame)#, background='White')
        self.PatientNameL.grid(row=8, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.PatientNameL.configure(anchor='w', width=wL, text='''Patient Name:''', font="Arial 12 bold")

        self.PatientNameE = ttk.Entry(self.RechnungFrame)
        self.PatientNameE.grid(row=8, column=1,sticky=W, padx=x, pady=y, columnspan=1)
        self.PatientNameE.configure(background="white", width=50, font="Arial 12 bold", justify='left')

        self.Geb_DataumL = ttk.Label(self.RechnungFrame)#, background='White')
        self.Geb_DataumL.grid(row=10, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.Geb_DataumL.configure(anchor='w', width=wL, text='''Geburtsdatum:''', font="Arial 12 bold")

        self.Geb_DataumE = ttk.Entry(self.RechnungFrame)
        self.Geb_DataumE.grid(row=10, column=1,sticky=W, padx=x, pady=y, columnspan=1)
        self.Geb_DataumE.configure(background="white", width=50, font="Arial 12 bold", justify='left')

        self.AnschriftL = ttk.Label(self.RechnungFrame)#, background='White')
        self.AnschriftL.grid(row=12, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.AnschriftL.configure(anchor='w', width=wL, text='''Anschrift:''', font="Arial 12 bold")

        self.AnschriftE = ttk.Entry(self.RechnungFrame)
        self.AnschriftE.grid(row=12, column=1,sticky=W, padx=x, pady=y, columnspan=1)
        self.AnschriftE.configure(background="white", width=50, font="Arial 12 bold", justify='left')

        self.LeistungenL = ttk.Label(self.RechnungFrame)#, background='White')
        self.LeistungenL.grid(row=14, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.LeistungenL.configure(anchor='w', width=wL, text='''Leistungen List''', font="Arial 12 bold")

        self.Leistungen_NameL = ttk.Label(self.RechnungFrame)#, background='White')
        self.Leistungen_NameL.grid(row=14, column=1, sticky=W, padx=x, pady=y, columnspan=1)
        self.Leistungen_NameL.configure(anchor='c', width=32, text='''Leistung Name''', font="Arial 12 bold")

        self.Leistungen_WertL = ttk.Label(self.RechnungFrame)#, background='White')
        self.Leistungen_WertL.grid(row=14, column=1, sticky=E, padx=x, pady=y, columnspan=1)
        self.Leistungen_WertL.configure(anchor='c', width=9, text='''Wert''', font="Arial 14 bold")

        self.Leistung_count = 1
        self.row = 16

        self.update_rechnung_datum()
        self.update_rechnung_nummer()

        self.display_patient_data()
        self.display_leistung_data()
        self.Leistungen_list = []

        self.EinfuegenB = ttk.Button(self.TNotebook2_t0, text = "Einfügen", command = self.insert_data)
        self.EinfuegenB.place(relx=0.4, rely=0.02, height=38, width=150)
        self.EinfuegenB_Tip = CreateToolTip(self.EinfuegenB,
                'Die Taste dient zum Hinzufügen neue Rechnung.\n'
                'Füllen Sie die folgenden Felder aus und drücken Sie mich.')

        self.PDF_GenB = ttk.Button(self.TNotebook2_t0, text = "PDF generieren", command = self.pdf_generieren)
        self.PDF_GenB.place(relx=0.6, rely=0.02, height=38, width=150)
        self.PDF_Gen_Tip = CreateToolTip(self.PDF_GenB,
                'Die Taste dient zum Generieren Rechnung im pdf-Format.')

        self.ResetB = ttk.Button(self.TNotebook2_t0, text = "Reset Form", command = self.reset_rechnung)
        self.ResetB.place(relx=0.6, rely=0.09, height=38, width=150)
        self.ResetB_Tip = CreateToolTip(self.ResetB,
                'Die Taste dient zum Zurücksetzen Rechnungsfrom zu Standard.')

        self.PrintB = ttk.Button(self.TNotebook2_t0, text = "Print", command = self.print_rechnung)
        self.PrintB.place(relx=0.8, rely=0.02, height=38, width=150)
        self.PrintB_Tip = CreateToolTip(self.ResetB,
                'Die Taste dient zum Drucken eine Rechnung, nach PDF Generierung.')

        self.Printer_ListBOXL = ttk.Label(self.TNotebook2_t0)
        self.Printer_ListBOXL.place(relx=0.8, rely=0.07, height=21, width=150)
        self.Printer_ListBOXL.configure(anchor='w',text='''Drucker List''',font="Arial 12 bold")

        all_printers = []
        if sys.platform == "win32":
            for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
                printer = p[2]
                all_printers.append(printer)
        else:
            all_printers = subprocess.getoutput("lpstat -a | awk '{print $1}'").split("\n")

        self.Printer_ListBOX = ttk.Combobox(self.TNotebook2_t0, values = all_printers)
        self.Printer_ListBOX.place(relx=0.8, rely=0.09, relheight=0.035, relwidth=0.08)
        self.Printer_ListBOX.configure(background="white", font="Arial 10 bold", justify='left')



        self.photo = PhotoImage(data = button_icon)

        self.add_lesitung_entry()

    def add_lesitung_entry(self):
        x = 2
        y = 2
        wL = 25
        self.Leistung_text = str(self.Leistung_count) + '. Leistung'

        self.Leistung_NameL = ttk.Label(self.RechnungFrame)#, background='White')
        self.Leistung_NameL.grid(row=self.row, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.Leistung_NameL.configure(anchor='w', width=wL, text=self.Leistung_text, font="Arial 12 bold")
        
        if self.row >= 16:
            self.MinusB = ttk.Button(self.RechnungFrame, image = self.photo, command=lambda 
                    row=self.row, column=0: self.delete_entry(row, column))
            self.MinusB.grid(row=self.row, column=2,sticky=W)
            self.image = self.photo
            #self.MinusB.config( height = 1, width = 1 )
            #self.MinusB.place(relx=0.96, rely=0.365, height=10, width=20)

        self.Leistung_NameE = ttk.Entry(self.RechnungFrame)
        self.Leistung_NameE.grid(row=self.row, column=1,sticky=W, padx=x, pady=y, columnspan=1)
        self.Leistung_NameE.configure(background="white", width=35, font="Arial 12 bold", justify='left')

        self.Leistung_WertE = ttk.Entry(self.RechnungFrame)
        self.Leistung_WertE.grid(row=self.row, column=1,sticky=E, padx=x, pady=y, columnspan=1)
        self.Leistung_WertE.configure(background="white", width=10, font="Arial 12 bold", justify='left')

        self.GesamtbetragL = ttk.Label(self.RechnungFrame)#, background='White')
        self.GesamtbetragL.grid(row=self.row+2, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.GesamtbetragL.configure(anchor='w', width=wL, text='''Gesamtbetrag''', font="Arial 12 bold")

        self.GesamtbetragE = ttk.Entry(self.RechnungFrame)
        self.GesamtbetragE.grid(row=self.row+2, column=1,sticky=E, padx=x, pady=y, columnspan=1)
        self.GesamtbetragE.configure(background="white", width=50, font="Arial 12 bold", justify='left')
        self.GesamtbetragE.insert(0, "0 €")

        self.TextObenL = ttk.Label(self.RechnungFrame)#, background='White')
        self.TextObenL.grid(row=self.row+4, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.TextObenL.configure(anchor='w', width=wL, text='''Oben Text''', font="Arial 12 bold")

        self.TextOben = tk.Text(self.RechnungFrame)
        self.TextOben.grid(row=self.row+4, column=1)#,sticky=E, padx=x, pady=y, columnspan=1)
        self.TextOben.configure(background="white", width=50,height=5, font="Arial 12 bold")
        self.TextOben.insert(tk.END, "vielen Dank für Ihren Auftrag und das damit vebunden Verterauen! \n"
                "Für Meine Leistung im verganenen Monat erlaube ich mir folgenden Leistungen in Rechnung zu stellen.")

        self.TextUntenL = ttk.Label(self.RechnungFrame)#, background='White')
        self.TextUntenL.grid(row=self.row+6, column=0, sticky=W, padx=x, pady=y, columnspan=1)
        self.TextUntenL.configure(anchor='w', width=wL, text='''Unten Text''', font="Arial 12 bold")

        self.TextUnten = tk.Text(self.RechnungFrame)
        self.TextUnten.grid(row=self.row+6, column=1)#,sticky=E, padx=x, pady=y, columnspan=1)
        self.TextUnten.configure(background="white", width=50,height=5, font="Arial 12 bold")
        self.date_15D = datetime.now() + timedelta(15)
        self.data_15D = self.date_15D.strftime('%d.%B.%Y')
        self.text = ("Bitte begleichen Sie den Gesamtbetrag von " +
                self.GesamtbetragE.get() +" bis zum "+ self.data_15D +
                " auf das unten genant Bankkonto.\n" +
                "Bei Rückfragen stehe ich Ihnen wie gewohnt jederzeit gerne zur Verfügung. \n\n" +
                "Mit besten Gesundheitswünschen\n\n"
                "Muster Klinik")
        self.TextUnten.insert(tk.END, self.text)

    def update_rechnung_nummer(self):
        if (Database().get_last_nummer_rechnung()):
            nummer =list(Database().get_last_nummer_rechnung())
            nummer = [x[0] for x in nummer][0]
            Nummer=str(int(nummer)+1)
        else:
            Nummer='5000'
        self.RechnungNummerE.insert(0, Nummer)

    def update_rechnung_datum(self):
        self.now = datetime.now()
        self.data = self.now.strftime('%d.%B.%Y')
        self.RechnungDatumE.insert(0, self.data)


    def display_patient_data(self):
        for data in self.PatientTreeview.get_children():
            self.PatientTreeview.delete(data)
        i=0
        for record in (Database().display_patienten()):
            record=[record[1]] + [record[2]] + [record[4]]
            i=i+1
            if (i % 2):
                self.PatientTreeview.insert('', 'end', values=(record), tags = ('oddrow'))
            else:
                self.PatientTreeview.insert('', 'end', values=(record), tags = ('evenrow'))

    def display_leistung_data(self):
        for data in self.LeistungTreeview.get_children():
            self.LeistungTreeview.delete(data)
        i=0
        for record in (Database().display_leistungen()):
            record=[record[1]] + [record[2]]
            i=i+1
            if (i % 2):
                self.LeistungTreeview.insert('', 'end', values=(record), tags = ('oddrow'))
            else:
                self.LeistungTreeview.insert('', 'end', values=(record), tags = ('evenrow'))

    def double_click_patient(self, _event=None):
        self.select_patient_record()

    def Convert(self, string):
        lst = list(string.split(" "))
        return lst

    def select_patient_record(self):
        self.RechnungDatumE.delete(0, END)
        self.RechnungNummerE.delete(0, END)
        self.PatientNameE.delete(0, END)
        self.Geb_DataumE.delete(0, END)
        self.AnschriftE.delete(0, END)
        self.update_rechnung_nummer()
        self.update_rechnung_datum()
        selected= self.PatientTreeview.focus()
        values = self.PatientTreeview.item(selected, 'values')
        if (values):
            self.ID =''
            self.Geschlecht =''
            self.Adresse = ''
            self.Krankenversicherung = ''
            data = (
                    self.ID,
                    values[0],
                    values[1],
                    self.Geschlecht,
                    values[2],
                    self.Adresse,
                    self.Krankenversicherung,
                    )
            empty = list(filter(None, data))
            if len(empty) == 0:
                self.display_patient_data()
            else:
                for record in (Database().search_patient(data)):
                    self.Geschlecht = record[3]
                    self.Adresse = record[5]
                    self.Krankenversicherung = record [6]
            PatientName=values[0]+" "+ values[1]
            self.PatientNameE.insert(0, PatientName)
            self.Geb_DataumE.insert(0, values[2])
            self.AnschriftE.insert(0, self.Adresse)
        else:
            self.valueErrorMessage = "Bitte, ein Record wählen"
            messagebox.showerror("Value Error", self.valueErrorMessage)

    def double_click_leistung(self, _event=None):
        self.select_leistung_record()

    def select_leistung_record(self):
        if self.Leistung_count > 1:
            self.GesamtbetragL.destroy()
            self.GesamtbetragE.destroy()
            self.TextObenL.destroy()
            self.TextOben.destroy()
            self.TextUntenL.destroy()
            self.TextUnten.destroy()
            self.row +=2
            self.add_lesitung_entry()
        else:
            self.Leistung_Gesamt = str('0 €')
        self.Leistung_NameE.delete(0, END)
        self.Leistung_WertE.delete(0, END)
        self.GesamtbetragE.delete(0, END)
        selected= self.LeistungTreeview.focus()
        values = self.LeistungTreeview.item(selected, 'values')
        if (values):
            self.ID = ''
            self.WertK = ''
            self.WertP = ''
            data = (
                    self.ID,
                    values[0],
                    values[1],
                    self.WertK,
                    self.WertP,
                    )
            lst = list(data)
            empty = list(filter(None, lst))
            if len(empty) == 0:
                self.display_leistung_data()
            else:
                for record in (Database().search_leistung(lst)):
                    if self.Krankenversicherung == 'Pflichtversichert':
                        self.Leistung_Wert = record[3]
                        self.Leistung_count += 1
                    elif self.Krankenversicherung == 'Privat':
                        self.Leistung_Wert = record[4]
                        self.Leistung_count += 1
                    else:
                        self.Leistung_Wert = ''
                        messagebox.showerror("Error", "Bitte, wählen Sie zurest ein Patient Record")
            self.Leistung_Gesamt = int(self.Leistung_Gesamt.replace(' €', '')) + int(self.Leistung_Wert.replace(' €', ''))
            self.Leistung_Gesamt = str(self.Leistung_Gesamt)+' €'
            self.Leistung_NameE.insert(0, record[2])
            self.Leistung_WertE.insert(0, self.Leistung_Wert)
            self.GesamtbetragE.insert(0, self.Leistung_Gesamt)
            self.Leistungen_list.append(self.Leistung_NameE.get())

        else:
            self.valueErrorMessage = "Bitte, ein Record wählen"
            messagebox.showerror("Value Error", self.valueErrorMessage)

    def search_patient_record(self):
        for data in self.PatientTreeview.get_children():
            self.PatientTreeview.delete(data)
        self.Geb_T=str(self.Geb_T_Box.get())
        self.Geb_M=str(self.Geb_M_Box.get())
        self.Geb_Y=str(self.Geb_Y_Box.get())
        self.Geb_Datum=str(self.Geb_T + "." + self.Geb_M + "." + self.Geb_Y)
        self.ID = ''
        self.Geschlecht= ''
        self.Adresse= ''
        self.Krankenversicherung = ''
        data = (
                self.ID,
                self.Vorname.get().capitalize(),
                self.Nachname.get().capitalize(),
                self.Geschlecht,
                self.Geb_Datum,
                self.Adresse,
                self.Krankenversicherung,
                )
        lst = list(data)
        if '..' in lst :
            lst[4]= ''
        empty = list(filter(None, lst))
        if len(empty) == 0:
            self.display_patient_data()
        else:
            i = 0
            for record in (Database().search_patient(lst)):
                record=[record[1]] + [record[2]] + [record[4]]
                i=i+1
                if (i % 2):
                    self.PatientTreeview.insert('', 'end', values=(record), tags = ('oddrow'))
                else:
                    self.PatientTreeview.insert('', 'end', values=(record), tags = ('evenrow'))

        self.Vorname.delete(0, END)
        self.Nachname.delete(0, END)
        self.Geb_T_Box.delete(0, END)
        self.Geb_M_Box.delete(0, END)
        self.Geb_Y_Box.delete(0, END)

    def search_leistung_record(self):
        for data in self.LeistungTreeview.get_children():
            self.LeistungTreeview.delete(data)
        self.ID = ''
        self.WertK = ''
        self.WertP = ''
        data = (
                self.ID,
                self.Nummer.get(),
                self.Leistungname.get(),
                self.WertK,
                self.WertP,
                )
        lst = list(data)
        empty = list(filter(None, lst))
        if len(empty) == 0:
           refresh=self.display_leistung_data()
        else:
            i = 0
            for record in (Database().search_leistung(lst)):
                record=[record[1]] + [record[2]]
                i=i+1
                if (i % 2):
                    self.LeistungTreeview.insert('', 'end', values=(record), tags = ('oddrow'))
                else:
                    self.LeistungTreeview.insert('', 'end', values=(record), tags = ('evenrow'))

        self.Nummer.delete(0, END)
        self.Leistungname.delete(0, END)

    def insert_data(self):
        #from rechnungen import rechnungen, Treeview
        self.Leistungen_list=(','.join(map(str, self.Leistungen_list)))
        bezahlt = 0
        data = (
                self.RechnungNummerE.get(),
                self.PatientNameE.get(),
                self.AnschriftE.get(),
                self.Leistungen_list,
                #self.Leistung_NameE.get(),
                self.RechnungDatumE.get(),
                self.GesamtbetragE.get(),
                bezahlt,
                )
        Database().insert_rechnung(data)
        self.display_data()
        self.reset_rechnung()
        self.PatientNameE.delete(0, END)
        self.Geb_DataumE.delete(0, END)
        self.AnschriftE.delete(0, END)
        self.Leistungen_list=[]

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

    def delete_entry(self, row, column):
        Gesamt = 0
        index = int((row - 16) / 2)
        if self.Leistungen_list:
            del self.Leistungen_list[index]
            temp_list=self.Leistungen_list.copy()
            self.reset_rechnung()
            for leistung in temp_list:
                if leistung:
                    wert = self.get_leistung_info(self.PatientNameE.get(), leistung)
                    Gesamt = (int(wert.replace(' €', '')) + Gesamt)
                    if self.Leistung_count > 1:
                        self.row +=2
                        self.GesamtbetragL.destroy()
                        self.GesamtbetragE.destroy()
                        self.TextObenL.destroy()
                        self.TextOben.destroy()
                        self.TextUntenL.destroy()
                        self.TextUnten.destroy()
                        self.add_lesitung_entry()
                    self.Leistung_WertE.insert(0, wert)
                    self.Leistung_NameE.insert(0, leistung)
                    self.Leistung_count +=1

            self.GesamtbetragE.delete(0, END)
            self.GesamtbetragE.insert(0, Gesamt)
            self.Leistungen_list = temp_list
            #self.Leistungen_list.insert(index, '')
        #for col in range(3):
        #    slave = self.RechnungFrame.grid_slaves(row, col)
        #    for item in slave:
        #        item.grid_forget()
        #self.Leistung_count -= 1
        len_list = len(list(filter(None, self.Leistungen_list)))
        if len_list == 0:
            self.reset_rechnung()

    def reset_rechnung(self):
        self.row = (self.row - 30) / 2
        lst = self.RechnungFrame.grid_slaves()
        n=(len(lst) - 15)
        for l in lst[0:n]:
            l.destroy()
        self.Leistungen_list= []
        self.Leistung_count = 1
        self.row = 16
        self.add_lesitung_entry()

    def get_leistung_info(self, patient_name, leistung):
        name = list(patient_name.split(" "))
        if (name):
            lst1=('', name[0], name[1], '', '', self.AnschriftE.get(), '')
            get_patient=tuple(Database().search_patient(lst1)[0])
            lst2=('', '', leistung, '', '')
            get_leistung=tuple(Database().search_leistung(lst2)[0])
            self.leistung_nr = get_leistung[1]
            if 'Pflichtversichert' in get_patient:
                self.leistung_wert = get_leistung[3]
            elif 'Privat' in get_patient:
                self.leistung_wert =  get_leistung[4]
        return self.leistung_wert

    def pdf_generieren(self):
        self.pdf_file = default_path + "rechnung.pdf"
        self.canvas = canvas.Canvas(self.pdf_file, pagesize=A4)
        self.canvas.setFillColor(black)
        self.canvas.setLineWidth(.2)
        self.canvas.setFont('Helvetica', 8)
        self.canvas.drawString(60,750,'Muster Klinik, Muster Str 1, 1234 MusterStadt')
        self.canvas.line(60,749,220,749)
        self.canvas.setFont('Helvetica', 9)

        self.canvas.drawString(60,712, self.PatientNameE.get())

        if (self.AnschriftE.get()):
            li = list(self.AnschriftE.get().split(" ")) 
            self.Anschrift_line1 = li[0] +' '+ li[1] + ','
            self.Anschrift_line2 = li[2] +' '+ li[3]
            self.canvas.drawString(60,700, self.Anschrift_line1)
            self.canvas.drawString(60,688, self.Anschrift_line2)
        else:
            pass

        self.canvas.drawString(400,750,'Muster Klinik')
        self.canvas.drawString(400,738,'Muster Str 1')
        self.canvas.drawString(400,726,'12345 Muster Stadt')

        self.canvas.drawString(400,700,'Tel:   +49 0123456789')
        self.canvas.drawString(400,688,'Email: info@clinic.de')
        self.canvas.drawString(400,676,'Web:   www.clinic.de')

        Nr = 'Rechnung Nr.: ' + self.RechnungNummerE.get()
        self.canvas.drawString(400,640, Nr)

        datum='Datum: ' + self.RechnungDatumE.get()
        self.canvas.drawString(400,628,datum)

        datum='Leistungsdatum: ' + self.RechnungDatumE.get()
        self.canvas.drawString(60,605, datum)

        self.canvas.setLineWidth(.5)
        self.canvas.setFont('Helvetica-Bold', 18)
        self.canvas.drawString(60,620,'Rechnung')

        if (self.PatientNameE.get()):
            name = list(self.PatientNameE.get().split(" "))
            lst=('', name[0], name[1], '', '', self.AnschriftE.get(), '')
            get_patient=Database().search_patient(lst)
            if any("Weiblich" in s for s in get_patient):
                rede_name = 'Sehr geehrte Frau ' + name[1] + ','
            elif any("Männlich" in s for s in get_patient):
                rede_name = 'Sehr geehrter Herr ' + name[1] + ','
            else:
                rede_name = self.PatientNameE.get()
            self.canvas.setFont('Helvetica', 10)
            self.canvas.drawString(60,580, rede_name)

        h = 570
        self.canvas.setFont('Helvetica', 10)
        for i, line in enumerate(self.TextOben.get("1.0", END).splitlines()):
            h = h - 15
            self.canvas.drawString(60,h, line)
        
        self.canvas.setLineWidth(0.5)
        self.canvas.setFont('Helvetica-Bold', 10)

        #========= Header1 =================
        self.canvas.line(60,h-20,535,h-20)
        self.canvas.line(60,h-22,535,h-22)
        #========= Header2 =================
        self.canvas.line(60,h-20-23,535,h-20-23)
        self.canvas.line(60,h-22-23,535,h-22-23)
        self.canvas.drawString(70,h-22-23+8 ,'Nr.')
        self.canvas.drawString(150,h-22-23+8 ,'Leistung')
        self.canvas.drawString(255,h-22-23+8 ,'Leistung Nr.')
        self.canvas.drawString(330,h-22-23+8 ,'Menge')
        self.canvas.drawString(385,h-22-23+8 ,'Preis €')
        self.canvas.drawString(460,h-22-23+8 ,'Gesamt €')

        L_dict = {i:self.Leistungen_list.count(i) for i in self.Leistungen_list}
        hT = h-22-23+8-2
        x = 0

        vE = h-22-23+8-6
        vEc = h-22-23+8-6

        lH = h-22-23+8-6

        for key, value in L_dict.items():
            x  = x+1
            hT  = hT - 15
            vE = vE - 15
            lH = lH - 15 
            if x%2 == 0:
                vEc= vEc - 30
                self.gray_transparent = Color(alpha=0.1)
                self.canvas.setFillColor(self.gray_transparent)
                self.canvas.rect(60,vEc,475,15, fill=True, stroke=False)

            self.canvas.setFillColor(black)
            self.canvas.setFont('Helvetica', 8)
            self.get_leistung_info(self.PatientNameE.get(), key)
            gesamt = int(self.leistung_wert.replace(' €', '')) * value
            self.canvas.drawString(65, hT, str(x))
            self.canvas.drawString(110,hT, key)
            self.canvas.drawString(255,hT, str(self.leistung_nr))
            self.canvas.drawString(330,hT, str(value))
            self.canvas.drawString(390,hT, str(self.leistung_wert).replace(' €', ''))
            self.canvas.drawString(465,hT, str(gesamt))

            #vertikal 0
            self.canvas.line(60,vE-45,60,h-20)
            #vertikal 1
            self.canvas.line(100,vE,100,h-20)
            #vertikal 2
            self.canvas.line(250,vE,250,h-20)
            #vertikal 3
            self.canvas.line(250,vE,250,h-20)
            #vertikal 4
            self.canvas.line(320,vE,320,h-20)
            #vertikal 5
            self.canvas.line(375,vE,375,h-20)
            #vertikal 6
            self.canvas.line(425,vE,425,h-20)
            #vertikal End
            self.canvas.line(535,vE-45,535,h-20)

            #========= End =================
        self.canvas.setFont('Helvetica-Bold', 8)
        self.canvas.line(60,lH+2,535,lH+2)
        self.canvas.line(60,lH,535,lH)

        self.canvas.drawString(70,lH-13+4 ,'Summe Netto')
        self.canvas.drawString(465,lH-13+4 ,self.GesamtbetragE.get())
        self.canvas.line(60,lH-13,535,lH-13)
        self.canvas.line(60,lH-15,535,lH-15)

        self.canvas.drawString(70,lH-28+4 ,'0.0% USt.')
        self.canvas.drawString(465,lH-28+4 ,'0.0')
        self.canvas.line(60,lH-28,535,lH-28)
        self.canvas.line(60,lH-30,535,lH-30)

        self.canvas.drawString(70,lH-43+4 ,'End Summe')
        self.canvas.drawString(465,lH-43+4 ,self.GesamtbetragE.get())
        self.gray_transparent = Color(alpha=0.1)
        self.canvas.setFillColor(self.gray_transparent)
        self.canvas.rect(60,vEc-43,475,13, fill=True, stroke=False)
        self.canvas.line(60,lH-43,535,lH-43)
        self.canvas.line(60,lH-45,535,lH-45)

        self.canvas.setFillColor("Black")
        self.canvas.setFont('Helvetica', 10)
        lH = lH -45 -10
        for i, line in enumerate(self.TextUnten.get("1.0", END).splitlines()):
            if '0 €' in line:
                line = line.replace('0 €', self.GesamtbetragE.get())
            lH = lH - 15
            self.canvas.drawString(60,lH, line)



        self.gray_transparent = Color(alpha=0.3)
        self.canvas.setFillColor(self.gray_transparent)
        self.canvas.rect(60,h-43,475,21, fill=True, stroke=False)


        self.canvas.setFillColor("Black")
        self.canvas.line(60,60,535,60)
        self.canvas.setFont('Helvetica', 9)
        self.canvas.drawString(60,47,'Bankkonto: '+ self.BankverbindungE.get())

        self.canvas.save()

    def find_installed_printers(self):
        all_printers = subprocess.getoutput("lpstat -a | awk '{print $1}'").split("\n")
        default_printer = subprocess.getoutput("lpstat -d").split(": ")[1]

    def print_rechnung(self):
        self.pdf_generieren()
        if (self.Printer_ListBOX.get()):
            selected_printer = self.Printer_ListBOX.get()
        else:
            if sys.platform == "win32":
                default_printer = subprocess.getoutput("wmic printer WHERE default=TRUE get name").split("\n")
                default_printer = list(filter(None, default_printer))
                default_printer = [x.strip(' ') for x in default_printer]
                default_printer.remove("Name")
            else:
                default_printer = subprocess.getoutput("lpstat -d").split(": ")[1]
            selected_printer = default_printer[0]
        filename = default_path + "rechnung.pdf"
      
        if sys.platform == "win32":
            open (filename, "rb")
            win32api.ShellExecute (0, "print", filename, '/d:"%s"' % selected_printer, ".", 0)
        else:
            subprocess.Popen(['lpr', '-P', selected_printer, filename])


    def _bind_mouse(self, event=None):
        self.Canvas.bind_all("<4>", self._on_mousewheel)
        self.Canvas.bind_all("<5>", self._on_mousewheel)
        self.Canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.Canvas.unbind_all("<4>")
        self.Canvas.unbind_all("<5>")
        self.Canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.Canvas.xview_scroll if event.state & 1 else self.Canvas.yview_scroll
        if event.num == 4 or event.delta > 0:
            func(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            func(1, "units" )

