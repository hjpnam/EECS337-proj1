import nltk
import re
import wikipedia
from collections import Counter
from MovieDBRequests import *


def remove_duplicates(tweets):
    return list(set(tweets))

#tmdb = getMovies({'include_adult':True, 'primary_release_year':2017, 'vote_average.gte':6.0}, save=True)
def get_people_names(words):
    # input: array of strings
	# names = nltk.corpus.names
	# all_names = names.words('male.txt') + names.words('female.txt')
	# all_names = [name.lower() for name in all_names]
    #
	# tweet_names= []
    #
	# for i in range(0, len(words)):
	# 	if(words[i] == '@'):
	# 		tweet_names.append(words[i+1])
	# 	if words[i].lower() in all_names:
	# 		first_name = words[i]
	# 		if i+1 < len(words):
	# 			last_name = words[i+1]
	# 			full_name = first_name.title() + " " + last_name.title()
	# 			if full_name in wikipedia.search(full_name) or full_name + " (actor)" in wikipedia.search(full_name):
	# 				tweet_names.append(full_name)
	# 		else:
	# 			tweet_names.append(first_name)
	# return tweet_names

    stopwords = ['Award', 'Golden', 'Globes', 'Television', 'Series', 'Motion', 'Picture', 'Actress', 'Actor', 'The', 'Best', 'In', 'And', 'Of', 'Drama', 'Role', 'Supporting', 'Speech', 'New', 'San', 'Their', 'Billboards', 'Blog', 'Amen', 'Watch', 'Gossip', 'Woman', 'Man']
    joined = ' '.join(words)
    proper = re.findall('([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', joined)
    names = []

    for i in range(0, len(proper)):
        local = proper[i]
        if 'Mc' in proper[i]:
            local = local + proper[i+1]
            i += 1
        splitted = local.split(' ')
        if (len(splitted) != 2 or splitted[0] in stopwords or splitted[1] in stopwords):
            continue

        result = wikipedia.search(local)
        if len(result) != 0 and local in result[0]:
            print('adding 1')
            names.append(local)
            continue

        result = wikipedia.search(local + " (actor)")
        if len(result) != 0 and local + " (actor)" in result[0]:
            print('adding 2')
            names.append(local)
            continue

    return names


def get_movie_names_simple(tweet):
    capitalized_words = []
    movie_words = []
    tmdb = json.load(open('./files/movies.json'))
		movie = []
    if '\'' in tweet:
        capitalized_words = set(re.findall('([A-Za-z]+\s[A-Za-z]+\'[a-z]\s[A-Za-z]+)', tweet))
    else:
        capitalized_words = set(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)', tweet))

    for words in capitalized_words:
        # need to ignore prepositions, "the", people names
        movie_words.append(words)
    if (' '.join(movie_words) in tmdb.keys()):
        movie.append(' '.join(movie_words))
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
