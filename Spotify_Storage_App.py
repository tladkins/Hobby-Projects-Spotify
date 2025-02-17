from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyodbc 
from datetime import datetime

index = 0
# Replace with your credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:/callback' 

# Create an OAuth2 instance
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    redirect_uri=REDIRECT_URI, 
    scope="user-top-read"
))

current_favs = sp.current_user_top_tracks(limit = 20, time_range = "short_term")

current_date = datetime.now().strftime("%Y-%m-%d")

connection_string = "Driver=SQL Server Native Client 11.0; Server=YOUR_SERVER; Database=dbSpotifyData; Trusted_Connection=yes;"

with pyodbc.connect(connection_string) as cnxn:
        with cnxn.cursor() as cursor:
            index = (1 + cursor.execute("Select Top 1 intSongID From TSongs ORDER BY intSongID DESC").fetchval())
cursor.close()

for item in current_favs['items']:
    name = item['name']
    artist = item['artists']
    #insert values into the table
    with pyodbc.connect(connection_string) as cnxn:
        with cnxn.cursor() as cursor:
            cursor.execute("INSERT INTO TSongs (intSongID, strSongName, strArtist, dtmListenedDate) VALUES (?, ?, ?, ?)", index, name, artist[0]['name'], current_date)
    cursor.close()
    index += 1
