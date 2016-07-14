# meetingsparser
Please use the 'concise version' branch of the code.
This code is designed to extract and separate lines of text from newspaper columns, geo-parse the place names in the text, and date the days of the week in the text according to the date of the newspaper. 
It is specifically designed for extracting, geo-parsing and dating political meetings recorded in the Northern Star newspaper, 1837-53, from the British Library newspaper collections. 
# details
http://politicalmeetingsmapper.co.uk
designed by Dr Katrina Navickas, University of Hertfordshire, and Ben O'Steen, British Library Labs
contact k.navickas@herts.ac.uk
# instructions
1. 'extractandgeotag.py' extracts the place information from the newspaper txt files and geoparses the places using the gazetteer  'NS_gazetteer.csv'
2. The csv output is then run through 'add_meetingdays_to_csv.py' using 'metadataNorthernStar.csv' to date the meetings.
