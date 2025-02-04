import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyodbc
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

# Replace with your credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:/callback' 

# Create an OAuth2 instance
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    redirect_uri=REDIRECT_URI, 
    scope="playlist-modify-public playlist-modify-private"
))

# Create the connection string
connection_string = "Driver=YOUR_DRIVER; Server=YOUR_SERVER; Database=YOUR_SQL_DATABASE; Trusted_Connection=yes;"

# Get today's date a year ago
now = datetime.now()
todaysdate = now.date() - relativedelta(years=1)
tomorrowsdate = todaysdate + timedelta(days=1)

# Create the select string
select_string = f"""
    SELECT DISTINCT TOP 100 
        SUBSTRING(strSpotifyTrackURI, 15, 23) AS TrackURI
    FROM TSongs
    WHERE dtmTimeListened > '{todaysdate}' AND dtmTimeListened < '{tomorrowsdate}'
"""

# Execute the query and get results
with pyodbc.connect(connection_string) as cnxn:
    with cnxn.cursor() as cursor:
        cursor.execute(select_string)
        result = cursor.fetchall()

# Extract track URIs and format them correctly
uris = [f"spotify:track:{row[0].strip()}" for row in result if row[0] and row[0].strip()]

# Spotify Playlist ID
playlist_id = str('YOUR_PLAYLIST_ID')

uris = [uri for uri in uris if uri and uri.strip()]

print(uris)

urisasstring = ",".join(uris)

# for uri in uris:
resut = sp.playlist_add_items(playlist_id, urisasstring, position=None)

# # Update the playlist
# if uris:
#     sp.playlist_add_items(playlist_id, uris, 0)
# else:
#     print("No tracks found for the given time range.")
