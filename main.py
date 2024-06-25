import os 
from dotenv import load_dotenv 

from spotify import SpotifyPlaylistExtracter  
from youtube import YouTube 
 

load_dotenv() 
client_id = os.getenv('ID')         
client_secret = os.getenv('SECRET') 


def main() -> None:
    """Extracts the Spotify playlist songs and search the songs in
    YouTube and downloads the audio.""" 
    playlistLink = input('Enter the Spotify playlist link: ') 
    path = input('Enter the path where to download: ')
    print()
    
    spotify = SpotifyPlaylistExtracter(client_id, client_secret)
    playlist = spotify.playlistSongs(playlistLink)
    
    for i, song in enumerate(playlist, start=1):
        print(f'{i}. {song}')
        try: 
            result = YouTube.search(song)
            print(f"Downloading {result['title']}")
            YouTube.download(
                            result['link'], 
                            path, 
                            onlyAudio=True)
        except Exception as e: 
            print(f'Error: {e}') 
        else: 
            print('downloaded.') 
        print()
        
        
if __name__ == '__main__': 
    try:        
        main() 
    except Exception as e: 
        print(f'Error: {e}')