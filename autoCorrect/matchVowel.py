import re # using regular expressions

def matchWord( word ):
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			return 1
	return 0

# search dictionary to see if there are any words with "c nsp r cy" pattern
def matchVowels( word, dictionary):
	
	word = word.lower()
	for letters in word:
		if letters in 'aeiou':
			word = word.replace(letters, '.')
	# now cunspericy becomes c nsp r cy
	print word
	
	#match = re.search(word, wordlist)
	matches = re.findall(word, dictionary.read())
	
	print matches
	if matches == []:
		return word
	else:
		return matches[0]
	
	
word = raw_input('>')

dictionary = open('wordlist.txt', 'r')

match = matchVowels( word, dictionary )

print match
