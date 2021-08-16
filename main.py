from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
USER_ID = os.getenv("USER_ID")
song_list = []
all_links = []

# RETURNS DATE ENTERED BY USER
date = input("prompt that asks what year you would like to travel to in YYYY-MM-DD format: ")
year = date.split("-")[0]

# SCRAPING PART
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
web_data = response.text
soup = BeautifulSoup(web_data, "html.parser")
scope = "playlist-modify-private"
all_songs = soup.find_all(name="span", class_="chart-element__information__song")

for song in all_songs:
    song_list.append(song.string)

playlist_id = f"{date} Top 100 Songs"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_secret=CLIENT_SECRET,
                                               client_id=CLIENT_ID,
                                               redirect_uri=REDIRECT_URL))

# CREATES A NEW PLAYLIST
playlist = sp.user_playlist_create(user=USER_ID, name=playlist_id, public=False)

# STORES ALL THE URLs OF ALL THE SONGS FROM SPOTIFY INTO A LIST CALLED (all_links)
for song in song_list:
    search_result = sp.search(type="track", q=f"track:{song}, year:2010")

    # CHECKS FOR IF SONG PRESENT
    try:
        song_url = search_result["tracks"]["items"][0]["uri"]
        all_links.append(song_url)

    # PRINTS ERROR IF SONG DOESNT EXIST
    except IndexError:
        print(f"{song} Doesn't Exist")

# ADDS EACH SONG TO PLAYLIST
sp.playlist_add_items(playlist_id=playlist["id"], items=all_links)
playlist_link = playlist["external_urls"]["spotify"]


print(f"Songs Added. Link for the playlist: {playlist_link}")
