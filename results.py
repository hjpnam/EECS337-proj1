import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from sets import Set
from difflib import SequenceMatcher
import wikipedia
from collections import Counter

def get_people_names(words):
	names = nltk.corpus.names
	all_names = names.words('male.txt') + names.words('female.txt')
	all_names = [name.lower() for name in all_names]

	tweet_names= []

	for i in range(0, len(words)):
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

def get_people_names2(tweet):
    names = nltk.corpus.names
    all_names = names.words('male.txt') + names.words('female.txt')
    all_names = [name.lower() for name in all_names]
    words = tweet.split()
    tweet_names= []

    for i in range(len(words)):
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
# print get_people_names2("seth meyers golden globes meryl streep")

def get_movie_names_simple(tweet):
	capitalized_words = []
	movie = []

	capitalized_words = set(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)', tweet))
	for words in capitalized_words:
        # need to ignore prepositions, "the" etc.
        # not names
		movie.append(words)
	return movie
# print get_movie_names("best movie goes to Call Me By Your Name")

def get_hosts(tweets):
    hosts = []
    cnt = Counter()
    host_names = []

    for tweet in tweets:
        if "host" in tweet or "Host" in tweet:
            host_names.append(get_people_names2(tweet))

    for group in host_names:
        for name in group:
            cnt[name]+=1

    hosts = cnt.most_common(1)
    # hosts is [('Seth Meyers', 3)]
    # hosts[0] is ('Seth Meyers', 3)
    return hosts[0][0]
print get_hosts(["seth meyers hosting golden globes meryl streep", "james franco hosting", "seth meyers hosted", "Host Seth Meyers"])

def get_nominees(tweets):
	awards_nominees = {}
	awards_nominees_tweets = {}
	nominee_tweets = []
	nominee_words = ['nominee', 'nominees', 'nominating', 'nominated', 'nominates', 'Nominee', 'Nominees', 'Nominating', 'Nominated', 'Nominates']

	for award in OFFICIAL_AWARDS:
		awards_nominees[award] = []
		awards_nominees_tweets[award] = []

	nominee_tweets = filter_tweets(tweets, nominee_words)

    # go through nominee tweets, if any award is in a nominee tweet, add that nominee tweet to dictionary
	for nominee_tweet in nominee_tweets:
		if any(word in nominee_tweet for award in OFFICIAL_AWARDS):
			awards_nominees_tweets[award].append(nominee_tweet)

	# values of dict are tweets, want to clean up so only names remain
	for key, values in award_nominees_tweets.iteritems():
		for value in values:
			awards_nominees[award].append(get_names(value))

	# for key, values in award_nominees.iteritems():
        # get 5 most common
