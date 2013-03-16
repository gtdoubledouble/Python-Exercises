''' this file is for testing purposes '''

def matchWord( word ):
	for line in dictionary:
		if ( line[0:-1].lower() ) == word.lower() : # convert user input to all lower case to check
			return 1
	return 0
	
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
		match = matchWord(word)
		print word,"gives result",match
		if( match ):
			print "u have won"
			return match
		else:
			word = word.replace(i,"",1)
			print "replaced:",word
	return word

	
''' do not paste below this line '''
word = raw_input('> ')
dictionary = open('wordlist.txt', 'r')
print removeDuplicates( word )