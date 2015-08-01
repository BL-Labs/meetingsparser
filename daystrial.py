#Import the keywords
f = open('daysgazetteer.txt', 'r')
alldays = f.read().lower().split("\n")
f.close()

#Import the texts you want to search
f = open('31julytextNSFM.txt', 'r')
allTexts = f.read().lower().split("\n")
f.close()

#Our programme:
for entry in allTexts:
    matches = 0
    storedMatches = []

    #for each entry:
    allWords = entry.split(' ')
    for words in allWords:

        #remove punctuation that will interfere with matching
        words = words.replace(',', '')
        words = words.replace('.', '')
        words = words.replace(';', '')


        #if a keyword match is found, store the result.
        if words in alldays:
            if words in storedMatches:
                continue
            else:
                storedMatches.append(words)
            matches += 1

    #if there is a stored result, print it out
    if matches == 0:
        print ' '
    else:
        matchString = ''
        for matches in storedMatches:
            matchString = matchString + matches + "\t"

        print matchString
