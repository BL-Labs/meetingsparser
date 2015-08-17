import csv, os

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