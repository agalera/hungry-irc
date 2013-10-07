#!/usr/bin/env python
#encoding: utf-8

import sys
from socket import *
import string
import os
import time
import popen2
import signal
import random
import datetime
global cafe = 0
import sqlite3 as lite
import sys

def daemonize():
    pid = os.fork()
    if(pid != 0):
        os._exit(0)
def check_cafe():
    global cafe
    if (10 == datetime.datetime.now().hour or 16 == datetime.datetime.now().hour):
        if (cafe == 0):
            cafe = 1                            
            return "no creeís que es hora de un café?"
    else:
        cafe = 0
    return False
class Sitios:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def random(self):
        self.cur.execute('SELECT * FROM Sitios ORDER BY RANDOM() LIMIT 1')
        return self.cur.fetchall()[0][1]

#    def remove(self, option):
#        sitios.remove(option)
#        self.con.commit()

    def add(self, text):
        self.cur.execute("INSERT INTO Sitios VALUES("",'"+str(text)+"')")
        self.con.commit()

    def lista(self):
        self.cur.execute('SELECT * FROM Sitios')
        return self.cur.fetchall()

class Frases:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def random(self):
        self.cur.execute('SELECT * FROM Frases ORDER BY RANDOM() LIMIT 1')
        return self.cur.fetchall()[0][1]

def main():
    HOST = "localhost"
    PORT = int(1234)
    NICK = "Hungry"
    CHAN = "#pepito"
    PASS = ""
    con = lite.connect('hungry.db')
    frases = Frases(con)
    sitios = Sitios(con)

    print "[+] Connecting to %s@%s:%s (chan:%s)" % ( NICK, HOST, PORT,CHAN )
    print "[+] Done.."
    contador = 0
    readbuffer = ""

    s = socket( )

    try:
        s.connect((HOST, PORT))
    except:
        print "[-] Couldn't connect to %s:%s" % (HOST, PORT)
        sys.exit(1)

    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (NICK , NICK, NICK))

    if len(PASS) != 0:
        s.send("JOIN %s %s\r\n" % (CHAN, PASS))
    else:
        s.send("JOIN %s\r\n" % (CHAN))

    while 1:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop()
        for line in temp:
            line=string.rstrip(line)
            line=string.split(line)
            if(line[0]=="PING"):
                s.send("PONG %s\r\n" % line[1])
                if (contador == 10):
                    if (9 > datetime.datetime.now().hour and 18 < datetime.datetime.now().hour):
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, frases.random()))
                    contador = 0
                else:
                    contador += 1
                    tmp = check_cafe()
                    if (tmp != False)
                    s.send("PRIVMSG %s :%s\r\n" % (CHAN, tmp))

            elif line[1] == "JOIN":
                name = str(line[0].split("!")[0])
                s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "Welcome ",name.replace(":","") , "!!"))
            elif line[1] == "QUIT":
                name = str(line[0].split("!")[0])
                s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "Bye ",name.replace(":","") , "!!"))
            else:
                try:
                    if line[3] == ":!frase":
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, frases.random()))
                    if line[3] == ":!help":
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Displayinglist of commands the bot understands"))
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !comer return one random value to list 'sitios'"))
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !comer_lista return list 'sitios'"))
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !add_site append value to list 'sitios'"))
                        #s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !delete_site remove value to list 'sitios'"))
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !frase return one random value to list 'frases'"))
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] !die    -die!!"))
                    if line[3] == ":!comer":
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, sitios.random()))
                    if line[3] == ":!comer_lista":
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, sitios.lista()))
                    if line[3] == ":!add_site":
                        temp = []
                        temp2 = []
                        for lines in line:
                            temp.append(lines)
                            if len(temp) > 4:
                                temp2.append(lines)
                        option = ' '.join(temp2)
                        sitios.add(option)
                        s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[+] Add \"", option, "\""))

                    #if line[3] == ":!delete_site":
                    #    try:
                    #        temp = []
                    #        temp2 = []
                    #        for lines in line:
                    #            temp.append(lines)
                    #            if len(temp) > 4:
                    #                temp2.append(lines)
                    #        option = ' '.join(temp2)
                    #        sitios.remove(option)
                    #        s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[-] Remove \"", option, "\""))
                    #    except:
                    #        s.send("PRIVMSG %s :%s%s%s\r\n" % (CHAN, "[-] Remove fail! \"", option, "\""))

                    if line[3] == ":!die":
                        if (line[0] == ":Pepito!~pepito@192.168.0.80"):
                            s.send("PRIVMSG %s :%s\r\n" % (CHAN, "[+] Killing me.."))
                            myproc = popen2.Popen3("")
                            pgid = os.getpgid(myproc.pid)
                            os.killpg(pgid, signal.SIGKILL)
                except:
                    for error in sys.exc_info():
                        s.send("PRIVMSG %s :%s\r\n" % (CHAN, error))
                    s.send("PRIVMSG %s :%s\r\n" % (CHAN, line))
                    s.send("PRIVMSG %s :%s\r\n" % (CHAN, "Me he roto por dentro"))

if __name__ == "__main__":
    daemonize()
    main()
