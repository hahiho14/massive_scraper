import os
import sys
import base64
import requests
import pandas as pd
from urllib.parse import quote

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from my_env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SONG_CATALOG_PATH


class SpotifyScraperAPI:
    def __init__(self, client_id, client_secret, song_catalog_path):
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.access_token = self.get_access_token()
        self.song_catalog = self.load_song_catalog(SONG_CATALOG_PATH)
    
    def get_access_token(self):
        """
        Retrieves an access token from Spotify API using client credentials.
        
        Returns:
            str: Access token for Spotify API.
        """
        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        }
        data = {
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(auth_url, headers=headers, data=data)
        response_data = response.json()
        
        if response.status_code == 200:
            return response_data['access_token']
        else:
            raise Exception(f"Failed to get access token: {response_data.get('error_description')}")
    
    def load_song_catalog(self, csv_path):
        """
        Loads song catalog data from a CSV file into a DataFrame.
        
        Args:
            csv_path (str): Path to the CSV file containing song catalog data.
        
        Returns:
            DataFrame: DataFrame containing the song catalog.
        """
        try:
            return pd.read_csv(csv_path, nrows=3)
        except Exception as e:
            raise Exception(f"Failed to load song catalog: {str(e)}")
    
    def preprocess_text(self, text):
        """Preprocesses and URL-encodes text."""
        return quote(str(text)) if text else ""
    
    def generate_query_params(self, row):
        """Generates query parameters for a given catalog row."""
        artist = self.preprocess_text(row['ORIGINAL ARTIST'])
        song_title = self.preprocess_text(row['SONG TITLE'])
        
        # Construct the query string
        query_parts = []
        if song_title:
            query_parts.append(f"remaster track:{song_title}")
        if artist:
            query_parts.append(f"artist:{artist}")
        
        # Join parts to form the final 'q' parameter
        query = " ".join(query_parts)
        
        # Construct the params dictionary
        return {
            "q": query,
            "type": "track",
            "market": "ID",
            "limit": 10
        }
    
    def search_tracks(self, params):
        """
        Searches for tracks on Spotify based on query parameters.
        
        Args:
            params (dict): Dictionary containing search parameters.
        
        Returns:
            dict: JSON response containing track data.
        """
        search_url = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(search_url, headers=headers, params=params)
        
        print(f"Request URL: {response.url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            print(f"Failed to fetch tracks: {response.status_code}")
            return {}
    
    def search_tracks_from_catalog(self):
        """
        Searches for tracks using the song catalog loaded from CSV.
        
        Returns:
            list: List of tracks found on Spotify.
        """
        found_tracks = []
        for index, row in self.song_catalog.iterrows():
            params = self.generate_query_params(row)
            if params["q"]:  # Only search if there's a query
                print(f"Searching for: {params['q']}")
                response = self.search_tracks(params)
                
                # Extract track items if available
                tracks = response.get("tracks", {}).get("items", [])
                found_tracks.extend(tracks)
                
        print(found_tracks)
        return found_tracks

# if __name__ == "__main__":
#     # Spotify API credentials
#     client_id = SPOTIFY_CLIENT_ID
#     client_secret = SPOTIFY_CLIENT_SECRET
#     csv_path = SONG_CATALOG_PATH
#     spotify_api = SpotifyScraperAPI(client_id, client_secret)
#     found_tracks = spotify_api.search_tracks_from_catalog()
#     # spotify_api.print_tracks("rock")
    
#     print(f"Total found tracks: {len(found_tracks)}")
#     for track in found_tracks:
#         print(f"Track Name: {track['name']} - Artist: {track['artists'][0]['name']}")
