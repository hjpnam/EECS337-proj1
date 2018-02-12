import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import re
from sets import Set
from difflib import SequenceMatcher
import wikipedia
from collections import Counter


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

def get_people_names(tweet):
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

def get_hosts(tweets):
    hosts = []
    cnt = Counter()
    host_names = []

    for tweet in tweets:
        if "host" in tweet or "Host" in tweet:
            host_names.append(get_people_names(tweet))

    for group in host_names:
        for name in group:
            cnt[name]+=1
	print "all hosts", host_names
    hosts = cnt.most_common(1)
    return hosts[0][0]

print get_hosts(data[0:20000])
