# Importing Important Libraries

import sqlite3
import bcrypt
import sys
import global_module
from pathlib import Path

MYSQL_USER      = global_module.MYSQL_USER
MYSQL_PASSWORD  = global_module.MYSQL_PASSWORD
MYSQL_HOST      = global_module.MYSQL_HOST
MYSQL_PORT      = global_module.MYSQL_PORT
DATABASE_NAME   = global_module.DATABASE_NAME

default_path = global_module.default_path
Path(default_path).mkdir(parents=True, exist_ok=True)

class Database:
    '''
        Database Class for sqlite3
        :params conn - sqlite3Connection
        :params curr - cursor
    '''
    def __init__(self):
        try:
            if global_module.Database == 'SQLite':
                db_path = default_path + 'pv.db'
                self.conn = sqlite3.connect(db_path)
            self.curr = self.conn.cursor()
        except:
            sys.exit() #print("Failed")

    def check_tables(self, table):
        self.check = 'SELECT count(*) FROM' +' '+ table + ';'
        #self.check='''SELECT count(*) FROM (select 0 from sqlite_master WHERE type='table' AND name=? limit 1)'''
        self.curr.execute(self.check)
        res = [x[0] for x in self.curr.fetchall()]
        if res[0] == 0:
            return 0
        else:
            return 1


    def createTable(self):

        '''
            Method for Creating Table in Database
        '''
        create_table_users = '''
            CREATE TABLE IF NOT EXISTS users(
                id Integer PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                isActive BOOLEAN
            );
        '''
        create_table_patienten = ''' 
            CREATE TABLE IF NOT EXISTS patienten(
                id Integer PRIMARY KEY AUTOINCREMENT,
                v_name TEXT NOT NULL, 
                n_name TEXT NOT NULL,
                geschlecht TEXT NOT NULL, 
                geb_datum TEXT NOT NULL, 
                address TEXT NOT NULL, 
                versicherung TEXT NOT NULL
                );
            '''
        create_table_leistungen = '''
            CREATE TABLE IF NOT EXISTS leistungen(
                id Integer PRIMARY KEY AUTOINCREMENT,
                nummer TEXT NOT NULL,
                leistung_name TEXT NOT NULL,
                wert_kassen TEXT NOT NULL,
                wert_privat TEXT NOT NULL
                );
            '''

        create_table_rechnungen = '''
            CREATE TABLE IF NOT EXISTS rechnungen(
                id Integer PRIMARY KEY AUTOINCREMENT,
                nummer TEXT NOT NULL,
                patient TEXT NOT NULL,
                anschrift TEXT NOT NULL,
                leistung_name TEXT NOT NULL,
                datum TEXT NOT NULL,
                gesamtbetrag TEXT NOT NULL,
                bezahlt BOOLEAN
                );
            '''
        create_table_termine = '''
            CREATE TABLE IF NOT EXISTS termine(
                id Integer PRIMARY KEY AUTOINCREMENT,
                patient TEXT NOT NULL,
                tel_nr INT NOT NULL,
                termin TEXT NOT NULL,
                tag TEXT NOT NULL,
                datum TEXT NOT NULL,
                zweck TEXT,
                notizen TEXT
                );
            '''
        create_table_settings = '''
            CREATE TABLE IF NOT EXISTS settings(
                id Integer PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value INT NOT NULL
                );
            '''

        self.curr.execute(create_table_users)
        self.curr.execute(create_table_patienten)
        self.curr.execute(create_table_leistungen)
        self.curr.execute(create_table_rechnungen)
        self.curr.execute(create_table_termine)
        self.curr.execute(create_table_settings)
        self.conn.commit()

    def insert_setting(self, data):
        insert_data = """
            INSERT INTO settings(key, value)
            VALUES(?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()

    def update_setting(self, data):
        update_data = """
            UPDATE settings SET value=? WHERE key=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()

    def get_setting(self, data):
        get_data = """
            SELECT * FROM settings WHERE key = (?);
        """

        self.curr.execute(get_data, data)
        records = self.curr.fetchall()
        return records



    def insert_user(self, data):

        '''
            Method for Insertig Data in Table in Database
        '''

        insert_data = """
            INSERT INTO users(username, password, role, isActive)
            VALUES(?, ?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()

    def search_user(self, data):

        '''
            Method for Searching Data in Table in Database
        '''

        search_data = '''
            SELECT * FROM users WHERE username = (?);
        '''

        self.curr.execute(search_data, data)

        rows = self.curr.fetchall()

        if rows == []:
            return False
        else:
            return True

    def validate_user(self, data, inputData):
        validate_data = """
            SELECT * FROM users WHERE username = (?);
        """

        self.curr.execute(validate_data, data)
        row = self.curr.fetchall()
        if not row:
            pass
        else:
            if row[0][1] == inputData[0]:
                return row[0][2] == bcrypt.hashpw(inputData[1].encode(), row[0][2])

    def display_users(self):
        self.curr.execute("SELECT * FROM users")
        records = self.curr.fetchall()
        return records

    def delete_user(self, data):
        delete_data = """
            DELETE FROM users WHERE id =?
        """
        self.curr.execute(delete_data, data)
        self.conn.commit()

    def update_user(self, data):
        update_data = """
            UPDATE users SET username=?, password=?, role=?, isActive=? WHERE id=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()


    def update_user_password(self, data):
        update_data = """
            UPDATE users SET password=? WHERE username=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()

    def get_user_role(self, data):
        get_data = """
            SELECT role from users WHERE username=?
        """
        self.curr.execute(get_data, data)
        role = self.curr.fetchall()
        return role

    def set_user_active(self, data):
        update_data = """
            UPDATE users SET isActive=? WHERE username=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()


    def is_user_Active(self):
        is_Active = """
            SELECT isActive FROM users WHERE username = (?);
        """
        if is_Active == 1:
            return True
        else:
            return False


    def delete_patienten_table(self):
        self.curr.execute('''DROP TABLE patienten;''')
        self.createTable()
        self.conn.commit()

    def delete_leistungen_table(self):
        self.curr.execute('''DROP TABLE leistungen;''')
        self.createTable()
        self.conn.commit()

    def delete_rechnungen_table(self):
        self.curr.execute('''DROP TABLE rechnungen;''')
        self.createTable()
        self.conn.commit()

    def delete_termine_table(self):
        self.curr.execute('''DROP TABLE termine;''')
        self.createTable()
        self.conn.commit()


    def insert_patient(self, data):
        insert_data = """
            INSERT INTO patienten(v_name, n_name, geschlecht, geb_datum, address, versicherung)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()

    def insert_leistung(self, data):
        insert_data = """
            INSERT INTO leistungen(nummer, leistung_name, wert_kassen, wert_privat)
            VALUES (?, ?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()


    def insert_rechnung(self, data):
        insert_data = """
            INSERT INTO rechnungen(nummer, patient, anschrift, leistung_name, datum , gesamtbetrag, bezahlt)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()

    def insert_termin(self, data):
        insert_data = """
            INSERT INTO termine(patient, tel_nr, termin, tag, datum , zweck, notizen)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()


    def display_patienten(self):
        self.curr.execute("SELECT * FROM patienten")
        records = self.curr.fetchall()
        return records

    def display_leistungen(self):
        self.curr.execute("SELECT * FROM leistungen")
        records = self.curr.fetchall()
        return records

    def display_rechnungen(self):
        self.curr.execute("SELECT * FROM rechnungen")
        records = self.curr.fetchall()
        return records

    def display_termine(self):
        self.curr.execute("SELECT * FROM termine")
        records = self.curr.fetchall()
        return records


    def update_patient(self, data):
        update_data = """
            UPDATE patienten SET v_name=?, n_name=?, geschlecht=?, geb_datum=?, address=?, versicherung=? WHERE id=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()

    def update_leistung(self, data):
        update_data = """
            UPDATE leistungen SET nummer=?, leistung_name=?, wert_kassen=?, wert_privat=? WHERE id=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()

    def update_rechnung(self, data):
        update_data = """
            UPDATE rechnungen SET nummer=?, patient=?, anschrift=?, leistung_name=?, datum=?, gesamtbetrag=?, bezahlt=? WHERE id=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()

    def update_termin(self, data):
        update_data = """
            UPDATE termine SET patient=?, tel_nr=?, termin=?, Tag=?, datum=?, zweck=?, notizen=? WHERE id=?
        """
        self.curr.execute(update_data, data)
        self.conn.commit()


    def delete_patient(self, data):
        delete_data = """
            DELETE FROM patienten WHERE id =?
        """
        self.curr.execute(delete_data, data)
        self.conn.commit()

    def delete_leistung(self, data):
        delete_data = """
            DELETE FROM leistungen WHERE id =?
        """
        self.curr.execute(delete_data, data)
        self.conn.commit()

    def delete_rechnung(self, data):
        delete_data = """
            DELETE FROM rechnungen WHERE id =?
        """
        self.curr.execute(delete_data, data)
        self.conn.commit()

    def delete_termin(self, data):
        delete_data = """
            DELETE FROM termine WHERE id =?
        """
        self.curr.execute(delete_data, data)
        self.conn.commit()


    def search_patient(self, data):
        '''
        Method for Searching Data in Table in Database
        '''
        new_data=data
        com0, com1, com2, com3, com4, com5, com6='', '', '', '', '', '', ''
        if data[0]:
            com0="(id = (?))"
        else:
            new_data = list(filter(None, data))

        if data[1]:
            com1="(v_name = (?))"
        else:
            new_data = list(filter(None, data))

        if data[2]:
            com2="(n_name = (?))"
        else:
            new_data = list(filter(None, data))

        if data[3]:
            com3="(geschlecht = (?))"
        else:
            new_data = list(filter(None, data))

        if data[4]:
            com4="(geb_datum = (?))"
        else:
            new_data = list(filter(None, data))

        if data[5]:
            com5="(address = (?))"
        else:
            new_data = list(filter(None, data))

        if data[6]:
            com6="(versicherung = (?))"
        else:
            new_data = list(filter(None, data))

        com=[com0, com1, com2, com3, com4, com5, com6]
        #com = [w.replace(' ', '') for w in com]
        com = list(filter(None, com))
        s=' AND '
        com=s.join(com)
        command="SELECT * FROM patienten WHERE" + " " + com + ";"
        self.curr.execute(command, new_data)
        rows = self.curr.fetchall()
        return rows

    def search_leistung(self, data):
        '''
        Method for Searching Data in Table in Database
        '''
        new_data=data
        com0, com1, com2, com3, com4='', '', '', '', ''
        if data[0]:
            com0="(id = (?))"
        else:
            new_data = list(filter(None, data))

        if data[1]:
            com1="(nummer = (?))"
        else:
            new_data = list(filter(None, data))

        if data[2]:
            com2="(leistung_name = (?))"
        else:
            new_data = list(filter(None, data))

        if data[3]:
            com3="(wert_kassen = (?))"
        else:
            new_data = list(filter(None, data))

        if data[4]:
            com4="(wert_privat = (?))"
        else:
            new_data = list(filter(None, data))

        com=[com0, com1, com2, com3, com4]
        com = list(filter(None, com))
        s=' AND '
        com=s.join(com)
        command="SELECT * FROM leistungen WHERE" + " " + com + ";"
        self.curr.execute(command, new_data)
        rows = self.curr.fetchall()
        return rows

    def search_rechnung(self, data):
        '''
        Method for Searching Data in Table in Database
        '''
        new_data=data
        com0, com1, com2, com3, com4, com5, com6, com7='', '', '', '', '', '', '', ''
        if data[0]:
            com0="(id = (?))"
        else:
            new_data = list(filter(None, data))

        if data[1]:
            com1="(nummer = (?))"
        else:
            new_data = list(filter(None, data))

        if data[2]:
            com2="(patient = (?))"
        else:
            new_data = list(filter(None, data))

        if data[3]:
            com3="(anschrift = (?))"
        else:
            new_data = list(filter(None, data))

        if data[4]:
            com4="(leistung_name = (?))"
        else:
            new_data = list(filter(None, data))

        if data[5]:
            com5="(datum = (?))"
        else:
            new_data = list(filter(None, data))

        if data[6]:
            com6="(gesamtbetrag = (?))"
        else:
            new_data = list(filter(None, data))

        if data[7]:
            com7="(bezahlt = (?))"
        else:
            new_data = list(filter(None, data))


        com=[com0, com1, com2, com3, com4, com5, com6, com7]
        com = list(filter(None, com))
        s=' AND '
        com=s.join(com)
        command="SELECT * FROM rechnungen WHERE" + " " + com + ";"
        self.curr.execute(command, new_data)
        rows = self.curr.fetchall()
        return rows

    def search_termin(self, data):
        new_data=data
        com0, com1, com2, com3, com4, com5, com6, com7='', '', '', '', '', '', '', ''
        if data[0]:
            com0="(id = (?))"
        else:
            new_data = list(filter(None, data))

        if data[1]:
            com1="(patient = (?))"
        else:
            new_data = list(filter(None, data))

        if data[2]:
            com2="(tel_nr = (?))"
        else:
            new_data = list(filter(None, data))

        if data[3]:
            com3="(termin = (?))"
        else:
            new_data = list(filter(None, data))

        if data[4]:
            com4="(tag = (?))"
        else:
            new_data = list(filter(None, data))
        if data[5]:
            com5="(datum = (?))"
        else:
            new_data = list(filter(None, data))

        if data[6]:
            com6="(zweck = (?))"
        else:
            new_data = list(filter(None, data))

        if data[7]:
            com7="(notizen = (?))"
        else:
            new_data = list(filter(None, data))


        com=[com0, com1, com2, com3, com4, com5, com6, com7]
        com = list(filter(None, com))
        s=' AND '
        com=s.join(com)
        command="SELECT * FROM termine WHERE" + " " + com + ";"
        self.curr.execute(command, new_data)
        rows = self.curr.fetchall()
        return rows


    def get_last_nummer_rechnung(self):
        command= '''
            SELECT nummer FROM rechnungen ORDER BY ID DESC LIMIT 1;
            '''
        self.curr.execute(command)
        return self.curr.fetchall()


    def get_last_nummer(self):
        command= '''
            SELECT nummer FROM leistungen ORDER BY ID DESC LIMIT 1;
            '''
        self.curr.execute(command)
        return self.curr.fetchall()
