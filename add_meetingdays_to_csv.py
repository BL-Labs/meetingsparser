import csv
from datetime import datetime, timedelta

INPUTFILE = 'geocoded_notdated_allyears.csv'
MATCHOUTPUTFILE = 'daysfound.csv'
NOMATCH_FILE = 'unmatched.csv'

MEETINGDATE_HEADER = 'Item Type Metadata:meeting date'

# NB This doesn't do anything? commenting out for now.
#Import the keywords
#f = open('daysgazetteer3.txt', 'r')
#alldays = f.read().lower().split("\n")
#f.close()

alldays = { 'today': timedelta(days=0),
            'this day': timedelta(days=0),
            'tomorrow': timedelta(days=1),
            'to-morrow': timedelta(days=1),
            'sunday': timedelta(days=1),
            'monday': timedelta(days=2),
            'tuesday': timedelta(days=3),
            'wednesday': timedelta(days=4),
            'thursday': timedelta(days=5),
            'friday': timedelta(days=6),
            'saturday': timedelta(days=7) }

def find_matches(inputtext):
  matching = []
  for token in inputtext.split():
    if token.strip(".") in alldays:
      matching.append(token.strip("."))
  return matching

with open(INPUTFILE, "r", newline="") as csvfile:
  # open the source file and create a dictionary csv reader. 
  # ASSUMPTION: All the columns will have *different* header names
  reader = csv.DictReader(csvfile)
  
  with open(NOMATCH_FILE, 'w', newline="") as nomatchfile:
    nomatchwriter = csv.DictWriter(nomatchfile, delimiter = ",", fieldnames = reader.fieldnames)
    # writing headers
    nomatchwriter.writerow(dict((fn,fn) for fn in reader.fieldnames))

    with open(MATCHOUTPUTFILE,'w', newline="") as matchfile:
      # Add a new column to the data row types
      headerlist = reader.fieldnames + [MEETINGDATE_HEADER]
      # Creating a dictionary writer and setting the fieldnames parameter, as
      # this defines the ordering of the output columns in the csv.
      writermatch = csv.DictWriter(matchfile, delimiter = ",", fieldnames = headerlist)
      # writing headers
      writermatch.writerow(dict((fn,fn) for fn in headerlist))
      # Going through the source data
      for row in reader:
        # Preflight work on the meeting text data. To lowercase, and potentially anything else
        # needed here:
        meetingText = row['Item Type Metadata:NewspaperText'].lower()
        # Get the publication date of the paper and parse it into a datetime object
        paperdate = datetime.strptime(row['Dublin Core:Date'], '%d/%m/%Y')
        # Print out the things we know:
        print("Date of paper: '{0}'\nNewspaper Text: '{1}'".format(paperdate, meetingText))
        
        # Now, search through the text, looking for works that match our Gazetteer list
        # Outcomes:
        #   1 - No match is found. 
        #       Response: Write row, unchanged to the hinted NOMATCH_FILE?
        #   2 - More than one matching word is found. Response: ...?
        #   3 - Only one matching word is found. 
        #       Response: Increment the date by that amount and add it to the new column, formatted
        #                 in a basic isoformat.
        
        matching = find_matches(meetingText)
        if not matching:
          # Add to NOMATCH_FILE
          nomatchwriter.writerow(row)
        elif len(matching) > 1:
          # Choice 2 - more than one match 
          print("More than one match! '{0}'".format(matching))
          print("Not doing anything with these for now. Writing to {0}".format(NOMATCH_FILE))
        elif len(matching) == 1:
          # Choice 3 - Exactly one match
          meetingdate = paperdate + alldays[matching[0]]
          row[MEETINGDATE_HEADER] = datetime.strftime(meetingdate,'%Y-%m-%d')
          print("Single match! '{0}' - meeting date = {1}".format(matching[0], row[MEETINGDATE_HEADER]))
          writermatch.writerow(row)
        

