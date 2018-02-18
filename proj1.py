import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from AwardCounter import *
from MovieDBRequests import *
from results import *


def tokenize_awards():
	stop_words = set(['Motion', 'motion', 'performance','Performance', 'by','By','an','An', 'a', 'role','Role','A','original','Original','series','Series','for','For',u'\u2013','in','In','Or','or','Award','award'])
	awards = get_awards()
	tokenized_awards = []
	for i in range(len(awards)):
		tk = word_tokenize(awards[i].lower())
		tk[tk.index('television')] = 'tv'
				
		tokenized_awards.append(set(tk) - stop_words)
	return tokenized_awards

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	tweet = re.sub(r"#\S+", "", tweet)
	#tweet = re.sub(r"@\S+", "", tweet)
	#stop_words = set(stopwords.words('english')) | set(["GoldenGlobes", 'goldenglobes', 'Goldenglobes', 'Golden','golden','globes','Globes', 'RT', 'I', "Oscars", "oscars","!",",",".","?",';',"#","@"]) - set(['in','In','Out','out','by','By','for','For','From','from','over','Over','under','Under'])
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

def main():
	data = json.load(open('gg2018.json'))
	#getMovies({'primary_release_year': '2017', 'vote_average.gte': '6.5'}, True)
	print get_winners(data)

main()
