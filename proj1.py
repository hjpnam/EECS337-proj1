import textblob as tb
import nltk
from nltk.corpus import stopwords
from nltk.corpus import names
import json
import os
import re
import wikipedia

stop = stopwords.words('english')
data = json.load(open('gg2018.json'))
text = []
a = "Suddenly, Mary Poppins flew away with her umbrella. Later in the day, John Johnson did something."


# for i in range(0, 10):
# 	tweet = data[i].get("text")
# 	text.append(tweet)
# print text

strdata = "Allison Sun Meryl Streep brad pitt chris evans Golden Globes sameena william peter"

def getnames2(str):
	names = []
	people = re.findall('([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'," ".join(text))
	print people
	for word in people:
		names.append(word)

def get_names(str):
	names = nltk.corpus.names
	all_names = names.words('male.txt') + names.words('female.txt')
	all_names = [name.lower() for name in all_names]

	tweet_names= []
	words = str.lower().split()

	for i in range(0, len(words)):
		if words[i] in all_names:
			first_name = words[i]
			if i+1 < len(words):
				last_name = words[i+1]
				full_name = first_name.title() + " " + last_name.title()
				if full_name in wikipedia.search(full_name) or full_name + " (actor)" in wikipedia.search(full_name):
					print full_name
					tweet_names.append(full_name)
			else:
				tweet_names.append(first_name)
	return tweet_names

print get_names(strdata)
