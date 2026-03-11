import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os 
import csv

# Load credentials from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-top-read"

# Authenticate user
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Fetch Top 200 tracks
top_tracks = []
for offset in range(0, 200, 50):  # 0, 50, 100, 150
    results = sp.current_user_top_tracks(limit=50, offset=offset, time_range='long_term')
    top_tracks.extend(results['items'])

top_tracks = top_tracks[:-1]
print(f"Fetched {len(top_tracks)} top tracks.")

# Write CSV including duration_ms and track id
with open("top_200_tracks.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Rank", "Track Name", "Artists", "Album",
        "Duration (ms)", "Track ID"
    ])

    for idx, track in enumerate(top_tracks, start=1):
        artists = ', '.join([a['name'] for a in track['artists']])
        writer.writerow([
            idx,
            track['name'],
            artists,
            track['album']['name'],
            track['duration_ms'],
            track['id']
        ])

print("Saved top 200 tracks to top_200_tracks.csv")

