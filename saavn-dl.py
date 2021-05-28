# This is a downloader for JioSaavn that works by making some http request to JioSaavn

# low  -128kbps-125k bitrate
# med  -256kbps-250k bitrate
# high -320kbps-500k bitrate

import os
import sys
import meta

import fetcher
from moviepy.editor import AudioFileClip

param = None                                                    # To store whether playlist or not
url = None                                                      # To store song original url
curSong = None                                                  # To store name of current song

try:
    param = sys.argv[1]
    url = sys.argv[2]
# If one param is passed
except:
    url = sys.argv[1]

fetch = fetcher.Fetcher()

# If downloading playlist
if(param == 'p'):
    playList = fetch.getSongsFromPlaylist(url)
    for song in playList:
        # Getting url of each song
        url = song['perma_url']
        
        metaData = fetch.download(url)
        curSong = metaData['title']

        # Converting raw song to mp3
        audioFile = AudioFileClip('temp.mp4')
        audioFile.write_audiofile((curSong + '.mp3'), bitrate='500k')

        # Embedding metaData in mp3
        Meta = meta.Metadata(curSong, metaData)
        Meta.embbed()

        # Deleting raw song and cover art
        os.remove('temp.mp4')
        os.remove('temp.jpg')
# If single song
else:
    metaData = fetch.download(url)
    curSong = metaData['title']

    # Converting raw song to mp3
    audioFile = AudioFileClip('temp.mp4')
    audioFile.write_audiofile((curSong + '.mp3'), bitrate='500k')

    # Embedding metaData in mp3
    Meta = meta.Metadata(curSong, metaData)
    Meta.embbed()

    # Deleting raw song and cover art
    os.remove('temp.mp4')
    os.remove('temp.jpg')