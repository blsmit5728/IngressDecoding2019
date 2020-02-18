import requests
from lxml import html
from HTMLParser import HTMLParser
from datetime import datetime


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

def getArchTypeData(archtype):
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
    for solve in nl:
        date = solve[0]
        time = solve[1]
        time = time[:-1] # remove trailing :
        ign = solve[2]
        strTime = "%s %s" % (date,time)
        if indCounter == 0:
            firstSolve = datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')
            #print "%s %s %s" % (date, time, ign)
            retData.append((ign, 0))
        else:
            followSolve = datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S') 
            diffTimeObj = followSolve - firstSolve
            #print "%s %s %s %f" % (date, time, ign, diffTimeObj.total_seconds())
            retData.append((ign,diffTimeObj.total_seconds()))
        indCounter += 1        
    return retData





TYPES = ["Dreamer","Trickster"]



for archtype in TYPES:
    getArchTypeData(archtype)    
    
