"""
Auto correct algorithm:

Author: Gary Tse
Start Date: March 14, 2013

Input: user enters a word
Output: prints out the autocorrected version of the word, if not corrected then it will print out "No suggestion"
Sources: wordlist.txt, testcases.txt

main.py = the code using normal O(n) search, n being the amount of words in the dictionary file
main2.py = verbose version of main.py
autoCorrect.py = updated, hash table using search

* all three use regular expressions for the majority of searches, and hash table lookup for the initial search
re.findall is faster than O(n), shown in Search speed comparisons.png, but I'd say the bottleneck is when the input word is very complex and requires multiple iterations to fix

matchWord.py = old slow search
matchWordBadImplementation.py = a failed idea at trying to take index numbers of all words starting with different alphabets in the dictionary list, which would make it O(n/26) but slow nonetheless
newMatchWord.py = current working hash table lookup for search
removeRepeats.py = test file for that function

Pseudocode:
Setup--
1. reads wordlist.txt into memory
Program flow--
1. reads words from stdin
2a. IF autocorrrection is found, print that word out
2b. ELSE print out "No suggestion"

What doesn't work:
jjoobbb
Proper nouns will print out as all lower case

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
	print "Trying to correct the word:",wordToMatch
	
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
	print "Possible matches are:", matches
	
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
		
	print "Revised matches:", revisedMatches
		
	if revisedMatches == [] or revisedMatches == None:
		return None
	else:
		# example: for the test case 'jjoooobbb' -> 'j_b' there would pbe the revisedMatch choices 'jab' and 'job'
		# In case the user just entered a word with repeated consonants but NOT different vowels, then that original vowel should be the first pick
		for r in revisedMatches:
			if vowelList[0] in r:
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
	
	print "Repeated letters: ",repeats
	print indexOfRepeats
	
	return indexOfRepeats
		
def correctWord( wordList, word ):

	indexOfRepeats = repeatedLetters( word )
		
	# convert input word to a list
	temp = list(word) 
		
	tempWord = word
	
	# Do a vowel change first on the incorrect word and see if is correct
	match = matchVowels( wordList, tempWord )
	if( match != None ):
		return match # exit and return word if its correct
	
	#print "Index of repeated letters:",indexOfRepeats
	
	count = 0 # this variable is used to prevent pop out of index error (see below)
	for i in indexOfRepeats:
		temp.pop(i-count) # everytime a repeat letter is removed from the word, it will get shorter, so we need to decrement to avoid IndexErrors
		tempWord = ''.join(temp) # convert back to string to check if word is correct
		match = matchVowels( wordList, tempWord )
		if( match != None ):
			return match # exit and return word if its correct
		count += 1
	
	return "No suggestion" # "no suggestion" if no match after removing repeated letters and changing vowels

	
	
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
		word = word[0:-1]
		wordList.seek(0)
		# Check to see if typed word was correct in the first place (no correction needed)
		if( matchWord( dictionary, word.lower() ) ):
			print word.lower()
			
		# Otherwise, attempt to correct it, print out "No suggestion" if all else fails
		else:	
			corrected = correctWord( wordList, word.lower() ).strip()
			print "Corrected:", corrected
			#print matchWord( dictionary, corrected ) <- prints index number of word, ranging from 0 to 45401
			
		print "Done in",millis()-timeBefore, "ms"
		
# Choice to enter your own words
else:
	while True:

		word = raw_input('> ')
		
		# Convert word to lower case to make matching easier
		word = word.lower() 
		
		# Calculate time it takes to perform the autocorrect
		timeBefore = millis()
		# Check to see if typed word was correct in the first place (no correction needed)
		if( matchWord( dictionary, word.lower() ) ):
			print word.lower()
			
		# Otherwise, attempt to correct it, print out "No suggestion" if all else fails
		else:	
			corrected = correctWord( wordList, word.lower() )
			print "Corrected:", corrected
			#print matchWord( dictionary, corrected ) <- prints index number of word, ranging from 0 to 45401
			
		# Display time required
		print "Done in", millis() - timeBefore, "ms."
