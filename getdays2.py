import csv
import itertools
from datetime import datetime, timedelta

inputfile = 'outputgeo1aug.csv'
matchoutputfile = 'daysfound.csv'
nomatchoutputfile = 'unmatched.csv'

#Import the keywords
f = open('daysgazetteer3.txt', 'r')
alldays = f.read().lower().split("\n")
f.close()

alldays = [['today', timedelta(days=0)],
['this day', timedelta(days=0)],
['tomorrow', timedelta(days=1)],
['to-morrow', timedelta(days=1)],
['Sunday', timedelta(days=1)],
['Monday', timedelta(days=2)],
['Tuesday', timedelta(days=3)],
['Wednesday', timedelta(days=4)],
['Thursday', timedelta(days=5)],
['Friday', timedelta(days=6)],
['Saturday', timedelta(days=7)]]

#Import the 'Details' column from the CSV file
allTexts = []
fullRow = []

with open(inputfile) as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    with open(matchoutputfile,'w') as matchfile:
		writermatch = csv.writer(matchfile)
		newheaders = list(headers).append('meeting date')
		writermatch.writerow(headers)
		for row in itertools.islice(reader,5):
			meetingText = row[0].lower()
			paperdate = datetime.strptime(row[7], '%d/%m/%Y')
			print paperdate
			print meetingText
			for (day, dayOffset) in alldays:
				ind=meetingText.find(day.lower())
				if not ind==-1:
					meetingdate = paperdate + dayOffset
					newrow = list(row)
					newrow.append(datetime.strftime(meetingdate,'%d/%m/%Y'))
					print newrow, meetingdate
					writermatch.writerow(newrow)

    				

