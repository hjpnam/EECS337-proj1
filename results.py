import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from sets import Set
from difflib import SequenceMatcher
import wikipedia
from collections import Counter

data = json.load(open('gg2018.json'))
data = [tweet['text'] for tweet in data]

def remove_duplicates(tweets):
    return list(set(tweets))

def process_tweet(tweet):
	tweet = re.sub(r"http\S+", "", tweet)
	#tweet = re.sub(r"#\S+", "", tweet)
	#tweet = re.sub(r"@\S+", "", tweet)
	word_tokens = word_tokenize(tweet)
	stop_words = Set(stopwords.words('english')) | Set(["GoldenGlobes", 'goldenglobes', 'Goldenglobes', 'Golden','golden','globes','Globes', 'RT', 'I', "Oscars", "oscars", "Awards", "awards","!",",",".","?",":",';',"#","@"])

	filtered = [w for w in word_tokens if not w in stop_words]
	return filtered

tweets = remove_duplicates(data[0:20000])
processed_tweets = []
for tweet in tweets:
    processed_tweets.append(process_tweet(tweet))

def get_people_names(words):
    # input: array of strings
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
print "host is", get_hosts(processed_tweets)
