import imdb
from arrapi import RadarrAPI
import arrapi.exceptions
import time


def get_movies():
    # Creating an instance of the Cinemagoer class
    ia = imdb.Cinemagoer()
    # Finding the top 100 movies
    top = ia.get_popular100_movies()
    return top


def get_100movies():
    # Creating an instance of the Cinemagoer class
    ia = imdb.Cinemagoer()
    # Finding the top 250 movies
    top = ia.get_top250_movies()
    return top[0:100]


def send_movies(movies):
    # Creating an instance of the RadarrAPI class
    baseurl = "http://192.168.1."
    apikey = ""
    radarr = RadarrAPI(baseurl, apikey)
    # Search all of these movies on radarr, and print only the ones that are aged 1 year or older
    ok_movies = []
    for movie in movies:
        if "year" not in movie:
            movie['year'] = 0
        if movie['year'] < 2022:
            print(movie['title'] + " - " + str(movie['year']))
            ok_movies.append(movie['title'])

    # Search each movie on radarr
    dw_movies = []
    for movie in ok_movies:
        time.sleep(1)
        try:
            search = radarr.search_movies(movie)[0]
        except arrapi.exceptions.NotFound:
            print("Not found : ", movie)

        else:
            print("Found : ", movie)
            dw_movies.append(search)

    # Add each movie to the download queue
    for movie in dw_movies:
        time.sleep(30)
        try:
            movie.add("/films-series/films6To/radarr", "HD - 720p/1080p - English")
        except arrapi.exceptions.Exists:
            print("Already exists : ", movie.title)
        else:
            print("Added : ", movie.title)


# elements = get_movies()
# send_movies(elements)
elements = get_100movies()
send_movies(elements)
