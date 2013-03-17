def removeRepeats( word ):

	#repeats = [] # an array of repeated letters
	indexOfRepeats = [] # an array of the index positions of the repeated letters
	temp = "" # initialize this variable
	index = 0 # keeps track of where the repeated letters are in the word
	for letter in word: 
		# place any consecutive letters into the "repeats" array
		# the "temp" variable makes sure they're consecutive
		if( temp == letter ):
			#repeats.append(temp)
			indexOfRepeats.append(index)
		temp = letter	
		index += 1
	return indexOfRepeats