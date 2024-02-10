import re 
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify 
from youtubesearchpython import VideosSearch
from pytube import YouTube


def getSongTitles(playlist, CLIENT): 
	"""Gives the list of song titles from a Spotify playlist""" 	
	credentials = SpotifyClientCredentials(client_id=CLIENT['ID'], 	client_secret=CLIENT['SECRET']) 
	
	session = Spotify(client_credentials_manager=credentials)  
    
	results = session.playlist_tracks(playlist) 
	tracks = results['items']
	
	while results['next']: 
		results = session.next(results)  
		tracks.extend(results['items']) 
		
	def format(track): 
		"""Format it like 'song_name by artist1, artist2,.. ' """ 		
		artists = ', '.join([artist['name'] for artist in track['artists']])
		return f"{track['name']} by {artists}"
	
	return [format(track['track']) for track in tracks] 
	
	
def getLinks(queries):  
	"""Gives the list of YouTube links for the given list of 
	queries"""	
	links = [] 
	for query in queries:
	   	videos_search = VideosSearch(query, limit=1)
	   	results = videos_search.result()
	   	links.append(results['result'][0]['link'])
	return links
      

def download(links, output_path=None): 
	"""Download the audios of the given YouTube links""" 	
	for link in links: 
		try:
		   yt = YouTube(link) 
		   audio = yt.streams.filter(only_audio=True).first()
		except Exception as e: 
		   print(e) 
		   print(f'video link: {link}')  
		else: 
	   	   print(f'Downloading: {yt.title}')
	   	   audio.download(output_path) 
	   	     	
	print('Download complete.')



if __name__ == '__main__':  
	"""Getting the Spotify playlist link and downloading the audios from YouTube""" 
	
	playlist_link = input('Enter the playlist link: ')    
	output_path = 'playlist' 
	CLIENT = dotenv_values('.env')
	
	if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist_link):
		playlist = match.groups()[0]
	else:
	    raise ValueError("Expected format: https://open.spotify.com playlist/...") 
	    
	try:      	
		songs = getSongTitles(playlist, CLIENT)  
		print(f'{len(songs)} song titles got')
    	
		links = getLinks(songs) 
		print(f'{len(links)} links got') 

		download(links, output_path)  
	except Exception as err: 
			print(err)
	
