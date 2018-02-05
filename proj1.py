import textblob as tb
from nltk import *
from nltk.corpus import stopwords
import json
import os
import re

stop = stopwords.words('english')

data = json.load(open('gg2018.json'))
strdata = "Allison Sun best director 2018 Golden Globes"
'''
for i in range(5):
	b = tb.TextBlob(data[i]["text"])
	if ("my son" in b.lower())
		print i
'''
'''
def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences
		
		
def extract_names(document):
		names = []
		sentences = ie_preprocess(document)
		for tagged_sentence in sentences:
			for chunk in nltk.ne_chunk(tagged_sentence):
				if type(chunk) == nltk.tree.Tree:
					if chunk.label() == 'PERSON':
						names.append(' '.join([c[0] for c in chunk]))
					if chunk.label() == "ORGANIZATION":
						names.append(' '.join([c[0] for c in chunk]))
		return names
		'''

tagged = pos_tag(strdata.lower().split())
names = [word for word,pos in tagged if pos == "NNP"]

print names