import re # using regular expressions

def matchWord( word ):
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			return 1
	return 0

# search dictionary to see if there are any words with "c nsp r cy" pattern
def matchVowels( word, dictionary ):
	
	wordToMatch = word
	for letters in wordToMatch:
		if letters in 'aeiou':
			wordToMatch = wordToMatch.replace(letters, '.')
	# now cunspericy becomes c nsp r cy
	print wordToMatch
	
	dictionary.seek(0)
	matches = re.findall(wordToMatch, dictionary.read())
	print "MATCHES ARE......",matches
	if matches == []:
		return None
	else:
		return matches[0]
	
	
word = raw_input('>')

dictionary = open('wordlist.txt', 'r')

match = matchVowels( word, dictionary )

print match
