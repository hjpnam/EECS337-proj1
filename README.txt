# EECS 337 Project: Golden Globes

## Group Members
Allison Sun (ast760), Sameena Khan (ssk409), Peter Nam (hjn483), William Ho (wch002)

## 3rd Party Packages Imported and Installation Instructions:
 - nltk (pip install nltk)
 - nltk.tokenize (pip install nltk.tokenize)
 - requests (pip install requests)
 - wikipedia (pip install wikipedia)

## To Run
Coded and tested with Python 2.7.

To run, give the command:
```
python proj1.py
```
to start the `main` function. This will load the JSON file and start parsing tweets, printing out relevant messages.

Options you may set at the top of `proj1.py`:
```
GG_File => the relative path to the Golden Globes JSON file.
TMDB_QUERY => set to True if you would like to update The Movie Database (TMDB) JSON local file. Sends multiple API Requests.
MOVIE_YEAR => the year you would like to retrieve movies/TV shows from TMDB (TMDB_QUERY must be set to True).
ENABLE_EXTRA_QUERIES => set to True if you would like to get results for most popular and other miscelleous categories.
```
