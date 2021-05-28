# This is a downloader for JioSaavn that works by making some http request to JioSaavn

# low  -128kbps-125k bitrate
# med  -256kbps-250k bitrate
# high -320kbps-500k bitrate

import os
import sys

import fetcher
from moviepy.editor import AudioFileClip

songUrl = sys.argv[1]                                       # To store song original url

fetch = fetcher.Fetcher()
fetch.download(songUrl)

# Converting raw song to mp3
audioFile = AudioFileClip('test.mp4')
audioFile.write_audiofile('test.mp3', bitrate='500k')

# Deleting raw song
os.remove('test.mp4')