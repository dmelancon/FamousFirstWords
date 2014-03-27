import sys
import urllib
import random
import json
import nltk
from time import sleep

api_key = sys.argv[1]
files = sys.argv[2]
text = open(files)


#returns list of parts of speech, followed by a list of the original words in order
def returnPOS(words):              
	token = nltk.word_tokenize(words)
	POS = list()
	WORDS =list()
	for i in nltk.pos_tag(token):
		POS.append(i[1])
		WORDS.append(i[0])
	return POS, WORDS


#returns single words POS tag,	
def checkPOS(word):                 
	return nltk.pos_tag(nltk.word_tokenize(word))[0][1]
 

#replaces a word by searching a randomly assigned related word 'type' and then tests if result is correct POS, 
#continues running until there is a part of speech match, or it returns the original word    
def replaceWord(word,pos): 
	pos = pos
	if len(word)>2:                       
		types =['related-word', 'synonym' , 'antonym' ,'same-context','hypernym']
		params = {
			'useCanonical': 'true',
			'relationshipTypes' : types[random.randrange(5)],
			'limitPerRelationshipType': '10',
			'api_key': api_key
			}
		url = "http://api.wordnik.com/v4/word.json/" + urllib.quote_plus(word) \
		+"/relatedWords?" + urllib.urlencode(params)
		urlobj = urllib.urlopen(url)
		result = json.loads(urlobj.read())
		if len(result) > 0 and pos is not None:
			for definition in result:
				count = 0
				while True:
					newWord = definition['words'][random.randrange(len(definition['words']))]
					count+=1
					if checkPOS(newWord) == pos:
						return newWord
						break
					elif count>30:
						return word
						break
		else:
		 	return word	
	else:
		return word	


for line in text:         #need to fix, was tryin to append so that new parts of speechs would be passed through
	mLine = []
	newSentence = list()
	Sentences = list()
	mSentence = str
	mLine = returnPOS(line)
	for i in range(len(mLine[0])):
		newSentence.append(replaceWord(mLine[1][i],mLine[0][i]))
	mSentence = " ".join(newSentence).replace(' ,', ',')
	mSentence = mSentence.replace(' .', '.')
	for x in range(10):
		new=[]
		mLine = returnPOS(mSentence)
		for y in range(len(mLine[0])):
			new.append(replaceWord(mLine[1][y],mLine[0][y]))
		Sentences.append(new)
		Sentence = " ".join(Sentences[x]).replace(' ,', ',')
		print Sentence.replace(' .', '.')


