import csv, string, os, re

MDFILE = "metadataNorthernStar.csv"
OCRFOLDER = "Northern Star 1841 OCR text forthcoming meetings\TEXT FILES"
FINALCSV = "outputgeo27july2015.csv"

HEADERS = ["NewspaperText", "Date of meeting", "Place","Longitude", "Latitude", "Newspaper", "Date"]

#load and process gazetteer
gazdict={}
gaz = open("Gazetters/NS_gazetteer.csv","rb")
linenum = 0
p=re.compile(',\ *(-?[0-9.]*),\ *(-?[0-9.]*)')
for binline in gaz:
    print(linenum)
    # convert byteline to characters
    line = str( binline, encoding = "cp1252")
    (place, fullplace, longlat) = line[1:-3].split('""')
    rematch = p.match(longlat)
    linenum+=1
    if rematch:
        lng = p.match(longlat).group(1)
        lat = p.match(longlat).group(2)
        try:
            if float(lng)>58 or float(lng)<50 or float(lat)>4 or float(lat)<-6:
                print("{0} (line {1}) looks well-dodgy longlat wise".format(linenum, place))
            gazdict[place[:-1]]=(lng, lat)
        except ValueError as e:
            print("Error parsing lat/long from line: {0}".format(linenum))
    else:
        print("Error in gazetteer line {0}: {1}. Skipping".format(linenum, line))


def get_place(meeting_txt):
    return string.capwords(meeting_txt.split(".")[0].lower())

with open(FINALCSV, "wt") as final:
    finalcsv = csv.writer(final)
    finalcsv.writerow(HEADERS)
    with open(MDFILE, "rt") as mdfile:
        mdcsv = csv.DictReader(mdfile)
        for row in mdcsv:
            # get OCR
            ocrfn = row['OCR file name']
            if ocrfn and os.path.exists(os.path.join(OCRFOLDER, ocrfn)):
                with open(os.path.join(OCRFOLDER, ocrfn), "rt") as txtfile:
                    txt = txtfile.read().decode("cp1252")
                    txt2 = ''.join([c if ord(c) < 128 else ' ' for c in txt])
                    meetings = txt2.split("\r\n\r\n")
                    print(("Found {0} meetings for {1}, ({2})".format(len(meetings), row['newspaper'], row['date'])))
                    for meeting in meetings:
                        place = get_place(meeting)
                        if place in gazdict:
                            (long, lat) = gazdict[place]
                            geofound = True
                        else:
                            (long, lat) = ('', '')
                            geofound = False
                        if not geofound:
                            print(("No co-ordinates found for {0}".format(place)))
                            finalcsv.writerow([meeting, "", place, long, lat, row['newspaper'], row['date']])
            else:
                print("No transcription file found for '{0}, ({1})'. Skipping.".format(row['newspaper'], row['date']))
