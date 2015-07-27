import csv

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