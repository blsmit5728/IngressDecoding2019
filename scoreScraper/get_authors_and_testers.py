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

def getData(archtype, getIgn=None):
    page = requests.get('https://ingress.com/decoding/%s' % (archtype))
    tree = html.fromstring(page.content)
    site = tree.get_element_by_id(archtype)
    s = html.tostring(site)
    p = s.split("\n")
    for ele in p:
        a = strip_tags(ele)
        if "<li>" in ele:
            b = ele.split('"')
            print b[1]
        #print a
        #print ele.split("\"")
        #if "en/discussion/" in ele:
        #    print ele
        #if "Written by" in ele:
        #    print ele
        #if "Tested" in ele:
        #    print ele


getData("Catalyst")
