Auto correct algorithm:

Author: Gary Tse
Start Date: March 14, 2013

Input: user enters a word
Output: prints out the autocorrected version of the word, if not corrected then it will print out "No suggestion"
Sources: wordlist.txt, testcases.txt

main.py = the code using normal O(n) search, n being the amount of words in the dictionary file
main2.py = verbose version of main.py
autoCorrect.py = updated, hash table using search

* all three use regular expressions for the majority of searches, and hash table lookup for the initial search
re.findall is faster than O(n), shown in Search speed comparisons.png, but I'd say the bottleneck is when the input word is very complex and requires multiple iterations to fix

matchWord.py = old slow search
matchWordBadImplementation.py = a failed idea at trying to take index numbers of all words starting with different alphabets in the dictionary list, which would make it O(n/26) but slow nonetheless
newMatchWord.py = current working hash table lookup for search
removeRepeats.py = test file for that function

Pseudocode:
Setup--
1. reads wordlist.txt into memory
Program flow--
1. reads words from stdin
2a. IF autocorrrection is found, print that word out
2b. ELSE print out "No suggestion"

What doesn't work:
jjoobbb
Proper nouns will print out as all lower case

---

Resources consulted:

Peter Norvig's spell checker: http://norvig.com/spell-correct.html
Regex: https://developers.google.com/edu/python/regular-expressions
http://stackoverflow.com/questions/10017808/best-data-structure-for-dictionary-implementation
- considered using tries: http://www.billdimmick.com/devjournal/using-a-trie-in-python.html
- considered implementing BK tree: http://code.activestate.com/recipes/572156-bk-tree/
