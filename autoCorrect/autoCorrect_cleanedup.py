"""
Auto correct algorithm

Author: Gary Tse
Start Date: March 14, 2013

Input: user enters a word
Output: prints out the autocorrected version of the word, if not corrected then it will print out "No suggestion"
Files: autoCorrect.py, wordlist.txt, testcases.txt

Notes: consonant_priority and vowel_priority are optional, they guarantee a bit more success rate
There are two ways of checking words in this program: regular expression (regex)'s re.findall, and traditional hash table lookup; both are faster than O(n).

Using notepad++ to view this code would be easier (minimize function codes).

Flow of program:
	Setup: Hash table (dict) is first created out of the word list text file
1. Program gets to choose between entering words or using testcases list (not very thorough)
2. Words are first checked to see if they're already correct
3. If not, words are sent to correct_word function
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
def match_word( dictionary, word ):
	try:
		return [k for k, w in dictionary.iteritems() if w == word][0]
	except IndexError:
		return 0

def replace_vowels( wordlist, word ):
	
	# 1. Replace input word's vowels with '.' (wildcard), match with dictionary using regex's findall
	# 2. Revise those matches based on number of vowels in word, so a word like 'sheeeeep' does not become 'sharply'
		
	# Count amount of vowels
	vowel_count = 0
	vowel_list = []
	
	word_to_match = word
	print "Trying to correct the word:", word_to_match
	
	# Replace all occurrences of vowels inside the input word
	# '.' allows replacement with any character using regex
	for letters in word:
		if letters in 'aeiou':
			vowel_list.append(letters)
			word_to_match = word_to_match.replace(letters, '.')
			vowel_count += 1
	# Now a word like cunspericy becomes c.nsp.r.cy
	
	#print word_to_match, "has", vowel_count, "vowels."
	
	# Regex
	# findall was found to be as fast if not faster than hash table lookup, definitely not O(n) time
	wordlist.seek(0)
	matches = re.findall(word_to_match+'\s', (wordlist.read()).lower())
	#print "Possible matches are:", matches
	
	# Initialize a list for matching words that have the SAME number of vowels 
	revised_matches = [] 
	# Initialize variable for counting vowels in each word of the matches list
	matchvowel_count = 0 
	
	# Loop through matched words, add the ones with proper vowel count to 'revised_matches'
	for m in matches:
		for letters in m:
			if letters in 'aeiou':
				matchvowel_count += 1
				if matchvowel_count == vowel_count:
					revised_matches.append(m)
		matchvowel_count = 0 # Make sure matched words have same amount of vowels as previously			
		
	#print "Revised matches:", revised_matches
		
	if len(revised_matches) is 0:
		return None
	else:
		# example: for the test case 'jjoooobbb' -> 'j_b' there would pbe the revisedMatch choices 'jab' and 'job'
		# In case the user just entered a word with repeated consonants but NOT different vowels, then that original vowel should be the first pick
		for same_vowels, r in enumerate(revised_matches):
			for v in vowel_list:
				if v in r:
					if same_vowels >= 1:
						return r
		return revised_matches[0]

def repeated_letters( word ):

	# this function removes repeated letters one by one, while checking for correctness and changing vowels
	
	# an array of repeated letters, e.g. ['e','e','p'] in sheeepp
	repeats = []
	prev = "" # initialize this variable
	
	for i, letter in enumerate(word): 
		# place any CONSEUCTIVE letters into the "repeats" array
		# the 'temp' variable checks for consecutiveness
		if( prev == letter ):
			repeats.append((letter, i))
		prev = letter
	return repeats	
			
def correct_word( wordlist, word ):

	repeats = repeated_letters( word )
	
	# iterate through two different copies of word, i.e. split off into two "branches"
	# one to reduce repeated consonants first, one to reduce repeated vowels first
	# because for the test case peepple, if we reduce vowels first, then it could become pepple and not match 'people'
	temp_word_c = word
	temp_word_v = word
		
	# Do a vowel check first on the incorrect word and see if is correct
	match = replace_vowels( wordlist, temp_word_c ) # doesn't matter which one yet
	if( match != None ):
		return match # exit and return word if its correct
		
	# Because we want to avoid decrementing vowels or consonants first and not coming up with a match
	# So we generate matches based on replacing consonants first, and also replacing vowels first
	repeats_v = prioritise_consonants( repeats )
	repeats_c = prioritise_vowels( repeats )
		
	matches = [] # stores the final collection of matches from both branches
	temp_c = list(word) # convert input word to a list
	temp_v = list(word)
	
	print "Consonants prioritised:", repeats_c
	print "Vowels prioritised:", repeats_v
		
	# Decrement consonants first
	for count, i in enumerate(repeats_c):
		if( (i[1]-count) > 0 ): # prevent removing the first letter of a word
			temp_c.pop(i[1]-count) # everytime a repeat letter is removed from the word, it will get shorter, so we need to decrement to avoid IndexErrors
		else:
			temp_c.pop(1) # this code was implemented for the test case 'jjoooobbbb'. It would reduce to 'joob' and stop decrementing. Remove if necessary
		temp_word_c = ''.join(temp_c) # convert back to string to check if word is correct
		match = replace_vowels( wordlist, temp_word_c )
		if( match != None ):
			matches.append(match) # exit and return word if its correct
		
	# Decrement vowels first
	for count, i in enumerate(repeats_v):
		if( (i[1]-count) > 0 ): # prevent removing the first letter of a word, or decrementing too much
			temp_v.pop(i[1]-count) # everytime a repeat letter is removed from the word, it will get shorter, so we need to decrement to avoid IndexErrors
		else:
			temp_v.pop(1) # this code was implemented for the test case 'jjoooobbbb'. It would reduce to 'joob' and stop decrementing. Remove if necessary
		temp_word_v = ''.join(temp_v) # convert back to string to check if word is correct
		match = replace_vowels( wordlist, temp_word_v )
		if( match != None ):
			matches.append(match) # exit and return word if its correct
		
	print "Final matches", matches 
	if( matches != [] ):
		return matches[0]
	
	return "No suggestion" # "no suggestion" if no match after removing repeated letters and changing vowels

def group_repeats(repeats):
    vowels = []
    consonants = []
    for ch, i in repeats:
        if ch in 'aeiou':
            vowels.append((ch, i))
        else:
            consonants.append((ch, i))
    return vowels, consonants
	
def prioritise_vowels(repeats):
    vowels, consonants = group_repeats(repeats)
    return consonants + vowels

def prioritise_consonants(repeats):
    vowels, consonants = group_repeats(repeats)
    return vowels + consonants
	
### Start of program ###

# Open the dictionary/wordlist file	
wordlist = open('wordlist.txt', 'r')
# Strip/remove the whitespace or \n at the end of each word, convert to lower case
words = [( line.lower() ).strip() for line in wordlist]
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
		wordlist.seek(0)
		# Check to see if typed word was correct in the first place (no correction needed)
		if( match_word( dictionary, word.lower() ) ):
			print word.lower()
			
		# Otherwise, attempt to correct it, print out "No suggestion" if all else fails
		else:	
			corrected = correct_word( wordlist, word.lower() ).strip()
			print "Corrected:", corrected
			#print match_word( dictionary, corrected ) <- prints index number of word, ranging from 0 to 45401
			
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
		if( match_word( dictionary, word.lower() ) ):
			print word.lower()
			
		# Otherwise, attempt to correct it, print out "No suggestion" if all else fails
		else:
			if len(word) == 1: # don't bother running the program on one letter (will loop)
				print word.lower()
			else:
				corrected = correct_word( wordlist, word.lower() )
				print "Corrected:", corrected
				#print match_word( dictionary, corrected ) <- prints index number of word, ranging from 0 to 45401
			
		# Display time required
		print "Done in", millis() - timeBefore, "ms."
