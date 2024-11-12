import os
from settings import logger
from scraper.spotify import SpotifyScraperAPI
from scraper.youtube import YouTubeScraperAPI
from db_handler import MongoDB
from my_env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, YOUTUBE_API_KEY, \
    SONG_CATALOG_PATH

# def main():
#     # Define a sample search query
#     # search_query = "favorite song"

#     # csv_path = SONG_CATALOG_PATH

#     # Initialize and use Spotify API
#     spotify_api = SpotifyScraperAPI(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
#     mongo_handler_spotify = MongoDB(db_name="massive_scraper", collection_name="spotify_data")

#     try:
#         # Fetch and store Spotify data
#         spotify_tracks = spotify_api.search_tracks_from_catalog()  # Assuming this method exists
#         for track in spotify_tracks:
#             print(f"Track Name: {track['name']} - Artist: {track['artists'][0]['name']}")
#             mongo_handler_spotify.insert(track)
#         print("Spotify data scraped and stored.")
#         print(f"Total found tracks: {len(spotify_tracks)}")
#     finally:
#         # Close MongoDB connection for Spotify
#         mongo_handler_spotify.client.close()

#     # Initialize and use YouTube API
#     youtube_api = YouTubeScraperAPI(YOUTUBE_API_KEY)
#     mongo_handler_youtube = MongoDB(db_name="massive_scraper", collection_name="youtube_data")

#     try:
#         # Fetch and store YouTube data
#         youtube_videos = youtube_api.search_videos_from_catalog()  # Assuming this method exists
#         for video in youtube_videos:
#             print(f"Title: {video['title']} - Channel: {video['channelTitle']} - ISRC: {video.get('isrc', 'N/A')}")
#             mongo_handler_youtube.insert(video)
#         print("YouTube data scraped and stored.")
#         print(f"Total found videos: {len(youtube_videos)}")
#     finally:
#         # Close MongoDB connection for YouTube
#         mongo_handler_youtube.client.close()

# if __name__ == "__main__":
#     main()

# main.py

def main():
    # Set your Spotify API credentials and the path to the song catalog CSV file
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    catalog_path = "path_to_your_catalog.csv"  # Replace with the path to your catalog file

    # Initialize the SpotifyScraperAPI
    scraper = SpotifyScraperAPI(client_id, client_secret, catalog_path)
    
    # Search tracks based on the catalog data
    tracks = scraper.search_tracks_from_catalog()

    # Process the results
    for track in tracks:
        track_name = track.get("name", "Unknown Track")
        artists = [artist.get("name") for artist in track.get("artists", [])]
        print(f"Track: {track_name}, Artists: {', '.join(artists)}")

if __name__ == "__main__":
    main()
