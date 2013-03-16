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
			return word.lower()
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

def removeDuplicates( word ):
	# for repeated alphabets such as the word "sheeep", try removing one 'e', then two
	
	# note: the space bar is treated as an "i"
	
	# initialize alphabets
	alphabets = "abcdefghijklmnopqrstuvwxyz"
	repeatList = []
	# 1. Convert to list
	l = list(word)
	# 2. Count instances of alphabets repeated more than once in the input word and append to an array called repeatList
	# So "sheeep" would generate a repeatList array = ['e', 'e'] since there are 2 unncessary repetitions
	for a_z in alphabets:
		count = l.count(a_z)
		for n in range(2, count+1):
			repeatList.append(a_z)
	#print repeatList
	
	# 3. Delete duplicated alphabets one by one while checking for matches
	# So before 'sheeeeep' gets reduced to 'shep', we should find a match for 'sheep'
	for i in repeatList:
		# Match word
		match = matchWord( word )
		if( match != 0 ):
			return match
		word = word.replace(i,"",1)
	return word

def correctWord( word ):
	# check to see if typed word was correct in the first place
	if( matchWord( word ) ):
		return word
	
	# reduce duplicated alphabets (done first)
	word = removeDuplicates( word )
	# vowel correction (done second)
	word = changeVowel( word ) 
	
	return (matchWord( word ))
	

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

