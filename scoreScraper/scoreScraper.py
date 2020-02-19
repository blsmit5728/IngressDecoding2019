import requests
from lxml import html
from HTMLParser import HTMLParser
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import getopt
import sys

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

def getArchTypeData(archtype, getIgn=None):
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
        return retData.index(getIgn), len(retData)



def main():
    getIgn = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help"])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-i":
            getIgn = a
        elif o in ("-h", "--help", "help"):
            print "python scoreScraper.py [-i <ign>] --help"
            sys.exit(0)
        else:
            assert False, "unhandled exception"
    
    
    TYPES = ["Dreamer","Interpreter","Visionary","Skeptic","Listener","Spiritualist","Humanist","Omniscient", "Explorer", "Alchemist", "Trickster"]
    colors = ['b','g','r','c','m','y','k','b','g','r','c']
    
    if getIgn is not None:
        print "Decoding Challenge: 13 Archtypes Results for: " + getIgn
        for archtype in TYPES:
            
            try:
                rank, total = getArchTypeData(archtype, getIgn)
                print archtype + ": " + str(int(rank) + 1) + " of " + str(total)
            except:
                print archtype + ": Did not solve? or not updated yet"
                pass
    else:
        fig, ax = plt.subplots()
        now = datetime.utcnow()
        dt_string_now = now.strftime("Solves as of: %Y-%m-%d %H:%M:%S UTC")
        ax.set(xlabel='Time', ylabel='Solvers',title=dt_string_now)
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.grid(b=True, which='minor', color='#666666', linestyle='-')
        i = 0
        for archtype in TYPES:
            print archtype
            offsets, dtList, iList = getArchTypeData(archtype)
            ax.plot(dtList, iList, colors[i], label=archtype)
            i += 1
            
        ax.legend(loc='best')    
        plt.show()
    
if __name__ == "__main__":
    main()
