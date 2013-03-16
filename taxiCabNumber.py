"""
Title: Taxi Cab Number
Author: Gary Tse
Start Date: March 14, 2013
Link: http://www.GitHub.com/garytse89

Input: user enters a number, N
Output: prints out a list of numbers up to N that are taxi cab numbers

A taxi cab number:
	Given 4 DIFFERENT numbers: a,b,c,d, then a taxi cab number = a^3 + b^3 = c^3 + d^3.

Note**: this isn't the official taxi cab number definition found on Wikipedia, it is a bit more lenient
Credits: none, original algorithm

Pseudocode:
1. Take in a number N from user.
2. Since we know that a,b,c, or d cannot be greater than the cube root of N, we only iterate up to N^(1/3), called "max"
3. We run through all permutations of a,b,c,d up to max
	For a particular permutation (e.g. 1,2,3,4) called temp (array):
	3a) Check to see if any of the numbers are the same (1,3,2,3 would not pass)
		3a1) Check to see if a^3 + b^3 (could be c^3 + d^3 too) exceed user's entered number, N 
			3a1a) Check to see if a^3 + b^3 = c^3 + d^3 (that's a taxi number right there if true)
				3a1a1) Add the taxi number to list
				
Test cases:
1729 is the first taxi cab number

Functions:
millis is used to display the runtime of the program.
cube is used to cube a number.
taxiCabNumber is where everything is done.
"""

import math
import time as time_

def millis():
    return int(round(time_.time() * 1000))

def cube( num ):
	return num*num*num
	
def taxiCabNumber( N, max ):
	taxiNum = []
	temp = []
	# iterate through all possible permutations of a,b,c,d up to "max"
	i = 1
	delivered = 0
	for a in range( i, max+1 ):
	
		for b in range( i, max+1 ):
			for c in range( i, max+1 ):
				for d in range( i, max+1 ):
					temp = [a,b,c,d]
					# check to see if a b c d are duplicates of each other (smart!)
					if( len(temp) == len(set(temp)) ):
						if( cube(a) + cube(b) )<N:
							if( cube(a)+cube(b) == cube(c)+cube(d) ):
								# only add taxi number into an array if there were no previous duplicate entries
								# (since duplicated permutations were not accounted for, e.g. abcd = 1342 vs. 1234)
								if (cube(a)+cube(b)) not in taxiNum: 
									taxiNum.append(cube(a)+cube(b))
									print a, "^3 +", b, "^3 =", c, "^3 +", d, "^3 =", cube(a)+cube(b)
	return taxiNum
	

N = raw_input()

timeBefore = millis()

N = int(N)
max = int(round(pow(N,1/3.0)))
print "Max =", max

taxiNum = taxiCabNumber( N, max )
taxiNum.sort()
print taxiNum

timeAfter = millis()
print "Runtime: ", timeAfter-timeBefore , "ms"
