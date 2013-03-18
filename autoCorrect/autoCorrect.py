"""
Auto correct algorithm

Author: Gary Tse
Start Date: March 14, 2013

Input: user enters a word
Output: prints out the autocorrected version of the word, if not corrected then it will print out "No suggestion"
Files: autoCorrect.py, wordlist.txt, testcases.txt

Notes: consonantPriority and vowelPriority are optional, they guarantee a bit more success rate
There are two ways of checking words in this program: regular expression (regex)'s re.findall, and traditional hash table lookup; both are faster than O(n).

Using notepad++ to view this code would be easier (minimize function codes).

Flow of program:
	Setup: Hash table (dict) is first created out of the word list text file
1. Program gets to choose between entering words or using testcases list (not very thorough)
2. Words are first checked to see if they're already correct
3. If not, words are sent to correctWord function
	a. A vowel change is done first using matchVowel, and if the result is right, it will be outputted
	b. Words then have their repeated letters tracked and removed one by one, with a vowel change done each time and checked against word list
	c. Either a matched, correct word will be outputted to screen, or it will be "No suggestion".
	
The vowelChange function replaces all vowels in a word with ".", which is a wildcard character.
Then the "."-filled word is checked against the whole wordlist using findall (which is a lot faster than normal search).

"""

import re # regular expressions, aka. regex
import time as time_ # to benchmark time required to perform operations

def millis():
    return int(round(time_.time() * 1000))

# Searches the Python dict (essentially a hash table)
# The try/except is for incorrect words, which don't exist in the dict
def matchWord( dictionary, word ):
	try:
		return [k for k, w in dictionary.iteritems() if w == word][0]
	except IndexError:
		return 0

def matchVowels( wordList, word ):
	
	# 1. Replace input word's vowels with '.' (wildcard), match with dictionary using regex's findall
	# 2. Revise those matches based on number of vowels in word, so a word like 'sheeeeep' does not become 'sharply'
		
	# Count amount of vowels
	vowelCount = 0
	vowelList = []
	
	wordToMatch = word
	print "Trying to correct the word:", wordToMatch
	
	# Replace all occurrences of vowels inside the input word
	# '.' allows replacement with any character using regex
	for letters in word:
		if letters in 'aeiou':
			vowelList.append(letters)
			wordToMatch = wordToMatch.replace(letters, '.')
			vowelCount += 1
	# Now a word like cunspericy becomes c.nsp.r.cy
	
	#print wordToMatch, "has", vowelCount, "vowels."
	
	# Regex
	# findall was found to be as fast if not faster than hash table lookup, definitely not O(n) time
	wordList.seek(0)
	matches = re.findall(wordToMatch+'\s', (wordList.read()).lower())
	#print "Possible matches are:", matches
	
	# Initialize a list for matching words that have the SAME number of vowels 
	revisedMatches = [] 
	# Initialize variable for counting vowels in each word of the matches list
	matchVowelCount = 0 
	
	# Loop through matched words, add the ones with proper vowel count to 'revisedMatches'
	for m in matches:
		for letters in m:
			if letters in 'aeiou':
				matchVowelCount += 1
				if matchVowelCount == vowelCount:
					revisedMatches.append(m)
		matchVowelCount = 0 # Make sure matched words have same amount of vowels as previously			
		
	#print "Revised matches:", revisedMatches
		
	if revisedMatches == [] or revisedMatches == None:
		return None
	else:
		# example: for the test case 'jjoooobbb' -> 'j_b' there would pbe the revisedMatch choices 'jab' and 'job'
		# In case the user just entered a word with repeated consonants but NOT different vowels, then that original vowel should be the first pick
		sameVowels = 0
		for r in revisedMatches:
			for v in vowelList:
				if v in r:
					sameVowels += 1
					if sameVowels >=1:
						return r
		return revisedMatches[0]

def repeatedLetters( word ):

	# this function removes repeated letters one by one, while checking for correctness and changing vowels
	
	# an array of the index positions of the repeated letters
	indexOfRepeats = [] 
	# an array of repeated letters, e.g. ['e','e','p'] in sheeepp
	repeats = []
	temp = "" # initialize this variable
	index = 0 # keeps track of where the repeated letters are in the word
	for letter in word: 
		# place any CONSEUCTIVE letters into the "repeats" array
		# the 'temp' variable checks for consecutiveness
		if( temp == letter ):
			repeats.append(temp)
			indexOfRepeats.append(index)
		temp = letter	
		index += 1
	
	#print "Repeated letters: ",repeats
	#print indexOfRepeats
	
	return repeats, indexOfRepeats
		
