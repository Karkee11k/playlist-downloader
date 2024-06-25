import re
from spotipy import Spotify 
from spotipy.oauth2 import SpotifyClientCredentials 


class SpotifyPlaylistExtracter:
    """Class to get the songs of a Spotify playlist using Spotify Web API."""
    
    def __init__(self, client_id: str, client_secret: str):
        """Initialises the instance with the credentials.
        
        Args:
            client_id - Client ID to authenticate with the API.
            client_secret - Client secret to authenticate with the API.
        """
        creds = SpotifyClientCredentials(
                           client_id=client_id,
                           client_secret=client_secret) 
        self.__session = Spotify(client_credentials_manager=creds)

                                                                                                
    def playlistSongs(self, playlistLink: str) -> list:
        """Returns the playlist songs of the given playlist link.
           
           Args:
               playlistLink - URL of the Spotify Playlist.
           
           Returns:
               list: Song titles of the playlist.
        """
        playlistId = SpotifyPlaylistExtracter.__getPlaylistId(playlistLink)
        if not playlistId:
            format = 'https://open.spotify.com playlist/...'
            raise ValueError(f'Expected format: {format}')
        
        results = self.__session.playlist_tracks(playlistId) 
        tracks = results['items'] 
	     
        while results['next']:
            results = self.__session.next(results)
            tracks.extend(results['items']) 
	    
        return [SpotifyPlaylistExtracter.__formatTrack(track['track']) for track in tracks]

    
    @staticmethod   
    def __getPlaylistId(playlistLink: str) -> str: 
        """Returns playlist ID if playlist link is in correct format else None."""
        match = re.match(r'https://open.spotify.com/playlist/(.*)\?', playlistLink)
        return match.groups()[0] if match else None 

                  
    @staticmethod          
    def __formatTrack(track: dict) -> str:
        """Returns a string  like song name by artist1, artist2,.."""
        artists = ', '.join([ artist['name'] for artist in track['artists'] ])
        return f"{track['name']} by {artists}"