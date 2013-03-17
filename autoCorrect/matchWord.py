''' this file is for testing purposes '''

def matchWord( word ):
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			return 1
	return 0
	
word = "sheeep"
l = list(word)
l.replace('e',"",1)
dictionary = open('wordlist.txt', 'r')
match = matchWord( l )
print match