def correctWord( wordList, word ):

	repeats, indexOfRepeats = repeatedLetters( word )
	
	# iterate through two different copies of word, i.e. split off into two "branches"
	# one to reduce repeated consonants first, one to reduce repeated vowels first
	# because for the test case peepple, if we reduce vowels first, then it could become pepple and not match 'people'
	tempWord_c = word
	tempWord_v = word
	rc = list(repeats)
	rv = list(repeats)
	ic = list(indexOfRepeats)
	iv = list(indexOfRepeats)
	
	# Do a vowel check first on the incorrect word and see if is correct
	match = matchVowels( wordList, tempWord_c ) # doesn't matter which one yet
	if( match != None ):
		return match # exit and return word if its correct
	
	#print rc, rv
	
	# Because we want to avoid decrementing vowels or consonants first and not coming up with a match
	# So we generate matches based on replacing consonants first, and also replacing vowels first
	if( ic and iv ):
		repeats_c, indexOfRepeats_c = consonantPriority( rc, ic )
		repeats_v, indexOfRepeats_v = vowelPriority( rv, iv )
		ic = list(indexOfRepeats_c)
		iv = list(indexOfRepeats_v)
	
	
	#print "Consonants first:",repeats_c
	#print "Vowels first:",repeats_v
	
	matches = [] # stores the final collection of matches from both branches
	temp_c = list(word) # convert input word to a list
	temp_v = list(word)
	
	# Decrement consonants first
	count = 0 # this variable is used to prevent pop out of index error (see below)
	
	for i in ic:
		if( (i-count) > 0 ): # prevent removing the first letter of a word
			temp_c.pop(i-count) # everytime a repeat letter is removed from the word, it will get shorter, so we need to decrement to avoid IndexErrors
		else:
			temp_c.pop(1) # this code was implemented for the test case 'jjoooobbbb'. It would reduce to 'joob' and stop decrementing. Remove if necessary
		tempWord_c = ''.join(temp_c) # convert back to string to check if word is correct
		match = matchVowels( wordList, tempWord_c )
		if( match != None ):
			matches.append(match) # exit and return word if its correct
		count += 1
	# Decrement vowels first
	count = 0 # this variable is used to prevent pop out of index error (see below)
	for i in iv:
		if( (i-count) > 0 ): # prevent removing the first letter of a word, or decrementing too much
			temp_v.pop(i-count) # everytime a repeat letter is removed from the word, it will get shorter, so we need to decrement to avoid IndexErrors
		else:
			temp_v.pop(1) # this code was implemented for the test case 'jjoooobbbb'. It would reduce to 'joob' and stop decrementing. Remove if necessary
		tempWord_v = ''.join(temp_v) # convert back to string to check if word is correct
		match = matchVowels( wordList, tempWord_v )
		if( match != None ):
			matches.append(match) # exit and return word if its correct
		count += 1
	
	print "Final matches", matches 
	if( matches != [] ):
		return matches[0]
	
	return "No suggestion" # "no suggestion" if no match after removing repeated letters and changing vowels
	
def consonantPriority( repeats_c, indexOfRepeats_c ):
	# If consonants have higher priority
	# Do this by swapping consonants to the front
	# Note: does not work ideally with repeated vowels in a word
	for r in range(0, len(repeats_c)):
		if( r+1 < len(repeats_c) ):
			if( repeats_c[r] in 'aeiou' and repeats_c[r+1] not in 'aeiou'):
				# swap with consonant
				temp = repeats_c[r]
				repeats_c[r] = repeats_c[r+1]
				repeats_c[r+1] = temp
				# swap the indices
				temp_i = indexOfRepeats_c[r]
				indexOfRepeats_c[r] = indexOfRepeats_c[r+1]
				indexOfRepeats_c[r+1] = temp_i
	# Decrement once from back to front to ensure switching (OPTIONAL)
	for r in range(len(repeats_c)-1, -1, -1):
		if( r-1 > -1 ):
			if( repeats_c[r] not in 'aeiou' and repeats_c[r-1] in 'aeiou'):
				# swap with consonant
				temp = repeats_c[r]
				repeats_c[r] = repeats_c[r-1]
				repeats_c[r-1] = temp
				# swap the indices
				temp_i = indexOfRepeats_c[r]
				indexOfRepeats_c[r] = indexOfRepeats_c[r-1]
				indexOfRepeats_c[r-1] = temp_i
	return repeats_c, indexOfRepeats_c
				
