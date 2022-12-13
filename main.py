from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "Your Spotify Client ID"
CLIENT_SECRET = "Your Spotify Client Secret Key"

################################## Scraping Billboard 100 ##################################
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(url="https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
titles = soup.select(selector="div li ul li h3")
songs_names = [title.getText().replace("\n", "").replace("\t", "") for title in titles]

################################## Spotify Authentication ##################################
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback/",
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        show_dialog= True,
        cache_path= "token.txt"
    )
)
user_id = sp.current_user()["id"]

################################## Searching Spotify for songs by title ##################################
songs_uris = []
year = date.split('-')[0]
for song in songs_names:
    result = sp.search(q= f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist in Spotify. Skipped")

############################# Creating a new private playlist in Spotify ##################################
playlist = sp.user_playlist_create(user= user_id, name= f"{date} Billboard 100", public=False, description='')

############################## Adding songs found into the new playlist ##################################
sp.user_playlist_add_tracks(user= user_id, playlist_id= playlist["id"], tracks= songs_uris, position=None)