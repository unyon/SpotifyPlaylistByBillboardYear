from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_ID = YOUR UNIQUE CLIENT ID,
SPOTIFY_SECRET = YOUR UNIQUE CLIENT SECRET,
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="user-library-read playlist-modify-private playlist-modify-public"))
#GET CURRENT USER SPOTIFY ID
results = sp.current_user()
cu_id = results['id']

#GET DATE FROM USER
date = input("Which year do you want to travel back to? Type in this format YYYY-MM-DD")
year = date.split("-")[0]

#CREATE NBW SPOTIFY PLAYLIST
playlist = sp.user_playlist_create(user=cu_id, name=f"{date} Billboard 100", public=False)

#BILLBOARD WEBSITE
bb_url = "https://www.billboard.com/charts/hot-100/" + date
print(bb_url)
response = requests.get(url=bb_url)
bb_web_page = response.text

#GET SONG TITLES
song_list = []
soup = BeautifulSoup(bb_web_page, "html.parser")
songs = soup.find_all("h3", class_="a-no-trucate")
for song in songs:
    song_list.append(song.string.strip())

#GET SONG URIS
song_uris = []
for song in song_list:
    print(song)
    song_uri = sp.search(q="track:" + song + " year:" + year, limit=1, offset=0, type="track", market=None)
    print(song_uri)
    if len(song_uri['tracks']['items']):
        song_id = song_uri['tracks']['items'][0]['uri']
        song_uris.append(song_id)
    else:
        print("Song not found")

#ADD SONGS TO PLAYLIST
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