def vowelPriority( repeats_v, indexOfRepeats_v ):				
	# If vowels have priority
	# Do this by swapping vowels to the front
	for r in range(0, len(repeats_v)):
		if( r+1 < len(repeats_v) ):
			if( repeats_v[r] not in 'aeiou' and repeats_v[r+1] in 'aeiou'):
				# swap with consonant
				temp = repeats_v[r]
				repeats_v[r] = repeats_v[r+1]
				repeats_v[r+1] = temp
				# swap the indices
				temp_i = indexOfRepeats_v[r]
				indexOfRepeats_v[r] = indexOfRepeats_v[r+1]
				indexOfRepeats_v[r+1] = temp_i
	# Decrement once from back to front to ensure switching (OPTIONAL)
	for r in range(len(repeats_v)-1, -1, -1):
		if( r-1 > -1 ):
			if( repeats_v[r] in 'aeiou' and repeats_v[r-1] not in 'aeiou'):
				# swap with consonant
				temp = repeats_v[r]
				repeats_v[r] = repeats_v[r-1]
				repeats_v[r-1] = temp
				# swap the indices
				temp_i = indexOfRepeats_v[r]
				indexOfRepeats_v[r] = indexOfRepeats_v[r-1]
				indexOfRepeats_v[r-1] = temp_i
	return repeats_v, indexOfRepeats_v
	
### Start of program ###

# Open the dictionary/wordlist file	
wordList = open('wordlist.txt', 'r')
# Strip/remove the whitespace or \n at the end of each word, convert to lower case
words = [( line.lower() ).strip() for line in wordList]
# Put them all into a Python dict (hash table implementation)
dictionary = dict(zip(range(0,len(words)), words))

# Give the user an option
print "Would you like to enter your own words or use the test case file?"
print "   [1] Test case file"
print "   [2] Enter your own words"
choice = raw_input('> ')

# Use test case file
if( choice == '1' ):
	testcases = open('testcases.txt' ,'r')
	# remove whitespace / enter key behind every word
	
	for word in testcases:
		
		print "\nWord to be matched: ", word[0:-1]
		timeBefore = millis()
		
		word = ''.join(re.findall("[A-Za-z]", word)) # extracts only alphabets out of input string
		wordList.seek(0)
		# Check to see if typed word was correct in the first place (no correction needed)
		if( matchWord( dictionary, word.lower() ) ):
			print word.lower()
			
		# Otherwise, attempt to correct it, print out "No suggestion" if all else fails
		else:	
			corrected = correctWord( wordList, word.lower() ).strip()
			print "Corrected:", corrected
			#print matchWord( dictionary, corrected ) <- prints index number of word, ranging from 0 to 45401
			
		print "Done in",millis()-timeBefore, "ms.\n\n"
		
# Choice to enter your own words
else:
	while True:

		word = raw_input('> ')
		word = ''.join(re.findall("[A-Za-z]", word)) # extracts only alphabets out of input string
		
		# Convert word to lower case to make matching easier
		word = word.lower() 
		
		# Calculate time it takes to perform the autocorrect
		timeBefore = millis()
		# Check to see if typed word was correct in the first place (no correction needed)
		if( matchWord( dictionary, word.lower() ) ):
			print word.lower()
			
		# Otherwise, attempt to correct it, print out "No suggestion" if all else fails
		else:
			if len(word) == 1: # don't bother running the program on one letter (will loop)
				print word.lower()
			else:
				corrected = correctWord( wordList, word.lower() )
				print "Corrected:", corrected
				#print matchWord( dictionary, corrected ) <- prints index number of word, ranging from 0 to 45401
			
		# Display time required
		print "Done in", millis() - timeBefore, "ms."
