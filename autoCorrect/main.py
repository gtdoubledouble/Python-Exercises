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
from changeVowel import changeVowel

import sys
import string
import time as time_

def millis():
    return int(round(time_.time() * 1000))

def matchWord( word ):
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			return word.lower()
	return "No suggestions found"
	
def correctWord( word ):
	# reduce duplicated alphabets (done first)
	
	# vowel correction (done second)
	# use case: weke => wake
	
	# try out each possible vowel combination for a given word
	while ( changeVowel( word ) != "No suggestions found" ):
		if( matchWord( changeVowel( word ) ) != "No suggestions found" ):
			word = matchWord( word )
			return word
	
	return "No suggestions found"
	

dictionary = open('wordlist.txt', 'r')


while True:

	word = raw_input('> ')
	
	timeBefore = millis()
		
	corrected = matchWord(word)
	
	print corrected
				
	timeAfter = millis()
	timeRequired = timeAfter - timeBefore
	
	print "Autocorrection completed in", timeRequired, "ms."
	
	dictionary.seek(0)
	
	# Get search time for a word using O(n) vs. O(logn)
	# Implement Hash Map/Table(?)



	# On exit

