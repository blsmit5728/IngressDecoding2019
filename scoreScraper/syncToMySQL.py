import MySQLdb
from datetime import datetime
import json
import yaml
import sys
import os
import errno
import base64
import requests
from lxml import html
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def checkForNullFaction(database, cursor, table_name, uid, faction):
    str_command = "SELECT * FROM {} WHERE userid = \'{}\';".format(table_name,uid)
    cursor.execute(str_command)
    row = cursor.fetchone()
    if row != None:
        # we have an entry, is thier faction NULL?
        if row[5] ==  None:
            str_command = "UPDATE {} SET Faction = \'{}\' WHERE userid = \'{}\';".format(table_name, faction, uid)
            print("Executing: %s" % str_command)
            cursor.execute(str_command)
            database.commit()

def checkForExistingEntry(database, cursor,table_name,uid):
    str_command = "SELECT * FROM {} WHERE userid = \'{}\';".format(table_name,uid)
    cursor.execute(str_command)
    row = cursor.fetchone()
    if row != None:
        return False
    else:
        return True


def insertIntoDatabase(database, cursor, table, ign, solvenum, d, t, faction, verbose=False):
    uid = base64.b64encode(ign.lower().encode())
    checkForNullFaction(database, cursor, table, uid, faction)
    if checkForExistingEntry(database, cursor, table, uid):
        str_command = "INSERT INTO " + table + " VALUES (\'" + str(uid.decode()) + "\',\'" + str(solvenum) + "\',\'" + str(ign) + "\',\'" + str(d) + "\',\'" + str(t) + "\',\'" + str(faction) + "\' );"
        print("Executing: %s" % str_command)
        cursor.execute(str_command)
        database.commit()
    else:
        if verbose:
            print("Entry for: %s Exists in %s!" % (ign, table))


def getArchTypeData(db, cur, archtype, verbose=False):
    page = requests.get('https://ingress.com/decoding/%s' % archtype)
    tree = html.fromstring(page.content)
    element = tree.get_element_by_id(archtype)
    s = html.tostring(element)
    retData = []
    p = s.split("\n")
    nl = []
    for ele in p:
        if ele != "</li>":
            if "<li>" in ele:
                factionList = ele.split('"')
                faction = factionList[1]
                #nl.append(ele)
                d = strip_tags(ele)
                e = d.split(" ")
                e.append(faction)
                nl.append(e)
    indCounter = 0
    dtObjs = []
    indexList = []
    for solve in nl:
        date = solve[0]
        time = solve[1]
        time = time[:-1] # remove trailing :
        ign = solve[2]
        faction = solve[3]
        strTime = "%s %s" % (date,time)
        insertIntoDatabase(db, cur, archtype, ign, indCounter, date, time, faction, verbose)
        indCounter += 1

def getAllEntriesForArch(db, cur, archtype):
    entriesList = []
    str_command = "SELECT * from releases WHERE archname = \'{}\';".format(archtype)
    cur.execute(str_command)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            entriesList.append(row)
    return entriesList

def getDifference(db, cur, archtype):
    str_command = "SELECT * from releases WHERE archname = \'{}\';".format(archtype)
    cur.execute(str_command)
    row = cur.fetchone()
    if row != None:
        date = row[2]
        time = row[3]
        strTime = "%s %s:00" % (date,time)
        releaseTime = datetime.strptime(strTime, '%m/%d/%Y %H:%M:%S') 
        allSolvesList = getAllEntriesForArch(db, cur, archtype)
        print allSolvesList
        
        
    else:
        print "Archtype Not found in releases"
        return False

def main():
    configFilename="InternalConfig.yml"

    with open(configFilename, 'r') as yamlConfig:
        cfg = yaml.load(yamlConfig, Loader=yaml.FullLoader)


    mysql_host=cfg['database']['mysql-host']
    mysql_user=cfg['database']['mysql-user']
    mysql_pass=cfg['database']['mysql-pass']
    mysql_db=cfg['database']['mysql-db']

    db = MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,db=mysql_db)
    cur = db.cursor()

    TABLES = ["Dreamer","Interpreter","Visionary","Skeptic","Listener","Spiritualist","Humanist","Omniscient", "Explorer", "Alchemist", "Trickster", "Catalyst", "Patron"]

    for table_name in TABLES:
        str_command = "SHOW TABLES LIKE \'" + table_name + "\'"
        cur.execute(str_command)
        row = cur.fetchone()
        if row is not None:
            print("Table exists")
        else:
            print("**** %s Table not found... ****", table_name)
            str_command = "CREATE TABLE " + table_name + " (userid VARCHAR(64), solvenum INTEGER, playername VARCHAR(64), date VARCHAR(64), time VARCHAR(64), faction VARCHAR(64));"
            print("Executing: %s" % str_command)
            db = MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,db=mysql_db)
            cur = db.cursor()
            cur.execute(str_command)
            db.commit()
        
    #getDifference(db,cur,TABLES[0]);

    for arch in TABLES:
        print("Syncing: %s" % arch)
        getArchTypeData(db,cur,arch)


if __name__ == "__main__":
    main()
