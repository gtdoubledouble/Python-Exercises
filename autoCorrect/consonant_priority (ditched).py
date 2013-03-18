# Consonants have a higher priority to be removed first (found to have more success rate)
	# Do this by swapping consonants to the front
	# Note: does not work ideally with repeated vowels in a word
	for r in range(0, len(repeats)):
		if( r+1 < len(repeats) ):
			if( repeats[r] in 'aeiou' and repeats[r+1] not in 'aeiou'):
				# swap with consonant
				temp = repeats[r]
				repeats[r] = repeats[r+1]
				repeats[r+1] = temp
				# swap the indices
				temp_i = indexOfRepeats[r]
				indexOfRepeats[r] = indexOfRepeats[r+1]
				indexOfRepeats[r+1] = temp_i