''' this file is for testing purposes '''
import time as time_

def indexOfFirstAlphabet( index_az ):
	indexNum = 0
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	for i in range(0,26):
		if index_az == alphabet[i:i+1]:
			return indexNum
		indexNum += 1

def searchWord( word, index_i, index_f ):
	for i in range(index_i, index_f):
		if word == dictionary[i]:
			print i
			return 1
	return 0
	
# Build hash table from the word list called 'dictionary'
dictionary = {}
i = 0
with open('wordlist.txt', 'r') as wordlist:
	for lines in wordlist:
		dictionary[i]= lines[0:-1]
		i += 1
	
	# Gather the index numbers of where each different alphabet in the dictionary starts
	wordlist.seek(0)
	wordIndex = {} 
	a_z = []
	alphabet = 'a'
	a_z.append(0)
	i = 0
	for line in wordlist:
		wordIndex[i] = line[0:-1].lower() 
		if line[0:1].lower() != alphabet.lower():
				a_z.append(i)
				alphabet = line[0:1].lower()
		i += 1
	print a_z # a = 0-4, b = 5-11, c = 12 onwards
#print dictionary


# if I pass in "changers", it should start looking in 12+ only
word = raw_input('>')
# extract first alphabet:
index_az = (word.lower())[0]
# get indices
indexNum = indexOfFirstAlphabet( index_az )
# print a_z[indexNum], a_z[indexNum+1] # prints out the lower and upper bound of indices in the dictionary to search from
searchFrom = a_z[indexNum]
if( index_az != 'z' ):
	searchTo = a_z[indexNum+1]
match = searchWord( word, searchFrom, searchTo ) 
if match: print "Yes"
else: print "no"


