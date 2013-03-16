def changeVowel( word ):
	
	vowel = "aeiou"
	# change each vowel, then test
	# return word as soon as match is found
	
	for i in word:
		if i in vowel:
			for j in vowel:
				word = word.replace(i,j)
				return word
	return "No suggestions found"

# functions to test this class

word = raw_input('> ')
changeVowel( word ) # for a word like python, it should return pythun