import os
import sys
import requests
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from my_env import YOUTUBE_API_KEY, SONG_CATALOG_PATH


class YouTubeScraperAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.song_catalog = self.load_song_catalog(SONG_CATALOG_PATH)

    def search_videos(self, query, limit=5, page_token=None):
        """
        Searches for YouTube videos based on a query.
        
        Args:
            query (str): Search query (e.g., artist name, track name).
            limit (int): Number of videos to retrieve per request.
            page_token (str): Token for the next page of results (for pagination).
        
        Returns:
            dict: JSON response containing video data.
        """
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": limit,
            "pageToken": page_token,
            "key": self.api_key
        }
        
        response = requests.get(search_url, params=params)
        return response.json()

    def get_video_details(self, video_ids):
        """
        Retrieves details for a list of YouTube video IDs.
        
        Args:
            video_ids (list): List of YouTube video IDs.
        
        Returns:
            dict: JSON response containing video details.
        """
        details_url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,contentDetails",
            "id": ",".join(video_ids),
            "key": self.api_key
        }
        
        response = requests.get(details_url, params=params)
        return response.json()

    def load_song_catalog(self, csv_path):
        """
        Loads song catalog data from a CSV file into a DataFrame.
        
        Args:
            csv_path (str): Path to the CSV file containing song catalog data.
        
        Returns:
            DataFrame: DataFrame containing the song catalog.
        """
        try:
            return pd.read_csv(csv_path, nrows=1)
        except Exception as e:
            raise Exception(f"Failed to load song catalog: {str(e)}")

    def search_videos_from_catalog(self):
        """
        Searches for YouTube videos using the song catalog loaded from CSV.
        
        Returns:
            list: List of video metadata dictionaries.
        """
        found_videos = []
        for index, row in self.song_catalog.iterrows():
            track_name = row['SONG TITLE']  # Adjust this to match your CSV column name
            artist_name = row['ORIGINAL ARTIST']  # Adjust this to match your CSV column name
            query = f"{track_name} {artist_name}"
            print(f"Searching for: {query}")
            videos = self.get_all_videos(query)
            found_videos.extend(videos)
        
        return found_videos

    def get_all_videos(self, query):
        """
        Retrieves all videos matching a search query and fetches details for each.
        
        Args:
            query (str): Search query to retrieve videos for.
        
        Returns:
            list: List of video metadata dictionaries with ISRC code if available.
        """
        all_videos = []
        limit = 5
        page_token = None

        while True:
            search_data = self.search_videos(query, limit=limit, page_token=page_token)
            video_ids = [item['id']['videoId'] for item in search_data.get("items", [])]
            
            if not video_ids:
                break

            # Get detailed information for each video
            video_details = self.get_video_details(video_ids)
            for video in video_details.get("items", []):
                video_data = {
                    "title": video["snippet"]["title"],
                    "channelTitle": video["snippet"]["channelTitle"],
                    "description": video["snippet"]["description"],
                    "videoId": video["id"],
                    "isrc": self.extract_isrc(video["snippet"]["description"])
                }
                all_videos.append(video_data)

            # Move to the next page of results
            page_token = search_data.get("nextPageToken")
            if not page_token:
                break

        return all_videos

    def extract_isrc(self, description):
        """
        Extracts ISRC code from the video description, if available.
        
        Args:
            description (str): Video description text.
        
        Returns:
            str: Extracted ISRC code, or None if not found.
        """
        # Simple check for ISRC code format in description (e.g., "ISRC IDxxxxxxx")
        import re
        match = re.search(r'ISRC\s?[:\-]?\s?(\b\w{2}\w{3}\d{7}\b)', description)
        return match.group(1) if match else None


# if __name__ == "__main__":
#     # YouTube API key
#     api_key = YOUTUBE_API_KEY
#     csv_path = SONG_CATALOG_PATH
#     youtube_api = YouTubeScraperAPI(api_key)
#     found_videos = youtube_api.search_videos_from_catalog()
    
#     print(f"Total found videos: {len(found_videos)}")
#     for video in found_videos:
#         print(f"Title: {video['title']} - Channel: {video['channelTitle']} - ISRC: {video.get('isrc', 'N/A')}")
