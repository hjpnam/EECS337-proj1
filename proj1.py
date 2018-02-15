import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from AwardCounter import *
from results import *


OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

data = json.load(open('gg2018.json'))
data = [tweet['text'] for tweet in data[400000:405000]]

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	#tweet = re.sub(r"#\S+", "", tweet)
	#tweet = re.sub(r"@\S+", "", tweet)
	word_tokens = word_tokenize(tweet)
	stop_words = set(stopwords.words('english')) | set(["GoldenGlobes", 'goldenglobes', 'Goldenglobes', 'Golden','golden','globes','Globes', 'RT', 'I', "Oscars", "oscars","!",",",".","?",';',"#","@"]) - set(['in','In','Out','out','by','By','for','For','From','from','over','Over','under','Under'])

	filtered = [w for w in word_tokens if not w in stop_words]
	return ' '.join(filtered)

def extract_award_tweets():
	helper_words = set(['Drama', 'drama', 'Performance', 'performance', 'Best', 'best', 'Original', 'original', 'Screenplay', 'screenplay', 'Director', 'director', 'Role', 'role', 'Score', 'score', 'Song', 'song', 'actor', 'Actor', 'Actress', 'actress', 'Comedy','comedy', 'Musical', 'musical', 'Feature', 'feature', 'supporting','Supporting', 'Foreign', 'foreign', 'animated','Animated', 'Picture', 'picture', 'Motion', 'motion', 'Language', 'language', 'Director', 'director', 'Mini-series', 'mini-series', 'mini','Mini'])

	award_tweets = []

	for tweet in data:
		tweet = process_tweet(tweet)
		if (len(set(tweet)&(helper_words)) >= 2):
			award_tweets.append(tweet)

	return award_tweets

def get_winners(tweets):
	presenters = AwardCounter()
	winners = AwardCounter()
	presenters_result = {}
	winners_result = {}
	nominees_result = {}
	
	for award in OFFICIAL_AWARDS:
		presenters.add_award(award)
		winners.add_award(award)
		
	for tweet in tweets:
		for award in OFFICIAL_AWARDS:
			if award in tweet:
				proper_nouns = get_proper_nouns(tweet)
				if "present" in tweet or "Present" in tweet:
					for noun in proper_nouns:
						presenters.increment(award,noun)
				else:
					for noun in proper_nouns:
						winners.increment(award, noun)
		
	for award in OFFICIAL_AWARDS:
		presenters_result[award] = presenters.get_max_actor(award)[0]
		winners_result[award] = winners.get_max_actor(award)[0]
		nominees_result[award] = winners.get_max_n_actors(award, 5)
	for 
	
	return presenters_result, winners_result, nominees_result
'''
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
'''

