import json
import os
import requests
import time
import arrapi
from arrapi import RadarrAPI
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
RADARR_BASEURL = os.getenv("RADARR_BASEURL")
RADARR_APIKEY = os.getenv("RADARR_APIKEY")
DESTINATION_FOLDER = os.getenv("DESTINATION_FOLDER")

if not all([TMDB_API_KEY, RADARR_BASEURL, RADARR_APIKEY, DESTINATION_FOLDER]):
    raise EnvironmentError("Please ensure all environment variables are set.")

DOWNLOAD_HISTORY_FILE: str = "./download_history.json"


def load_checked_movies() -> List[str]:
    """
    Loads the cache of movies already checked against Radarr from a JSON file.

    :return: List of already checked movie titles.
    """
    if os.path.exists(DOWNLOAD_HISTORY_FILE):
        with open(DOWNLOAD_HISTORY_FILE, "r") as f:
            return json.load(f)

    with open(DOWNLOAD_HISTORY_FILE, "w") as f:
        json.dump([], f)
    return []


def save_checked_movies(checked_movies: List[str]) -> None:
    """
    Saves the list of already checked movies to a JSON file.

    :param checked_movies: List of movie titles to save.
    """
    with open(DOWNLOAD_HISTORY_FILE, "w") as f:
        json.dump(checked_movies, f)


def get_tmdb_trending_movies(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Fetches trending movies from TMDb API.

    :param limit: Number of trending movies to fetch.
    :return: A list of dictionaries, each containing the title and year of release.
    """
    url: str = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    response: requests.Response = requests.get(url)
    response.raise_for_status()  # Raise an error for a bad response

    # Process the response
    movies: List[Dict[str, Any]] = response.json().get("results", [])[:limit]
    return [
        {"title": movie["title"], "year": movie["release_date"].split("-")[0]}
        for movie in movies
    ]


def send_movies_to_radarr(movies: List[Dict[str, Any]]) -> None:
    """
    Adds the list of movies to Radarr's download queue after checking their existence.

    :param movies: A list of dictionaries containing movie title and year to be processed.
    """
    # Initialize the Radarr API
    radarr: RadarrAPI = RadarrAPI(RADARR_BASEURL, RADARR_APIKEY)

    # Load checked movies from the cache
    checked_movies: List[str] = load_checked_movies()

    # Filter out already checked movies
    ok_movies: List[str] = [
        movie["title"] for movie in movies if movie["title"] not in checked_movies
    ]

    newly_checked_movies: List[str] = []
    dw_movies: List[RadarrAPI.Movie] = []

    # Search for each movie in Radarr and append to the download list if found
    for movie in ok_movies:
        time.sleep(5)  # To avoid API rate limits
        try:
            search: RadarrAPI.Movie = radarr.search_movies(movie)[0]
        except arrapi.exceptions.NotFound:
            print(f"Not found: {movie}")
        else:
            print(f"Found: {movie}")
            dw_movies.append(search)
            newly_checked_movies.append(movie)

    # Add movies to Radarr's download queue
    for movie in dw_movies:
        time.sleep(15)  # Delay to prevent overwhelming the API
        try:
            movie.add(DESTINATION_FOLDER, "HD - 720p/1080p - English")
        except arrapi.exceptions.Exists:
            print(f"Already exists: {movie.title}")
        else:
            print(f"Added: {movie.title}")

    # Save the updated cache
    save_checked_movies(checked_movies + newly_checked_movies)


if __name__ == "__main__":
    # Fetch trending movies from TMDb
    print("Fetching trending movies from TMDb...", end=" ")
    trending_movies: List[Dict[str, Any]] = get_tmdb_trending_movies()
    print("Done!")
    

    # Process and send movies to Radarr
    print("Processing and sending movies to Radarr. This may take at least 5 minutes...", end=" ")
    send_movies_to_radarr(trending_movies)
    print("Done!")
    
    print("If this scripts has been run really fast, it may be due to the fact that the movies are already in the Radarr database.")
