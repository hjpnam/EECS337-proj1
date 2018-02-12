import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from sets import Set
from difflib import SequenceMatcher
import wikipedia
import urllib2

tmdb = json.load(urllib2.urlopen("https://api.themoviedb.org/3/discover/movie?api_key=2dc7ef3006499011242fcfbe603339e2&language=en-US&sort_by=popularity.desc&include_adult=true&include_video=false&primary_release_year=2017&vote_average.gte=6.5"))


OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

data = json.load(open('gg2018.json'))
data = [tweet['text'] for tweet in data]

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	#tweet = re.sub(r"#\S+", "", tweet)
	#tweet = re.sub(r"@\S+", "", tweet)
	word_tokens = word_tokenize(tweet)
	stop_words = Set(stopwords.words('english')) | Set(["GoldenGlobes", 'goldenglobes', 'Goldenglobes', 'Golden','golden','globes','Globes', 'RT', 'I', "Oscars", "oscars", "Awards", "awards","!",",",".","?",":",';',"#","@"])

	filtered = [w for w in word_tokens if not w in stop_words]
	return filtered

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

print get_names(tokenized_data)

def extract_award_tweets():
	helper_words = set(['Drama', 'drama', 'Performance', 'performance', 'Best', 'best', 'Original', 'original', 'Screenplay', 'screenplay', 'Director', 'director', 'Role', 'role', 'Score', 'score', 'Song', 'song', 'actor', 'Actor', 'Actress', 'actress', 'Comedy','comedy', 'Musical', 'musical', 'Feature', 'feature', 'supporting','Supporting', 'Foreign', 'foreign', 'animated','Animated', 'Picture', 'picture', 'Motion', 'motion', 'Language', 'language', 'Director', 'director', 'Mini-series', 'mini-series', 'mini','Mini'])

	award_tweets = []

	for tweet in data:
		tweet = process_tweet(tweet)
		if (len(set(tweet)&(helper_words)) >= 2):
			award_tweets.append(tweet)

	return award_tweets

def extract_awards():
	helper_words = set(['Drama', 'drama', 'Performance', 'performance', 'Best', 'best', 'Original', 'original', 'Screenplay', 'screenplay', 'Director', 'director', 'Role', 'role', 'Score', 'score', 'Song', 'song', 'actor', 'Actor', 'Actress', 'actress', 'Comedy','comedy', 'Musical', 'musical', 'Feature', 'feature', 'supporting','Supporting', 'Foreign', 'foreign', 'animated','Animated', 'Picture', 'picture', 'Motion', 'motion', 'Language', 'language', 'Director', 'director', 'Mini-series', 'mini-series', 'mini','Mini'])
	award_tweets = extract_award_tweets()
	awards = []
	for tweet in award_tweets:
		i = len(tweet) - 1
		for helper in helper_words:
			if helper in tweet:
				j = tweet.index(helper)
				if j < i:
					i = j
		arr = []
		for word in tweet:
			if word in helper_words and tweet.index(word) >= i:
				arr.append(word.lower())

		awardStr = ' '.join(arr)
		if awardStr not in awards:
			awards.append(awardStr)
	for award in awards:
		if awards.split()[0] != 'best':
			awards.remove(award)

	return awards
