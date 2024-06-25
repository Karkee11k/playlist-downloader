import pytube
from youtubesearchpython import VideosSearch


class YouTube:
    """The YouTube class provides static methods to search in YouTube 
    and to download the YouTube videos."""
    
    @staticmethod
    def download(url: str, outputPath: str, onlyAudio: bool) -> None: 
        """Downloads the YouTube video of the given url.
           
           Args:
               url - URL of the YouTube video.
               outputPath - Path where to downloaded the video.
               onlyAudio - Flag to download the audio or video.       
        """
        yt = pytube.YouTube(url)

        #  if onlyAudio true, download the audio of the video
        #  else download the video
        if onlyAudio:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()
        stream.download(outputPath)

        
    @staticmethod    
    def search(query: str) -> dict: 
        """Searches the query in YouTube.

           Args:
               query - The query to search in YouTube.     
           Returns: 
               A dictionary with the title, link and thumbnail of the 
               result video.
        """
        result = VideosSearch(query, limit=1).result()['result'][0]
        title = result['title']
        link = result['link']
        thumbnail = result['thumbnails'][0]['url']
        return {'title': title, 'link': link, 'thumbnail': thumbnail}
        
         
# Testing the code      
if __name__ == '__main__':
    while True:
        query = input('Enter: ') 
        result = YouTube.search(query)
        print('Search Result: ')
        print(f" • title: {result['title']}")
        print(f" • link: {result['link']}")
        answer = input('Want to download the audio [y/n]? ')
        if answer == 'y': 
            path = input('path: ')
            YouTube.download(result['link'], path) 
            print('Downloaded') 
        print()