import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

secrets_dict = {}

secret_file = open("spotify_creds.txt")

for line in secret_file:
	key, val = line.split(":")
	secrets_dict[key] = val[:-1]

print(secrets_dict.keys())

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=secrets_dict["Client ID"],
                                               client_secret=secrets_dict["Client Secret"],
                                               redirect_uri="https://localhost:8080/callback",
                                               scope="user-library-read"))

results = sp.current_user_saved_tracks(limit=50)
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])