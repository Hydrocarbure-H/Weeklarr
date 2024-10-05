# Radarr TMDb Trending Movie Downloader

This Python project retrieves trending movies from **The Movie Database (TMDb)** and checks if the movies already exist in **Radarr**. If a movie is not already present, it adds the movie to Radarr’s download queue in a specified folder. The script also maintains a cache of previously checked movies to avoid rechecking and reduce unnecessary API calls.
**Disclaimer:**

This project is intended for educational and personal use only. It utilizes APIs provided by **TMDb** and **Radarr** to manage movie downloads. Please ensure that you comply with all local laws, copyright regulations, and the terms of service of **TMDb** and **Radarr** when using this software. Unauthorized downloading or distribution of copyrighted content may result in legal consequences. The developer assumes no responsibility for any misuse of this tool.
## Features
- Fetches trending movies from **TMDb**.
- Uses **Radarr** API to check if the movie is already in the database.
- Automatically adds movies to Radarr’s download queue if they are not already present.
- Stores a list of already checked movies to optimize performance and avoid redundant API requests.
- Uses environment variables for sensitive information such as API keys and Radarr server details.

## Requirements

- **Python 3.x**
- **TMDb API Key**: You will need to create an account at [TMDb](https://www.themoviedb.org/) and obtain an API key.
- **Radarr**: An instance of Radarr running and accessible from the machine running the script.

### Required Python Packages

Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

Here are the required libraries:

- `arrapi`: To interact with the Radarr API.
- `requests`: For making HTTP requests to the TMDb API.
- `python-dotenv`: For loading environment variables from a `.env` file.

## Setting Up

### Environment Variables

Create a `.env` file in the root directory of your project to store your environment variables:

```
TMDB_API_KEY=your_tmdb_api_key
RADARR_BASEURL=http://your_radarr_url
RADARR_APIKEY=your_radarr_api_key
DESTINATION_FOLDER=/path/to/your/destination/folder
```

### Example `.env` File:
```plaintext
TMDB_API_KEY=12345abcde
RADARR_BASEURL=http://192.168.1.67:7878
RADARR_APIKEY=f27f0463981940dd8848e95eeca51e65
DESTINATION_FOLDER=/films-series/films6To/radarr
```

Make sure the `.env` file is added to your `.gitignore` to avoid committing sensitive information.

## How It Works

1. **Fetch Trending Movies**: The script fetches trending movies from the TMDb API using the `get_tmdb_trending_movies()` function. You can specify how many movies to retrieve by setting the `limit` parameter.
   
2. **Check Radarr Database**: It then checks Radarr to see if the movies are already in your collection using the `radarr.search_movies()` method. If a movie is found, it skips the addition. If the movie is not found, it adds the movie to Radarr's download queue.
   
3. **Download Queue**: The script adds new movies to the download queue using the `movie.add()` method with a specified destination folder.

4. **Cache**: The script stores previously checked movies in `download_history.json`, so it won’t recheck the same movies in subsequent runs.

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/radarr-tmdb-downloader.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Script**:
   ```bash
   python weeklarr.py
   ```

4. The script will fetch the latest trending movies from TMDb and check Radarr for existing movies. Movies that are not found will be added to the download queue.

## Example Output

```
Fetching trending movies from TMDb... Done!
Processing and sending movies to Radarr. This may take at least 5 minutes... 
Found: The Platform 2
Found: Joker: Folie à Deux
Added: The Platform 2
Done!
If this script has run really fast, it may be due to the fact that the movies are already in the Radarr database.
```

## Customization

- **Change the number of movies to fetch**: Modify the `limit` parameter in the `get_tmdb_trending_movies()` function to change how many movies are retrieved from TMDb.
  
- **Modify download quality**: Adjust the quality in the `movie.add()` call (`HD - 720p/1080p - English` in the example) to set the desired resolution and language for downloaded movies.

## Disclaimer

This project is intended for educational purposes only. Please ensure that you comply with TMDb's and Radarr's terms of service when using their APIs. Unauthorized downloading of copyrighted material may violate local laws and regulations.
