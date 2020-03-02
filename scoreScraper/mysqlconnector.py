import MySQLdb
from datetime import datetime
import json
import yaml
import sys
import os
import errno
import base64
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def getArchTypeDataFaction(db, cur, archtype, faction='Resistance', getIgn=None):
    entriesList = []
    str_command = "SELECT * from {} WHERE faction = \'{}\';".format(archtype, faction)
    cur.execute(str_command)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            entriesList.append(row)
    indCounter = 0
    dtObjs = []
    indexList = []
    retData = []
    for solve in entriesList:
        date = solve[3]
        time = solve[4]        
        ign = solve[2]
        strTime = "%s %s" % (date,time)
        if indCounter == 0:
            firstSolve = datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')
            #print "%s %s %s" % (date, time, ign)
            retData.append(ign)
            dtObjs.append(firstSolve)
            indexList.append(0)
        else:
            followSolve = datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S') 
            diffTimeObj = followSolve - firstSolve
            #print "%s %s %s %f" % (date, time, ign, diffTimeObj.total_seconds())
            retData.append(ign)
            dtObjs.append(followSolve)
            indexList.append(indCounter)
        indCounter += 1   
    if getIgn is None:
        return retData,dtObjs,indexList
    else:
        return retData.index(getIgn), len(retData), dtObjs[retData.index(getIgn)],dtObjs,indexList



def getArchTypeData(db, cur, archtype, getIgn=None):
    entriesList = []
    str_command = "SELECT * from {};".format(archtype)
    cur.execute(str_command)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            entriesList.append(row)
    indCounter = 0
    dtObjs = []
    indexList = []
    retData = []
    for solve in entriesList:
        date = solve[3]
        time = solve[4]        
        ign = solve[2]
        strTime = "%s %s" % (date,time)
        if indCounter == 0:
            firstSolve = datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')
            #print "%s %s %s" % (date, time, ign)
            retData.append(ign)
            dtObjs.append(firstSolve)
            indexList.append(0)
        else:
            followSolve = datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S') 
            diffTimeObj = followSolve - firstSolve
            #print "%s %s %s %f" % (date, time, ign, diffTimeObj.total_seconds())
            retData.append(ign)
            dtObjs.append(followSolve)
            indexList.append(indCounter)
        indCounter += 1   
    if getIgn is None:
        return retData,dtObjs,indexList
    else:
        return retData.index(getIgn), len(retData), dtObjs[retData.index(getIgn)],dtObjs,indexList

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


def plotArchTypes(xDataList, yDataList, archTypeList, markerx=None, markery=None, ign=None, autoSave=False, faction=None):
    colors = ['b','g','r','c','m','y','k','b','g','r','c','m']#,'y']
    fig, ax = plt.subplots(figsize=(16.0,9.0))
    now = datetime.utcnow()
    dt_string_now = now.strftime("Solves as of: %Y-%m-%d %H:%M:%S UTC")
    if ign is not None:
        dt_string_now = dt_string_now + " for Agent: " + ign
    ax.set(xlabel='Time', ylabel='Solvers',title=dt_string_now)
    ax.minorticks_on()
    ax.grid(b=True, which='major', color='#666666', linestyle='-')
    ax.grid(b=True, which='minor', color='#666666', linestyle=':')

    listLen = len(xDataList)
    legList = []
    for l in range(0, listLen):
        #print archTypeList[l]
        ax.plot(xDataList[l], yDataList[l], colors[l], label=archTypeList[l])
        if markerx is not None and markery is not None:
            a = ax.plot(markerx[l], markery[l], marker='o', color=colors[l])
            legList.append(a)
    h,l = ax.get_legend_handles_labels()
    #ax.legend(h,l, loc=(1.04,0.5))
    ax.legend(h,l, loc='best')
    if autoSave:
        now = datetime.utcnow()
        dt_string_now = now.strftime("Solves_%Y-%m-%d_%H-%M-%S_UTC")
        if ign is not None:
            dt_string_now = dt_string_now + "_" + ign
        if faction is not None:
            saveName = dt_string_now + "_" + faction + "_" + ".png"
        else:
            saveName = dt_string_now + ".png"
        fig.savefig(saveName)
        return saveName
    else:
        plt.show()

def getGraph(ign=None,faction=None,archetype=None):
    configFilename="InternalConfig.yml"
    TABLES = ["Dreamer","Interpreter","Visionary","Skeptic","Listener","Spiritualist","Humanist","Omniscient", "Explorer", "Alchemist", "Trickster", "Catalyst"]#, "Patron"]
    with open(configFilename, 'r') as yamlConfig:
        cfg = yaml.load(yamlConfig, Loader=yaml.FullLoader)
    mysql_host=cfg['database']['mysql-host']
    mysql_user=cfg['database']['mysql-user']
    mysql_pass=cfg['database']['mysql-pass']
    mysql_db=cfg['database']['mysql-db']

    db = MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,db=mysql_db)
    cur = db.cursor()
    xDList = []
    yDList = []
    i = 0
    for arch in TABLES:
        if faction is not None:
            offsets, dtList, iList = getArchTypeDataFaction(db, cur, arch, faction)
        else:
            offsets, dtList, iList = getArchTypeData(db, cur, arch)
        xDList.append(dtList)
        yDList.append(iList)
        i += 1
    if faction is not None:
        plotArchTypes(xDList,yDList,TABLES,autoSave=True, faction=faction)
    return plotArchTypes(xDList,yDList,TABLES,autoSave=True)
