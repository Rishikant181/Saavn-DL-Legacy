# This is a downloader for JioSaavn that works by making some http request to JioSaavn

import os
import sys

import fetcher
from moviepy.editor import AudioFileClip

songUrl = sys.argv[1]                                       # To store song original url

fetcher.download(songUrl)

# Converting raw song to mp3
audioFile = AudioFileClip('test.mp4')
audioFile.write_audiofile('test.mp3', bitrate='3000k')

# Deleting raw song
os.remove('test.mp4')