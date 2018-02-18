import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from AwardCounter import *
from results import *

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

#SHORT_OFFICIAL_AWARDS = ['Cecil B. Demille Award', 'Best Motion Picture Drama', 'Best Performance by an Actress in a Motion Picture Drama', 'Best Performance by an Actor in a Motion Picture Drama', 'best motion picture comedy', 'best performance by an actress in a motion picture comedy', 'best performance by an actor in a motion picture comedy', 'best animated', 'best foreign language', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director', 'best screenplay', 'best original score', 'best original song', 'best television series drama', 'best performance by an actress in a television series drama', 'best performance by an actor in a television series drama', 'best television series comedy', 'best performance by an actress in a television series comedy', 'best performance by an actor in a television series comedy', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series', 'best performance by an actor in a supporting role in a series']

def tokenize_awards():
	stop_words = set(['Motion', 'motion', 'performance','Performance', 'by','By','an','An', 'a', 'role','Role','A','original','Original','series','Series','for','For',u'\u2013','in','In','Or','or','Award','award'])
	awards = get_awards()
	tokenized_awards = []
	for i in range(len(awards)):
		tokenized_awards.append(set(word_tokenize(awards[i].lower())) - stop_words)
	return tokenized_awards

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	#tweet = re.sub(r"#\S+", "", tweet)
	#tweet = re.sub(r"@\S+", "", tweet)
	#stop_words = set(stopwords.words('english')) | set(["GoldenGlobes", 'goldenglobes', 'Goldenglobes', 'Golden','golden','globes','Globes', 'RT', 'I', "Oscars", "oscars","!",",",".","?",';',"#","@"]) - set(['in','In','Out','out','by','By','for','For','From','from','over','Over','under','Under'])
	stop_words = ['@VanityFair', '@goldenglobes', '@voguemagazine', '@BuzzFeed', '@BuzzFeedNews','@THR','@chicagotribune','@people','@EW','@e_entertainment', 'goldenglobes', 'GoldenGlobes', '@GoldenGlobes']

	for stop in stop_words:
		if stop in tweet:
			tweet.replace(stop, '')

	word_tokens = word_tokenize(tweet)


	return word_tokens
'''
def extract_award_tweets(tweets):
	helper_words = set(['Drama', 'drama', 'Performance', 'performance', 'Best', 'best', 'Original', 'original', 'Screenplay', 'screenplay', 'Director', 'director', 'Role', 'role', 'Score', 'score', 'Song', 'song', 'actor', 'Actor', 'Actress', 'actress', 'Comedy','comedy', 'Musical', 'musical', 'Feature', 'feature', 'supporting','Supporting', 'Foreign', 'foreign', 'animated','Animated', 'Picture', 'picture', 'Motion', 'motion', 'Language', 'language', 'Director', 'director', 'Mini-series', 'mini-series', 'mini','Mini'])

	award_tweets = []

	for tweet in tweets:
		tweet = process_tweet(tweet)
		if (len(set(tweet)&(helper_words)) >= 2):
			award_tweets.append(tweet)

	return award_tweets
'''
def get_winners(tweets):
	presenters = AwardCounter()
	winners = AwardCounter()
	presenters_result = {}
	winners_result = {}
	nominees_result = {}

	awards = get_awards()
	award_tokenized = tokenize_awards()

	for i in range(len(award_tokenized)):
		presenters.add_award(awards[i])
		winners.add_award(awards[i])

	for tweet in tweets:
		tweet2 = [word.lower() for word in tweet]
		for i in range(len(award_tokenized)):
			if len(set(tweet2).intersection(award_tokenized[i])) == len(award_tokenized[i]):
				proper_nouns = get_people_names(tweet)
				proper_nouns.extend(get_handle_names(tweet))
				if "present" in ' '.join(tweet2):
					for noun in proper_nouns:
						presenters.increment(awards[i],noun)
				else:
					for noun in proper_nouns:
						winners.increment(awards[i], noun)

	for award in awards:
		#presenters_result[award] = presenters.get_max_actor(award)[0]
		#winners_result[award] = winners.get_max_actor(award)[0]
		nominees_result[award] = winners.get_max_n_actors(award, 5)

	return presenters_result, winners_result, nominees_result

def get_awards():
	golden_globes = wikipedia.page("Golden Globe Award")
	awards = []

	for string in (golden_globes.section("Motion picture awards") + "\n").splitlines():
		awards.append(string)
	for string in (golden_globes.section("Television awards") + "\n").splitlines():
		awards.append(string)

	short_awards = []
	for award in awards:
		short_award = award.encode("utf-8")
		short_award = short_award.split(":", 1)[0]
		short_award = short_award.split(",", 1)[0]
		short_award = short_award.split("for Lifetime Achievement in Motion Pictures", 1)[0]
		short_award = short_award.split("Film", 1)[0]
		short_award = short_award.decode('utf-8')
		short_awards.append(short_award)
	print "short_awards len", len(short_awards)

	return short_awards

# def get_handle_names(tweets):
# 	# tweets are tokenized
# 	handles = []
# 	handle_names = []
# 	for tweet in tweets:
# 		for i in range(0,len(tweet)):
# 			if tweet[i] == "@":
# 				if i+1 < len(tweet):
# 					handle = tweet[i+1]
# 					handles.append(handle)
#
# 	for handle in handles:
# 		if handle[0].isupper():
# 			name = (''.join(' ' + x if 'A' <= x <= 'Z' else x for x in handle)).strip()
# 			handle_names.append(name)
# 	print "number of @", len(handle_names)
# 	print handle_names
# 	return handle_names

def get_handle_names(tweet):
	handles = []
	handle_names = []
	for i in range(0,len(tweet)):
		if tweet[i] == "@":
			if i+1 < len(tweet):
				handle = tweet[i+1]
				handles.append(handle)

	for handle in handles:
		if handle[0].isupper():
			name = (''.join(' ' + x if 'A' <= x <= 'Z' else x for x in handle)).strip()
			handle_names.append(name)
	return handle_names

def main():
	data = json.load(open('gg2018.json'))
	tweets = []
	print (len(data))
	for tweet in data:
		if 'RT' not in tweet['text'][0:5]:
			tweets.append(process_tweet(tweet['text']))

	#award_tweets = extract_award_tweets(tweets)
	print get_winners(tweets)
	#print(award_tweets)

main()
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
