#!/usr/bin/env python
#encoding: utf-8

import sys
from socket import *
import string
import os
import time
import signal
import random
import datetime
import sqlite3 as lite
import sys

cafe = 0
def check_cafe():
    global cafe
    if (10 == datetime.datetime.now().hour or 16 == datetime.datetime.now().hour):
        if (cafe == 0):
            cafe = 1                            
            return "no creeís que es hora de un café?"
    else:
        cafe = 0
class Sitios:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def random(self):
        try:
            self.cur.execute('SELECT * FROM Sitios ORDER BY RANDOM() LIMIT 1')
            return self.cur.fetchall()[0][1]
        except:
            return False

#    def remove(self, option):
#        sitios.remove(option)
#        self.con.commit()

    def add(self, text):
        try:
            self.cur.execute("INSERT INTO Sitios VALUES(null,'"+str(text)+"')")
            self.con.commit()
            return True
        except:
            return False

    def lista(self):
        try:
            self.cur.execute('SELECT * FROM Sitios')
            return self.cur.fetchall()
        except:
            return False

class Frases:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def random(self):
        try:
            self.cur.execute('SELECT * FROM Frases ORDER BY RANDOM() LIMIT 1')
            return self.cur.fetchall()[0][1]
        except:
            return False

def main():
    HOST = "localhost"
    PORT = int(1234)
    NICK = "Hungry"
    CHAN = "#pepito"
    PASS = ""
    con = lite.connect('hungry.db')
    frases = Frases(con)
    sitios = Sitios(con)
    print("True is correct! ;)")
    
    if (sitios.random() != False):
    	print("sitios.random: True")
    else:
    	print("sitios.random: False")
    if (sitios.add("testing db") != False):
    	print("sitios.add: True")
    else:
    	print("sitios.add: False")
    if (sitios.lista() != False):
    	print("sitios.lista: True")
    else:
    	print("sitios.lista: False")
    if (frases.random() != False):
    	print("frases.random: True")
    else:
    	print("frases.random: False")


if __name__ == "__main__":
    main()

