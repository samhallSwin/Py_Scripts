import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your credentials
client_id = '65108a8a6bce427cbf64c383a9b40fdc'
client_secret = '3730894a5f084191bed9647f80141910'

# Create the credentials manager
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=credentials)

token_info = credentials.get_access_token()
print(token_info)

# Replace with your artist ID
artist_id = '2WX2uTcsvV5OnS0inACecP'  # Example: Birdy

# Get the top tracks of the artist (default market is 'US')
top_tracks_results = spotify.artist_top_tracks(artist_id, country='US')

# Extract track IDs for fetching audio features
track_ids = [track['id'] for track in top_tracks_results['tracks']]

# Get audio features for the top tracks
audio_features_results = spotify.audio_features(track_ids)

# Extract and print information about the top tracks along with audio features
for track, audio_features in zip(top_tracks_results['tracks'], audio_features_results):
    print(f"Track Name: {track['name']}")
    print(f"Track ID: {track['id']}")
    print(f"Popularity: {track['popularity']}")
    print(f"Duration (ms): {track['duration_ms']}")
    print(f"Album Name: {track['album']['name']}")
    print(f"Album Release Date: {track['album']['release_date']}")
    print(f"Track Preview URL: {track['preview_url']}")
    print(f"Explicit: {track['explicit']}")

    # Get audio features
    if audio_features:
        print(f"Danceability: {audio_features['danceability']}")
        print(f"Energy: {audio_features['energy']}")
        print(f"Tempo: {audio_features['tempo']} BPM")
        print(f"Valence (positivity): {audio_features['valence']}")
        print(f"Acousticness: {audio_features['acousticness']}")
        print(f"Instrumentalness: {audio_features['instrumentalness']}")
        print(f"Liveness: {audio_features['liveness']}")
        print(f"Speechiness: {audio_features['speechiness']}")
    else:
        print("No audio features available for this track.")
    
    # Get artists involved in the track
    artist_names = [artist['name'] for artist in track['artists']]
    print(f"Artists: {', '.join(artist_names)}")
    
    # Get available markets
    print(f"Available Markets: {len(track['available_markets'])} regions\n")