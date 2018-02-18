import requests
import json, io, time

api_key = "2dc7ef3006499011242fcfbe603339e2"
defaults = {"lanaguage": "en-US", "include_adult": "true", "include_video": "false"}

'''
Basic GET request that can also save movie data locally for faster retrieval.
By default, only English, adult, non-inclusive video movies are included in the request.
It is ASSUMED that all requests will be from page 1. Failure to do so may lead to duplicate and/or missing entries.

@param attributes: the dictionary of attributes that we want to filter the request by.
@param save: true if we want to save locally; default is false.
@param default: the default attributes of the request.
@return a dictionary of movie names mapped to a list of their genre IDs; None if an error has occured.
'''
def getMovies(attributes = {}, save = False, default = defaults):

    url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key

    for attribute, value in default.items():
        url += "&" + str(attribute) + "=" + str(value)

    for attribute, value in attributes.items():
        url += "&" + str(attribute) + "=" + str(value)

    data = requests.get(url)

    if data.status_code != 200:
        return None

    content = json.loads(data.content.decode('utf-8'))
    totalPages = content["total_pages"]

    movies = {}

    for movie in content["results"]:
        movies[movie["title"]] = movie["genre_ids"]

    if totalPages != 1:
        for i in range(2, totalPages + 1):
            print(i)
            url += "&page=" + str(i)
            if (i % 25 == 0):
                time.sleep(3)
            data = requests.get(url)

            if data.status_code != 200:
                return None

            content = json.loads(data.content.decode('utf-8'))

            for movie in content["results"]:
                movies[movie["title"]] = movie["genre_ids"]

    if save:
        with io.open("./files/movies.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(movies, ensure_ascii = False))

    return movies

'''
Gets the possible genres from the movie database, keyed by ID.

@param save: true if we want to save locally; default is false.
@return a dictionary of ids mapping to genre name.
'''
def getGenres(save = False):

    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key + "&language=en-US"
    data = requests.get(url)

    if data.status_code != 200:
        return None

    content = json.loads(data.content.decode('utf-8'))

    genres = {}

    for genre in content["genres"]:
        genres[str(genre["id"])] = genre["name"]

    if save:
        with io.open("./files/genres.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(genres, ensure_ascii = False))

    return genres
