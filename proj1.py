import nltk
from nltk.tokenize import word_tokenize
import json
import re
import wikipedia
from AwardCounter import *
from MovieDBRequests import *
from Helpers import *

'''
GLOBAL CONTROL VARIABLES TO SET THE STATE OF THE PROGRAM.
'''
# The relative path to the Golden Globes JSON file.
GG_FILE = './gg2018.json'

# Set to True if you would like to update The Movie Database (TMDB) JSON local file. Sends multiple API Requests.
TMDB_QUERY = False

# The year you would like to retrieve movies/TV shows from TMDB (TMDB_QUERY must be set to True).
MOVIE_YEAR = '2017'

# Set to True if you would like to get results for most popular and other miscelleous categories.
ENABLE_EXTRA_QUERIES = False

####################################################################################

def tokenize_awards():
	stop_words = set(['Motion', 'motion', 'performance','Performance', 'series', 'Series', 'by','By','an','An', 'a', 'role','Role','A','original','Original','for','For',u'\u2013','in','In','Or','or','Award','award', ','])
	awards = get_awards()
	tokenized_awards = []
	for i in range(len(awards)):
		tk = word_tokenize(awards[i].lower())
		if 'television' in tk:
			tk[tk.index('television')] = 'tv'

		tokenized_awards.append(set(tk) - stop_words)
	return tokenized_awards

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	tweet = re.sub(r"#\S+", "", tweet)
	stop_words = ['@VanityFair', '@goldenglobes', '@voguemagazine', '@BuzzFeed', '@BuzzFeedNews','@THR','@chicagotribune','@people','@EW','@e_entertainment', 'goldenglobes', 'GoldenGlobes', '@GoldenGlobes', 'Goldenglobes', '@YouTube', '@TMZ', '@GMA', 'Golden Globes']

	for stop in stop_words:
		if stop in tweet:
			tweet.replace(stop, '')

	word_tokens = word_tokenize(tweet)

	return word_tokens

def get_winners(tweets):
	presenters = AwardCounter()
	winners = AwardCounter()
	presenters_result = {}
	winners_result = {}
	nominees_result = {}

	hosts = []
	cnt = Counter()
	host_names = []

	awards = get_awards()
	award_tokenized = tokenize_awards()

	for i in range(len(award_tokenized)):
		presenters.add_award(awards[i])
		winners.add_award(awards[i])

	for tweet in tweets:
		if 'RT' in tweet['text'][0:5]:
			continue
		tweet = process_tweet(tweet['text'])
		tweet2 = [word.lower() for word in tweet]
		for word in tweet:
			if "host" in word or "Host" in word:
				host_names.append(get_people_names(tweet))
				break

		for i in range(len(award_tokenized)):
			if len(set(tweet2).intersection(award_tokenized[i])) == len(award_tokenized[i]):
				if ('actor' in award_tokenized[i] or 'actress' in award_tokenized[i] or 'director' in award_tokenized[i] or 'score' in award_tokenized[i] or 'screenplay' in award_tokenized[i] or 'cecil' in award_tokenized[i]):
					proper_nouns = get_people_names(tweet)
					proper_nouns.extend(get_handle_names(tweet))
					joined = ' '.join(tweet2)
					if "present" in joined or "announc" in joined:
						for noun in proper_nouns:
							presenters.increment(awards[i],noun)
					else:
						for noun in proper_nouns:
							winners.increment(awards[i], noun)
				else:
					proper_nouns = get_movie_names_simple(tweet)
					joined = ' '.join(tweet2)
					if "present" in joined or "announc" in joined:
						for noun in proper_nouns:
							presenters.increment(awards[i], noun)
					else:
						for noun in proper_nouns:
							winners.increment(awards[i], noun)

	for group in host_names:
		for name in group:
			cnt[name]+=1
	host = (cnt.most_common(1))[0][0]

	for award in awards:
		presenters_result[award] = presenters.get_max_actor(award)[0]
		winners_result[award] = winners.get_max_actor(award)[0]
		nominees_result[award] = winners.get_max_n_actors(award, 5)

	return presenters_result, winners_result, nominees_result, host

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

	return short_awards

def get_extra(data):
    most_popular = AwardCounter()
    most_popular.add_award("Most Popular")

    designerDict = {}
    designers = ["Christian Siriano", "Zuhair Murad", "Prabal Gurung", "Marc Jacobs", "Mario Dice", "Louis Vuitton", "Gucci", "Romona Keveza", "Alberta Ferretti", "Oscar de la Renta", "Armani Prive", "Tadashi Shoji", "Atelier Versace", "Brandon Maxwell", "Christian Dior", "Miu Miu", "Genny", "Zac Posen", "Givenchy"]

    for designer in designers:
        designerDict[designer] = set()
    for tweet in data:
        if "RT" in tweet['text'][0:5]:
            continue
        tweet = process_tweet(tweet['text'])
        for designer in designers:
            tweet2 = ' '.join(tweet)
            if designer in tweet2:
                proper_nouns = get_people_names(tweet)
                for noun in proper_nouns:
                    if designer != noun:
                        designerDict[designer].add(noun)
    return designerDict

def main():

	print('Loading file...')
	data = json.load(open(GG_FILE))
	print('Number of tweets: ' + str(len(data)))

	if TMDB_QUERY:
		print('Getting movies from TMDB for: ' + MOVIE_YEAR)
		getMovies({'primary_release_year': MOVIE_YEAR, 'vote_average.gte': '6.5'}, True)

	print('Parsing tweets for relevant information...(this might take awhile)')
	results = get_winners(data)
	awards = get_awards()

	print('\n')
	print("Host is: " + results[3])
	print("\n")

	for award in awards:
		print('Award: ' + award)
		print('Presented By: ' + results[0][award])
		print('Nominees: ' + ', '.join(results[2][award]))
		print('Winner: ' + results[1][award])
		print('\n')

	if ENABLE_EXTRA_QUERIES:
		print('Getting extra categories...(this will not take that long)')
		designerDict = get_extra(data)
		for key in designerDict.keys():
			ourList = list(designerDict[key])
			if ourList == []:
				ourList = ["no one that we could find"]
			ourList = ', '.join(ourList)
			print (key + " designed the dress for " + ourList)
		# print(get_extra(data))

'''
CALL THE MAIN FUNCTION TO RUN THE PROGRAM.
'''
main()
