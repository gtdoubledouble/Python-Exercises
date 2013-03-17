"""
Author: Gary Tse
Start Date: March 14, 2013
Link: GitHub

Input: user enters a word
Output: prints out the autocorrected version of the word; just like typing on a phone
Sources: wordlist.txt

Pseudocode:
Setup--
1. reads wordlist.txt into memory
Program Flow--
1. reads words from stdin
2a. IF autocorrrection is found, print that word out
2b. ELSE print out "NO SUGGESTION"

Objectives:
Faster than O(n) per word, n being length of wordlist/dictionary; don't scan the whole dictionary every time.
"""
import re
import string
import time as time_

def millis():
    return int(round(time_.time() * 1000))

def matchVowels( word, dictionary ):
	
	# Count amount of vowels
	vowelCount = 0
	
	wordToMatch = word
	print wordToMatch
	for letters in word:
		if letters in 'aeiou':
			wordToMatch = wordToMatch.replace(letters, '.')
			vowelCount += 1
	# now cunspericy becomes c nsp r cy
	print wordToMatch, "has", vowelCount, "vowels."
	
	dictionary.seek(0)
	matches = re.findall(wordToMatch+'\s', dictionary.read())
	print "Matches are:",matches
	
	revisedMatches = [] # List for matching words that have the SAME number of vowels 
	matchVowelCount = 0 # Initialize variable for counting vowels in each word of the matches list
	for matchedWords in matches:
		for letters in matchedWords:
			if letters in 'aeiou':
				matchVowelCount += 1
				'''if matchVowelCount == vowelCount:
					# Same vowels, but is the word an actual word, or just a segment of a longer word?
					# e.g. jjoobbb -> jobb and gets matched to jabb, which is a segment of the word 'jabber'
				'''	
				revisedMatches.append(matchedWords)
		matchVowelCount = 0 # Make sure matched words have same amount of vowels as previously			
		
	print "Revised matches:", revisedMatches
	
	if revisedMatches == [] or revisedMatches == None:
		return None
	else:
		return revisedMatches[0]

def correctWord( word, dictionary ):

	#repeats = [] # an array of repeated letters
	indexOfRepeats = [] # an array of the index positions of the repeated letters
	temp = "" # initialize this variable
	index = 0 # keeps track of where the repeated letters are in the word
	for letter in word: 
		# place any consecutive letters into the "repeats" array
		# the "temp" variable makes sure they're consecutive
		if( temp == letter ):
			#repeats.append(temp)
			indexOfRepeats.append(index)
		temp = letter	
		index += 1
	
	temp = list(word) # separate branch for repeated letter removing
	# the list makes it easy to track the indices of repeated letters
	
	count = 0 # this variable is used to prevent pop out of index error (see below)
	
	tempWord = word
	wordNotMatched = "No suggestion"
	
	match = matchVowels( tempWord, dictionary )
	if( match != None ):
		return match # exit and return word if its correct
	
	for i in indexOfRepeats:
		temp.pop(i-count) # everytime a letter is "popped" from the list, it will get shorter, so the original indexofRepeats need to be decremented
		tempWord = ''.join(temp) # convert back to string to check if word is correct
		match = matchVowels( tempWord, dictionary )
		if( match != None ):
			return match # exit and return word if its correct
		count += 1
	
	return wordNotMatched

dictionary = open('wordlist.txt', 'r')



while True:

	word = raw_input('> ')
	
	timeBefore = millis()
	
	# 1. Check to see if typed word was correct in the first place
	dictionary.seek(0)	
	
	match = 0
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			match = 1
	print "Word not in dictionary, attempting to match..."
	if( match == 1 ):
		print word
	# Otherwise, attempt to correct it
	else:	
		corrected = correctWord( word.lower(), dictionary )
		print "Corrected word is: ", corrected
		timeAfter = millis()
		timeRequired = timeAfter - timeBefore
		print "Time required:", timeRequired, "ms."
	
	
	
	# Get search time for a word using O(n) vs. O(logn)
	# Implement Hash Map/Table(?)

