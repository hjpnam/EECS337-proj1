import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import wikipedia
from collections import Counter
from MovieDBRequests import *

def remove_duplicates(tweets):
    return list(set(tweets))


def get_people_names(words):
    # input: array of strings
	names = nltk.corpus.names
	all_names = names.words('male.txt') + names.words('female.txt')
	all_names = [name.lower() for name in all_names]

	tweet_names= []

	for i in range(0, len(words)):
		if(words[i] == '@'):
			tweet_names.append(words[i+1])
		if words[i].lower() in all_names:
			first_name = words[i]
			if i+1 < len(words):
				last_name = words[i+1]
				full_name = first_name.title() + " " + last_name.title()
				if full_name in wikipedia.search(full_name) or full_name + " (actor)" in wikipedia.search(full_name):
					tweet_names.append(full_name)
			else:
				tweet_names.append(first_name)
	return tweet_names
	
def get_movie_names_simple(tweet):
	capitalized_words = []
	movie = []

	capitalized_words = set(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)', tweet))
	for words in capitalized_words:
        # need to ignore prepositions, "the", people names
		movie.append(words)
	return movie

	
def get_hosts(tweets):
    hosts = []
    cnt = Counter()
    host_names = []

    for tweet in tweets:
        for word in tweet:
            if "host" in word or "Host" in word:
                host_names.append(get_people_names(tweet))
                break

    for group in host_names:
        for name in group:
            cnt[name]+=1

    hosts = cnt.most_common(1)
    return hosts[0][0]

