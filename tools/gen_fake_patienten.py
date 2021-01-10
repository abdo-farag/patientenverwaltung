#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from faker import Faker
import random
from datetime import datetime
import sys
import locale
import csv


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
fake = Faker('de_DE')

def date_checker(date):
    try:
        datetime.strptime(date, "%d.%B.%Y")
        return date
    except Exception:
        day = fake.day_of_month()
        month = fake.month_name()
        year = fake.year()
        date = day + "." + month +"." + year
        return date_checker(date)

def ff_name_check(f_name):
    match=['-', ' ']
    if any(x in f_name for x in match):
        f_name= fake.first_name_female()
        return ff_name_check(f_name)
    else:
        return f_name

def mf_name_check(f_name):
    match=['-', ' ']
    if any(x in f_name for x in match):
        f_name= fake.first_name_male()
        return mf_name_check(f_name)
    else:
        return f_name

def l_name_check(l_name):
    match=['-', ' ']
    if any(x in l_name for x in match):
        l_name= fake.last_name()
        return l_name_check(l_name)
    else:
        return l_name

def female():
    versicherung = ('Privat', 'Pflichtversichert')
    ver = random.choice(versicherung)
    f_name= mf_name_check(fake.first_name_female())
    l_name= l_name_check(fake.last_name())
    street = fake.street_name()
    city = fake.city()
    address =  fake.address()
    address = address.replace('\n',' ')
    day = fake.day_of_month()
    month = fake.month_name()
    year = fake.year()
    date = day + "." + month +"." + year
    date = date_checker(date)
    iD=str(y)
    data = iD +","+ f_name +","+l_name +","+'Weiblich'+","+ date +","+address +","+ ver
    data_lst = data.split(",")
    return data_lst


def male():
    versicherung = ('Privat', 'Pflichtversichert')
    ver = random.choice(versicherung)
    f_name= mf_name_check(fake.first_name_male())
    l_name= l_name_check(fake.last_name())
    street = fake.street_name()
    city = fake.city()
    address =  fake.address()
    address = address.replace('\n',' ')
    day = fake.day_of_month()
    month = fake.month_name()
    year = fake.year()
    date = day + "." + month +"." + year
    date = date_checker(date)
    iD=str(x)
    data = iD +","+ f_name +","+l_name +","+'Männlich'+","+ date +","+address +","+ ver
    data_lst = data.split(",")
    return data_lst


with open('fake_data.csv', 'a', newline='', encoding="utf-8") as fake_data:
    write = csv.writer(fake_data, dialect='excel')
    x,y = 1,2
    for i in range(500):
        male_data=male()
        female_data=female()
        write.writerow(male_data)
        write.writerow(female_data)
        x = x + 2
        y = y + 2
