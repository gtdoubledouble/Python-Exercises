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

import string
import time as time_

def millis():
    return int(round(time_.time() * 1000))

def matchWord( word ):
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			return 1
	return 0
	
def changeVowel( word ):
	# try out each possible vowel combination for a given word
	vowel = "aeiou"
	# return word as soon as match is found
	offset=0
	vowelPosition=0
	for i in word:
		if i in vowel:
			offset += vowelPosition
			vowelPosition = word.find(i,offset)
			substr = word[offset+1:]
			for j in vowel:
				word = word.replace(i,j,1)
				for k in vowel:
					print word
					if( matchWord( word ) != "No suggestions found" ):
						return word
	return "No suggestions found"

def removeRepeats( word ):

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
	return indexOfRepeats

def correctWord( word ):
	# check to see if typed word was correct in the first place
	if( matchWord( word ) ):
		return word
	
	# reduce duplicated alphabets (done first)
	indexOfRepeats = removeRepeats( word )
	print indexOfRepeats
	
	temp = list(word) # separate branch for repeated letter removing
	# the list makes it easy to track the indices of repeated letters
	count = 0 # this variable is used to prevent pop out of index error (see below)
	for i in indexOfRepeats:
		temp.pop(i-count) # everytime a letter is "popped" from the list, it will get shorter, so the original indexofRepeats need to be decremented
		dictionary.seek(0)
		tempWord = ''.join(temp) # convert back to string to check if word is correct
		if( matchWord( tempWord ) ):
			return tempWord # exit and return word if its correct
		count += 1
	
	# vowel correction 
	word = changeVowel( word ) 
	
	return word.lower()
	

dictionary = open('wordlist.txt', 'r')

while True:

	word = raw_input('> ')
	
	timeBefore = millis()
		
	corrected = correctWord(word)
	
	print corrected
				
	timeAfter = millis()
	timeRequired = timeAfter - timeBefore
	
	print "Autocorrection completed in", timeRequired, "ms."
	
	dictionary.seek(0)
	
	# Get search time for a word using O(n) vs. O(logn)
	# Implement Hash Map/Table(?)



	# On exit

