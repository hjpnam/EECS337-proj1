import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from sets import Set
from difflib import SequenceMatcher
import wikipedia


OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

# data = json.load(open('gg2018.json'))
# data = [tweet['text'] for tweet in data]

tokenized_data = ["Allison", "Sun", "Meryl", "Streep", "brad", "pitt", "chris", "evans", "Golden", "Globes" "sameena", "william", "peter"]

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	#tweet = re.sub(r"#\S+", "", tweet)
	#tweet = re.sub(r"@\S+", "", tweet)
	word_tokens = word_tokenize(tweet)
	stop_words = Set(stopwords.words('english')) | Set(["GoldenGlobes", 'goldenglobes', 'Goldenglobes', 'Golden','golden','globes','Globes', 'RT', 'I', "Oscars", "oscars", "Awards", "awards","!",",",".","?",":",';',"#","@"])

	filtered = [w for w in word_tokens if not w in stop_words]
	return filtered

def get_awards():
	helper_list = ['best actor','best actress','best mini-series','performance','drama']

	tokenized_data = ["Allison", "Sun", "Meryl", "Streep", "brad", "pitt", "chris", "evans", "Golden", "Globes" "sameena", "william", "peter"]

def get_names(words):
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
# print get_names(tokenized_data)


def filter_tweets(tweets, keywords):
	keyword_tweets = []
	for tweet in tweets:
		for word in keywords:
			if word in tweet:
				keyword_tweets.append(tweet)
	return keyword_tweets

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

	for key, values in award_nominees.iteritems():
        # get 5 most common
