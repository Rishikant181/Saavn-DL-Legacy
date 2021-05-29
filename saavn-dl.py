# This is a downloader for JioSaavn that works by making some http request to JioSaavn

import os
import meta
import fetcher
import argparse
from moviepy.editor import AudioFileClip

class Main:
    # The constructor
    def __init__(self, args):
        self.url = args['url']                                             # To store song/playlist url
        self.quality = args['quality']                                     # To store song quality
        self.fetch = fetcher.Fetcher()                                       # To store object of fetcher class

    # Method to download each song
    def downloadSong(self):
        metaData = self.fetch.download(self.url)
        curSong = metaData['title']

        # Converting raw song to mp3
        audioFile = AudioFileClip('temp.mp4')
        audioFile.write_audiofile((curSong + '.mp3'), bitrate=(str(125 * self.quality * 2) + "k"))

        # Embedding metaData in mp3
        Meta = meta.Metadata(curSong, metaData)
        Meta.embbed()    

        # Deleting raw song and cover art
        os.remove('temp.mp4')
        os.remove('temp.jpg')

    # Method to download a playlist
    def downloadPlaylist(self):
        playList = self.fetch.getSongsFromPlaylist(self.url)
        
        # Iterating through playlist
        for song in playList:
            # Getting url of each song
            self.url = song['perma_url']
        
            # Downloading each song
            self.downloadSong()

    # Method to check if url is single song or playlist
    def isPlaylist(self):
        # If single song
        if(self.url.index(".com/song/") != -1):
            return False
        # If playlist
        else:
            return True

    # Method to download song using either downloadPlaylist or downloadSong method
    def download(self):
        # If playlist
        if(self.isPlaylist() == True):
            self.downloadPlaylist()
        # If single sone
        else:
            self.downloadSong()

# Method to parser arguments
def parseArgs():
    # Creating argument parser
    parser = argparse.ArgumentParser()

    # Adding arguments
    parser.add_argument("-u", "--url", help="The URL of the song or playlist to download", type=str)
    parser.add_argument("-q", "--quality", help="Set quality of downloaded song, 0 for 128 Kbps, 1 for 256 Kbps, 2 for 320 Kbps", type=int, default=3)

    # Parse args then return
    return parser.parse_args()

# The main method
def main():
    # Get parsed args
    args = parseArgs()
    
    # Creating main class object
    ob = Main(args.__dict__)

    # Downloading song
    ob.download()        

# Executing main method
if(__name__ == '__main__'):
    main()