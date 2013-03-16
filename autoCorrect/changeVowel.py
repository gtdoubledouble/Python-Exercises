
def matchWord( word ):
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			return word.lower()
	return "No suggestions found"
def changeVowel( word ):
	# try out each possible vowel combination for a given word
	vowel = "aeiou"
	
	# return word as soon as match is found
	for i in word:
		if i in vowel:
			for j in vowel:
				word = word.replace(i,j)
				print word
				if( matchWord( word ) != "No suggestions found" ):
					return word
	return "No suggestions found"

# functions to test this class

word = raw_input('> ')
print changeVowel( word ) # for a word like python, it should return pythun