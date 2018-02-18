import nltk
import re
import wikipedia
from collections import Counter
import json

stopwords = ['Award', 'Golden', 'Globes', 'Television', 'Series', 'Motion', 'Picture', 'Actress', 'Actor', 'The', 'Best', 'In', 'And', 'Of', 'Drama', 'Role', 'Supporting', 'Speech', 'New', 'San', 'Their', 'Billboards', 'Blog', 'Amen', 'Watch', 'Gossip', 'Woman', 'Man', 'YouTube', 'GMA', 'TMZ', 'GDIGM', 'GG', 'GoldenGlobes', 'goldenglobes', 'Goldenglobes', 'ABC', 'GoldenGlobesTNT', 'PerezHilton', 'TwoPointConv', 'AwardsCircuit']

def get_people_names(words):

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
            names.append(local)
            continue

        result = wikipedia.search(local + " (actor)")
        if len(result) != 0 and local + " (actor)" in result[0]:
            names.append(local)
            continue

    return names


def get_movie_names_simple(tweet):
    capitalized_words = []
    movie_words = []
    tmdb = json.load(open('./files/movies.json'))
    movie = []
    if '\'' in tweet:
        capitalized_words = re.findall(r'([A-Za-z]+\s*[A-Za-z|\'?]+[a-z]\s[A-Za-z]+)', ' '.join(tweet))
    else:
        capitalized_words = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[a-z]+)*(?:\s+[A-Z][a-z]+)*)', ' '.join(tweet))

    for words in capitalized_words:
        # need to ignore prepositions, "the", people names
        movie_words.append(words)
    #if (' '.join(movie_words) in tmdb.keys()):
    #movie.append(' '.join(movie_words))

    for key in tmdb.keys():
        if key in ' '.join(movie_words):
            movie.append(key)
    return movie

def get_handle_names(tweet):
    handles = []
    handle_names = []
    for i in range(0,len(tweet)):
        if tweet[i] == "@":
            if tweet[i+1] not in stopwords:
                if i+1 < len(tweet):
                    handle = tweet[i+1]
                    handles.append(handle)

    for handle in handles:
        if handle[0].isupper():
            name = (''.join(' ' + x if 'A' <= x <= 'Z' else x for x in handle)).strip()
            name = name.replace("_", "")
            handle_names.append(name)
    return handle_names
