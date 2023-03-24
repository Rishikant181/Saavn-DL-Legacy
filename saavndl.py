# This is a downloader for JioSaavn that works by making some http request to JioSaavn

import os
import meta
import fetcher
import argparse
from moviepy.editor import AudioFileClip

class Main:
    def __init__(self):
        # The fetch service instance that will be used for fetching the music
        self.fetch = fetcher.Fetcher()

    def download_single(self, url, quality):
        '''
        Download a music with the given url and quality.

        #### Parameters
            -   url (str): The url to the music to download.
            -   quality (int): The quality of the download (0 = 128 Kbps, 1 = 256 Kbps, 2 = 320 Kbps).

        '''

        # Fetching the raw music along with metadata
        music = self.fetch.download(url)

        # Setting the name of the music with the name received from metadata
        cur_track = music['title']

        # Converting raw music to mp3
        audio_file = AudioFileClip('temp.mp4')
        audio_file.write_audiofile((cur_track + '.mp3'), bitrate=(str(125 * quality * 2) + "k"))

        # Embedding meta data in mp3
        meta_data = meta.Metadata(cur_track, music)
        meta_data.embbed()    

        # Deleting residual raw music and cover art
        os.remove('temp.mp4')
        os.remove('temp.jpg')

    def download_playlist(self, url, quality):
        '''
        Download a playlist with the given url and quality.

        #### Parameters
            -   url (str): The url to the playlist to download.
            -   quality (int): The quality of the download (0 = 128 Kbps, 1 = 256 Kbps, 2 = 320 Kbps).

        '''

        # Getting the playlist from JioSaavn
        play_list = self.fetch.getSongsFromPlaylist(url)
        
        # Iterating through playlist
        for track in play_list:
            # Downloading each music track
            self.download_single(track['perma_url'], quality)

    def is_playlist(self, url):
        '''
        Checks if a given url is a playlist url or not.

        #### Parameters:
            -   url (str): The url which needs to be checked.

        #### Returns
            -   True if url is a playlist url.
            -   False if a music url.

        '''

        # If single music
        if(".com/song/" in url):
            return False
        # If playlist
        else:
            return True

    def download(self, url, quality):
        '''
        Checks if the given url is for a playlist or music.
        
        Then initiates download accordingly by calling the appropriate method.

        #### Parameters
            -   url (str): The url of the music/playlist to download.
            -   quality (int): The quality of the download (0 = 128 Kbps, 1 = 256 Kbps, 2 = 320 Kbps).

        '''

        # If the url is a playlist
        if(self.is_playlist == True):
            self.download_playlist(url, quality)
        # If the url is a music
        else:
            self.download_single(url, quality)

def parse_args():
    '''
    Parse input command-line arguments

    #### Returns
        -   The dictionary containing all parsed arguments.

    '''

    # Creating argument parser that will be used for parsing the command-line arguments
    argument_parser = argparse.ArgumentParser()

    # Adding arguments to the argument parser object
    argument_parser.add_argument("-u", "--url", help = "The URL of the music or playlist to download", type = str)
    argument_parser.add_argument("-q", "--quality", help = "Set quality of downloaded music, 0 for 128 Kbps, 1 for 256 Kbps, 2 for 320 Kbps", type = int, default = 3)

    # Parse args then return
    return argument_parser.parse_args()

# The main method
def main():
    # Getting the parsed commandline arguments
    args = parse_args()
    
    # Creating main class object
    prog = Main(args.__dict__)

    # Downloading the music/playlist with the given url and quality
    prog.download(args['url'], args['quality'])

# Executing main method
if(__name__ == '__main__'):
    main()