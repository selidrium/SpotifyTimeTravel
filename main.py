from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = "http://example.com/callback/"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read playlist-modify-public"))
user_key = sp.current_user()["id"]
play_result = sp.user_playlists(user=user_key)
sp.user_playlist_create(user=user_key, name="test_playlist")
play_list_id = play_result["items"][0]["id"]

date = input("Insert date: ")
# date = "2000-05-13"
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, "html.parser")
results = soup.select("li ul li h3")
song_names = [result.text.strip() for result in results]

# it would be better to call add item with a list of all the track_id
for song_name in song_names:
    song_search_result = sp.search(q=song_name)
    track_id = song_search_result["tracks"]["items"][0]["id"]
    sp.playlist_add_items(play_list_id, [track_id], position=None)