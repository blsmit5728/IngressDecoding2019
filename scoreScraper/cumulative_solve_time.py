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
import getopt
import time


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


def checkForExistingEntry(database, cursor,table_name,uid):
    str_command = "SELECT * FROM {} WHERE userid = \'{}\';".format(table_name,uid)
    cursor.execute(str_command)
    row = cursor.fetchone()
    if row != None:
        return False
    else:
        return True


def insertIntoDatabase(database, cursor, table, ign, solvenum, d, t, verbose=False):
    uid = base64.b64encode(ign.lower().encode())
    if checkForExistingEntry(database, cursor, table, uid):
        str_command = "INSERT INTO " + table + " VALUES (\'" + str(uid.decode()) + "\',\'" + str(solvenum) + "\',\'" + str(ign) + "\',\'" + str(d) + "\',\'" + str(t) + "\');"
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
                #nl.append(ele)
                d = strip_tags(ele)
                nl.append(d.split(" "))
    indCounter = 0
    dtObjs = []
    indexList = []
    for solve in nl:
        date = solve[0]
        time = solve[1]
        time = time[:-1] # remove trailing :
        ign = solve[2]
        strTime = "%s %s" % (date,time)
        insertIntoDatabase(db, cur, archtype, ign, indCounter, date, time, verbose)
        indCounter += 1

def getAllEntriesForArch(db, cur, archtype):
    entriesList = []
    str_command = "SELECT * from {};".format(archtype)
    cur.execute(str_command)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            entriesList.append(row)
    return entriesList

def getSolverEntryForArch(db, cur, archtype, solver):
    entriesList = []
    str_command = "SELECT * from {} WHERE LOWER(playername) = \'{}\';".format(archtype, solver.lower())
    cur.execute(str_command)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            entriesList.append(row)
    return entriesList


def getDifference(db, cur, archtype, solver=None):
    str_command = "SELECT * from releases WHERE archname = \'{}\';".format(archtype)
    cur.execute(str_command)
    row = cur.fetchone()
    solverTimes = []
    if row != None:
        date = row[2]
        time = row[3] + ":00"
        strTime = "%s %s" % (date.replace('/','-'),time)
        releaseTime = datetime.strptime(strTime, '%m-%d-%Y %H:%M:%S') 
        if solver is None:
            allSolvesList = getAllEntriesForArch(db, cur, archtype)
        else:
            allSolvesList = getSolverEntryForArch(db, cur, archtype, solver)
        for entry in allSolvesList:
            #print entry
            solveTimeStr = "%s %s" % (entry[3],entry[4])
            solveTimeObj = datetime.strptime(solveTimeStr, '%Y-%m-%d %H:%M:%S')
            diffTimeObj = solveTimeObj - releaseTime
            if solver is not None:
                return "%s solved %s in %f seconds" % (solver, archtype, diffTimeObj.total_seconds())
            else:
                name = (entry[2])
                solverTimes.append( (name, diffTimeObj.total_seconds()) )
            #print "%f" % (diffTimeObj.total_seconds()) 
        return solverTimes
    else:
        print "Archtype Not found in releases"
        return False


def sortAllSolves(tup):  
    # reverse = None (Sorts in Ascending order)  
    # key is set to sort using second element of  
    # sublist lambda has been used  
    return(sorted(tup, key = lambda x: x[2]))   
       
        
def main():
    configFilename="InternalConfig.yml"
    
    getIgn = None
    autoSave = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:s", ["help"])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-i":
            getIgn = a
        elif o in ("-h", "--help", "help"):
            print "python solveTimes.py [-i <ign>] --help"
            sys.exit(0)
        elif o == "-s":
            autoSave = True
        else:
            assert False, "unhandled exception"

    with open(configFilename, 'r') as yamlConfig:
        cfg = yaml.load(yamlConfig, Loader=yaml.FullLoader)


    mysql_host=cfg['database']['mysql-host']
    mysql_user=cfg['database']['mysql-user']
    mysql_pass=cfg['database']['mysql-pass']
    mysql_db=cfg['database']['mysql-db']

    db = MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,db=mysql_db)
    cur = db.cursor()

    TABLES = ["Dreamer","Interpreter","Visionary","Skeptic","Listener","Spiritualist","Humanist","Omniscient", "Explorer", "Alchemist", "Trickster", "Catalyst", "Patron"]

    #for table_name in TABLES:
    #    str_command = "SHOW TABLES LIKE \'" + table_name + "\'"
    #    cur.execute(str_command)
    #    row = cur.fetchone()
    #    if row is not None:
    #        print("Table exists")
    #    else:
    #        print("**** %s Table not found... ****", table_name)
    #        str_command = "CREATE TABLE " + table_name + " (userid VARCHAR(64), solvenum INTEGER, playername VARCHAR(64), date VARCHAR(64), time VARCHAR(64));"
    #        print("Executing: %s" % str_command)
    #        db = MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,db=mysql_db)
    #        cur = db.cursor()
    #        cur.execute(str_command)
    #        db.commit()
        
    storeLISTS = []
    for table_name in TABLES:
        if getIgn is None:
            storeLISTS.append(getDifference(db,cur,table_name,solver=getIgn))
        else:
            print getDifference(db,cur,table_name,solver=getIgn)
            
    ALLSOLVES = []
    archCount = 0
    for arch in storeLISTS:
        for entry in arch:
            newEntry = (TABLES[archCount], entry[0], entry[1])
            #print newEntry
            ALLSOLVES.append(newEntry)
        archCount += 1
    
    ARCH_SOLVES_SORTED = sortAllSolves(ALLSOLVES)
    
    for i in range(0,100):
        timeToSolve = time.strftime("%H:%M:%S", time.gmtime(ARCH_SOLVES_SORTED[i][2]))
        print "#%03d : %s Solved %s in %f seconds (%s)" % (i,ARCH_SOLVES_SORTED[i][1], ARCH_SOLVES_SORTED[i][0], ARCH_SOLVES_SORTED[i][2], timeToSolve)
        
    
                
            
'''
    for arch in TABLES:
        print("Syncing: %s" % arch)
        getArchTypeData(db,cur,arch)
'''

if __name__ == "__main__":
    main()

