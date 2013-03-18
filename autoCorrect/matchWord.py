import time
import re

def millis():
	return int(round(time.time() * 1000))

	
def matchWord(dict, val):
	try:
		return [k for k, v in dictionary.iteritems() if v == val][0]
	except IndexError:
		return 0

word = raw_input('>')

wordList = open('wordlist.txt', 'r')
words = [line.strip() for line in wordList]
#for lines in words:
dictionary = dict(zip(range(0,len(words)), words))

before = millis()
print matchWord(dictionary, word)
print "Hash table search requires",millis()-before,"ms."

before = millis()
wordList.seek(0)
for line in wordList:
	if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
		match = 1
	else: match = 0
print "Normal search requires",millis()-before,"ms."

wordList.seek(0)
before = millis()
matches = re.findall(word, wordList.read())
print matches
print "Findall requires",millis()-before,"ms."