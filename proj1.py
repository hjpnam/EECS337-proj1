import textblob as tb
import nltk
from nltk.corpus import stopwords
from nltk.corpus import names
import json
import os
import re

stop = stopwords.words('english')
data = json.load(open('gg2018.json'))
strdata = "Allison Sun Meryl Streep brad pitt chris evans Golden Globes sameena william peter"

def get_names(str):
    # currently only gets first names
	names = nltk.corpus.names
	all_names = names.words('male.txt') + names.words('female.txt')
	all_names = [name.lower() for name in all_names]

	tweet_names= []
	words = str.lower().split()

	for i in range(0, len(words)):
		if words[i] in all_names:
			tweet_names.append(words[i])
	print tweet_names
	return tweet_names

get_names(strdata)
