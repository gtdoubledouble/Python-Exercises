def removeRepeats( word ):

	repeats = [] #an array of repeated letters
	temp = ""
	for letter in word:
		if( temp == letter ):
			repeats.append(temp)
		temp = letter	
	return repeats

word = "sheeep"
print removeRepeats( word )
