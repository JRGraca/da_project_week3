#!/usr/bin/env python
# coding: utf-8

# In[76]:


"""This workflow produces a Spotify playlist in the specified user's account based on recommendations
of three randomly selected genres"""


# In[77]:


import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import random
from datetime import datetime
import time

# Opens a file with the format "Client ID:<CLIENT ID>\nClient Secret:<CLIENT SECRET>\n"
# and accesses Spotify with those credentials (that last line break MUST be there or IT WON'T WORK)

secret_file_name = "spotify_creds.txt"

secrets_dict = {}

secret_file = open("spotify_creds.txt")

for line in secret_file:
	key, val = line.split(":")
	secrets_dict[key] = val[:-1]

secret_file.close()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=secrets_dict["Client ID"],
                                               client_secret=secrets_dict["Client Secret"],
                                               redirect_uri="https://localhost:8080/callback",
                                               scope=["user-library-read,playlist-modify-private,playlist-modify-public,user-read-playback-state,user-modify-playback-state"]))


# In[78]:


username = "bogpoet"


# In[79]:


# gets the entire list of genres from Spotify
genres = sp.recommendation_genre_seeds()


# In[80]:


# defines genre lists for each mood and picks five at random to create the playlist
city_mood = ['acoustic',
  'ambient',
  'bluegrass',
  'blues',
  'bossanova',
  'chill',
  'classical',
  'piano',
  'r-n-b',
  'rainy-day',
  'soul'
]

open_road_mood = [  'anime',
  'country',
  'folk',
  'funk',
  'groove',
  'happy',
  'holidays',
  'indie-pop',
  'k-pop',
  'party',
  'pop',
  'reggae',
  'rockabilly',
  'romance',
  'sertanejo',
  'show-tunes',
  'summer',
  'world-music'
]

wake_up_mood = ['alt-rock',
  'death-metal',
  'deep-house',
  'electro',
  'electronic',
  'grindcore',
  'hard-rock',
  'heavy-metal',
  'metal',
  'metalcore',
  'power-pop',
  'progressive-house',
  'punk-rock',
  'samba',
  'techno',
  'work-out',
]

wake_up_selection = random.choices(wake_up_mood, k=5)
open_road_selection = random.choices(open_road_mood, k=5)
city_selection = random.choices(city_mood, k=5)

playlist_genre_selection = [city_selection, open_road_selection, wake_up_selection]
playlist_titles = ["City Mood", "Open Road Mood", "Wake Up! Mood"]


# In[81]:


#gets the predicted time for each segment of the trip to limit the time of the corresponding playlist

max_dur = [2, 2, 2]

max_duration = []

for i in max_dur:
	h = int(i/60)
	m = int(i%60)
	max_duration.append(str(h)+":"+str(m))

print(max_duration)

max_duration_ms = []

for i in max_duration:
	ts = datetime.strptime(i, '%H:%M')
	max_duration_ms.append(ts.hour * 3600000 + ts.minute * 60000)

print(max_duration_ms)


# In[82]:


playlist_ids = []
for i in range(len(playlist_genre_selection)):
	pl_title = playlist_titles[i]
	md = max_duration_ms[i]
	total_duration = 0
	recs = sp.recommendations(seed_genres=playlist_genre_selection[i], country='PT', limit=100)
	target_playlist = sp.user_playlist_create(username, name=pl_title)
	rec_id_list = []
	j = 0
	while total_duration < md:
		rec_id_list.append(recs["tracks"][j]["id"])
		total_duration += recs["tracks"][j]["duration_ms"]
		j += 1
	sp.playlist_add_items(target_playlist["id"], rec_id_list)
	playlist_ids.append(target_playlist["id"])


# In[83]:


device_list = sp.devices()
#TODO: Maybe alternative to choose genres


# In[84]:


for i in range(len(playlist_ids)):
	sp.start_playback(device_id=device_list["devices"][0]["id"], context_uri="spotify:playlist:"+playlist_ids[i])
	time.sleep(max_duration_ms[i]/1000)
	
	


# In[ ]:




