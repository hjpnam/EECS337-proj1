import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from difflib import SequenceMatcher


OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

data = json.load(open('gg2018.json'))
data = [tweet['text'] for tweet in data[400000:405000]]

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	#tweet = re.sub(r"#\S+", "", tweet)
	#tweet = re.sub(r"@\S+", "", tweet)
	word_tokens = word_tokenize(tweet)
	stop_words = set(stopwords.words('english')) | set(["GoldenGlobes", 'goldenglobes', 'Goldenglobes', 'Golden','golden','globes','Globes', 'RT', 'I', "Oscars", "oscars", "Awards", "awards","!",",",".","?",":",';',"#","@"])

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



def extract_award_tweets():
	helper_words = set(['Drama', 'drama', 'Performance', 'performance', 'Best', 'best', 'Original', 'original', 'Screenplay', 'screenplay', 'Director', 'director', 'Role', 'role', 'Score', 'score', 'Song', 'song', 'actor', 'Actor', 'Actress', 'actress', 'Comedy','comedy', 'Musical', 'musical', 'Feature', 'feature', 'supporting','Supporting', 'Foreign', 'foreign', 'animated','Animated', 'Picture', 'picture', 'Motion', 'motion', 'Language', 'language', 'Director', 'director', 'Mini-series', 'mini-series', 'mini','Mini'])

	award_tweets = []

	for tweet in data:
		tweet = process_tweet(tweet)
		if (len(set(tweet)&(helper_words)) >= 2):
			award_tweets.append(tweet)

	return award_tweets

def extract_awards():
	helper_words = ['Drama', 'drama', 'Performance', 'performance', 'Best', 'best', 'Original', 'original', 'Screenplay', 'screenplay', 'Director', 'director', 'Role', 'role', 'Score', 'score', 'Song', 'song', 'actor', 'Actor', 'Actress', 'actress', 'Comedy','comedy', 'Musical', 'musical', 'Feature', 'feature', 'supporting','Supporting', 'Foreign', 'foreign', 'animated','Animated', 'Picture', 'picture', 'Motion', 'motion', 'Language', 'language', 'Director', 'director', 'Mini-series', 'mini-series', 'mini','Mini','limited','Limited','Series','series','Cecil B. DeMille Award','cecil b. demille Award', 'Cecil B. DeMille']
	
	prepositions = ['-', 'Or','or','By','by','An','an','In','in','A','a', 'any', 'Any', 'for','For','made','Made',',']
	
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
			if (word in helper_words or word in prepositions) and tweet.index(word) >= i:
				arr.append(word.lower())
			else: 
				continue
		
		if((arr[0] == 'best' or arr[0] == 'Best') and arr[-1] in helper_words):
			awardStr = ' '.join(arr)
			if awardStr not in awards:
				awards.append(awardStr)
		
	remove = []
	for i in range(0, len(awards)-1):
		for j in range(i, len(awards)):
			award1 = awards[i]
			award2 = awards[j]
			
			if(SequenceMatcher(None,award1,award2).ratio() > 0.3):
				if not('actor' in award1 and 'actress' in award2 or 'actress' in award1 and 'actor' in award2):
					remove.append(award1)
	
	remove = set(remove)
	
	for r in remove:
		if r in awards:
			awards.remove(r)
		
	return awards


	
x = extract_awards()
print (x)
print (len(x))

