import csv, os

import re

class DateFinder(object):
    def __init__(self):
        self.shortmap = {'jan':'January',
                         'feb':'February',
                         'mar':'March',
                         'apr':'April',
                         'may':'May',
                         'jun':'June',
                         'jul':'July',
                         'june':'June',
                         'july':'July',
                         'aug':'August',
                         'sep':'September',
                         'sept':'September',
                         'oct':'October',
                         'nov':'November',
                         'dec':'December'}
    
    def find(self, inputtext):
        resp ={}
        for name, x in self.funclist():
            resp[name] = x(inputtext)
        return resp
    
    def funclist(self):
        return [('date_standard', self.date_standard),
                ('date_short', self.date_short)]
        
    def date_standard(self, inputtext):
        standard = "(?P<day>[0-9]+)(?:st|nd|rd|th) of (?P<month>[A-Za-z]+)"
        match = re.search(standard, inputtext, re.I|re.MULTILINE|re.U)
        if match != None:
            found = match.groupdict()
            return {'day':found['day'], 'month':found['month']}
        else:
            return
        
    def date_short(self, inputtext):
        standard = "(?P<month>[jan|feb|mar|apr|may|jun|june|jul|july|aug|sep|sept|oct|nov|dec]{3,})\.?\s+(?P<day>[0-9]{1,2})"
        match = re.search(standard, inputtext, re.I|re.MULTILINE|re.U)
        if match != None:
            found = match.groupdict()
            return {'month':self.shortmap.get(found['month'].lower(), found['month']), 'day':found['day']}
        else:
            return

def get_test_doc():
    with open("testgeoreferencedmeetings.csv", "r") as inputfile:
        doc = csv.DictReader(inputfile)
        outputlist = []
        g = 0
        for idx, row in enumerate(doc):
            if row['geolocation:latitude'] and row['geolocation:longitude']:
                g += 1
            #Add the item to the outputlist, regardless
            outputlist.append(row)
        print("Number of rows: {0} (Number with a lat/long: {1})".format(idx+1, g))
    return outputlist
    
def get_meeting_texts():
    for text in os.listdir("meetingtexts"):
        with open("meetingtexts/"+text, encoding="utf-8-sig", mode="r") as inp:
            yield inp.read()
            
def get_negative_texts():
    for text in os.listdir("negativetexts"):
        with open("negativetexts/"+text, encoding="utf-8", mode="r") as inp:
            yield inp.read()