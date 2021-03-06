import csv, string, os, re

MDFILE = "metadataNorthernStar.csv"
OCRFOLDER = "TEXT FILES"
FINALCSV = "outputgeo_1841to44.csv"

HEADERS = ["Item Type Metadata:NewspaperText", "Item Type Metadata:Date of meeting", "Item Type Metadata:Place","geolocation:longitude", "geolocation:latitude", "geolocation:zoom_level", "Item Type Metadata:Newspaper", "Dublin Core:Date", "itemType", "geolocation:map_type", "geolocation:address"]

#load and process gazetteer
gazdict={}
gaz = open("NS_gazetteer.csv","rb")
linenum = 0
p=re.compile(',\ *(-?[0-9.]*),\ *(-?[0-9.]*)')
for line in gaz:
        print linenum
        (place, fullplace, longlat) = line[1:-3].split('""')
        rematch = p.match(longlat)
        linenum+=1
        if rematch:
                lng = p.match(longlat).group(1)
                lat = p.match(longlat).group(2)
                if float(lng)>58 or float(lng)<50 or float(lat)>4 or float(lat)<-6:
                        print("{0} (line {1}) looks well-dodgy longlat wise".format(linenum, place))
                gazdict[place[:-1]]=(lng, lat)
        else:
                print("Error in gazetteer line {0}: {1}. Skipping".format(linenum, line))


def get_place(meeting_txt):
        return string.capwords(meeting_txt.split(".")[0].lower())
with open(FINALCSV, "wb") as final:
        finalcsv = csv.writer(final)
        finalcsv.writerow(HEADERS)
        with open(MDFILE, "rb") as mdfile:
                mdcsv = csv.DictReader(mdfile)
                for row in mdcsv:
                        # get OCR
                        ocrfn = row['OCR file name']
                        if ocrfn and os.path.exists(os.path.join(OCRFOLDER, ocrfn)):
                                with open(os.path.join(OCRFOLDER, ocrfn), "rb") as txtfile:
                                        txt = txtfile.read().decode("cp1252")
                                        txt2 = ''.join([c if ord(c) < 128 else ' ' for c in txt])
                                        meetings = txt2.split("\r\n\r\n")
                                        print("Found {0} meetings for {1}, ({2})".format(len(meetings), row['Item Type Metadata:Newspaper'], row['Dublin Core:date']))
                                        for meeting in meetings:
                                                place = get_place(meeting)
                                                if place in gazdict:
                                                        (long, lat) = gazdict[place]
                                                        geofound = True
                                                else:
                                                        (long, lat) = ('', '')
                                                        geofound = False
                                                if not geofound:
                                                        print("No co-ordinates found for {0}".format(place))
                                                finalcsv.writerow(map(lambda x: x.encode("utf-8"), [meeting, "", place, long, lat, "", row['Item Type Metadata:Newspaper'], "", "", row['Dublin Core:date'], "", "",]))
                        else:
                                print ocrfn
                                print os.path.join(OCRFOLDER, ocrfn)
                                print("No transcription file found for '{0}, ({1})'. Skipping.".format(row['Item Type Metadata:Newspaper'], row['Dublin Core:date']))
