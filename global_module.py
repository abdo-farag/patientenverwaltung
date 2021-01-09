import os, sys



active_user = None
salt = b'$2b$12$4yhmJUT2gnVlA1gaKQB1Qu'
rech_nummer = None

# default Database
Database        = 'SQLite'

# Mysql Connection
MYSQL_USER      = 'root'
MYSQL_PASSWORD  = 'root'
MYSQL_HOST      = 'localhost'
MYSQL_PORT      = 3306
DATABASE_NAME   = 'pv'

default_path    = os.path.expanduser('~') + '/Patientenverwaltung/'
