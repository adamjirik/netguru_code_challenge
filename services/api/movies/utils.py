import datetime
from decimal import Decimal
import requests
import os

def make_request_to_omdb(title):
    r = requests.post(f"http://www.omdbapi.com/?apikey={os.getenv('API_KEY')}&t={title}")
    json = r.json()
    return json

def format_omdb_response(old):
    new_movie = dict((key.lower(), value) for (key, value) in old.items())
    # ratings = new_movie.pop('ratings')
    if 'ratings' in new_movie.keys():
        new_ratings = []
        for rating in new_movie['ratings']:
            new_rating = dict((key.lower(), value) for (key, value) in rating.items())
            new_ratings.append(new_rating)
        new_movie['ratings'] = new_ratings
    if 'response' in new_movie.keys():
        new_movie.pop('response')
    return new_movie

def format_movie_fields(movie):
    for key in movie.keys():
        if movie[key] == 'N/A':
            movie[key] = None
            continue
        if key == "released" or key == "dvd":
            dt = datetime.datetime.strptime(movie[key], '%d %b %Y')
            date = datetime.date(day=dt.day, month=dt.month, year=dt.year)
            movie[key] = date
        if key == "imdbvotes":
            movie[key] = int(movie[key].replace(',', ''))
        if key == 'imdbrating':
            movie[key] = Decimal(movie[key])
        if key == 'runtime':
            movie[key] = int(movie[key].replace(' min', ''))
        if key == 'boxoffice':
            movie[key] = movie[key] = movie[key].replace('$', '')
            movie[key] = movie[key].replace(',', '')
            movie[key] = int(movie[key])
    return movie

def make_request_and_format(title):
    json = make_request_to_omdb(title)
    movie = format_omdb_response(json)
    movie = format_movie_fields(movie)
    return movie
