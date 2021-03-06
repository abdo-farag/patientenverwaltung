# Patientenverwaltung_WS2021

## Gebrauchte Software

* [x] Debian (Dev Environment)
* [x] Vim (Editor)
* [x] Git (Virsion Control)
* [x] Python3
* [x] tkinter (Pytion GUI module)
* [x] Reportlab (Pytion PDF Gen module)
* [x] sqlite3 (Pytion sqlite module)
* [x] pytweening (Pytion Notification module)

## Führen Sie die Anwendung aus

#### Von Portable ausführbare Datei

[Patientenverwaltung-Linux](https://mygit.th-deg.de/af21393/patientenverwaltung_ws2021/-/raw/master/exec/linux/patientenverwaltung)\
[Patientenverwaltung-Windows.exe](https://mygit.th-deg.de/af21393/patientenverwaltung_ws2021/-/raw/master/exec/win/patientenverwaltung.exe)

#### Von den Quellcode

1- install python >=3

2- `git clone https://mygit.th-deg.de/af21393/patientenverwaltung_ws2021.git` oder download [release](https://mygit.th-deg.de/af21393/patientenverwaltung_ws2021/-/releases)

3- Requirements installieren
#### Auf  Ms Windows  Betriebssystem
innerhalb des Repository-Verzeichnisses:
```
cd  \patientenverwaltung_ws2021
pip3 install -r requirements_win.txt
```

#### Auf  Linux  Betriebssystem
```
sudo apt install python3-tk
cd patientenverwaltung_ws2021
sudo pip3 install -r requirements.txt
```

4- Application starten
```
python3 app.py
```

Hinweis: Standard Datenbank und Rechnungen Verzeichnis `~/Patientenverwaltung/`\
~ ist "Home Directory":\
Auf Windows C:\Users\USERNAME\Patientenverwaltung\
Auf Linux /home/USERNAME/Patientenverwaltung

## Package Diagramm

![](diagramme/packages_pv.svg)

## Sequence diagram

![](diagramme/sequence-diagram.svg)

## Use Case Diagram

![](diagramme/Use_Case_Diagram.svg)

## Call Diagram

![](diagramme/Opject_Call_Diagram-1.svg)

## Class Diagram

![](diagramme/classes_pv_c.svg)


## Patienten verwaltung App Überblick
![](app_images/Einloggen.png)
![](app_images/Patienten.png)
![](app_images/Leistungen.png)
![](app_images/Rechnung_Erstellen.png)
![](app_images/Rechnungen_Verwaltung.png)
![](app_images/Termine.png)
![](app_images/Users.png)

