import csv
import itertools
from datetime import datetime, timedelta

inputfile = 'outputgeo1aug.csv'
matchoutputfile = 'daysfound.csv'

alldays = [['today', timedelta(days=0)],
['this day', timedelta(days=0)],
['tomorrow', timedelta(days=1)],
['to-morrow', timedelta(days=1)],
['Sunday next', timedelta(days=8)],
['Sunday', timedelta(days=1)],
['Monday', timedelta(days=2)],
['Tuesday', timedelta(days=3)],
['Wednesday', timedelta(days=4)],
['Thursday', timedelta(days=5)],
['Friday', timedelta(days=6)],
['Saturday', timedelta(days=7)]]

with open(inputfile) as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    with open(matchoutputfile,'w') as matchfile:
		writermatch = csv.writer(matchfile)
		newheaders = list(headers).append('meeting date')
		writermatch.writerow(headers)			# add csv column
		for row in reader:	#itertools.islice(reader,5):
			meetingText = row[0].lower()
			paperdate = datetime.strptime(row[7], '%d/%m/%Y')
			for (day, dayOffset) in alldays:
				ind=meetingText.find(day.lower())
				if not ind==-1:
					meetingdate = paperdate + dayOffset
					newrow = list(row)
					newrow.append('%02d/%02d/%d' % (meetingdate.day, meetingdate.month, meetingdate.year))
					writermatch.writerow(newrow)
					if day=='Sunday next':		#special case 'sunday next' so doesn't also match 'sunday'
						meetingText = meetingText.replace('sunday next', 'xunday next')


    				

