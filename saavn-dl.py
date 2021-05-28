# This is a downloader for JioSaavn that works by making some http request to JioSaavn

import os
import sys
import json
import requests as reqs
from moviepy.editor import AudioFileClip

# Method to extract song name from url
def getSongNameFromUrl(songUrl):
    songName = songUrl[songUrl.index('/', songUrl.index('/', songUrl.index('/', songUrl.index("//") + 1) + 1) + 1) + 1:]
    songName = songName[0:songName.index('/')]
    return songName

# Method to get song encrypted url
def getEncryptedUrl(songUrl):
    # Searching for song to get encrypted url
    # Setting requests params
    params = {
        "p": 1,
        "q": songName,
        "_format": "json",
        "marker": 0,
        "api_version": 4,
        "ctx": "web6dot0",
        "n": 20,
        "__call": "search.getResults"
    }
    # Sending request
    response = reqs.get("https://www.jiosaavn.com/api.php", params)

    # Getting response raw content
    results = response.content.decode('utf-8')

    # Stripping extras
    results = results[results.index("->") + 2:].strip()

    # Converting content to dict
    jsonResults = json.loads(results)

    # Getting encrypted_media_url
    encryptedUrl = jsonResults["results"][0]["more_info"]["encrypted_media_url"]

    return encryptedUrl

# Method to get authentication token
def getAuthUrl(encryptedMediaUrl):
    # Setting request params
    params = {
        "__call": "song.generateAuthToken",
        "url": encryptedMediaUrl,
        "bitrate": 128,
        "api_version": 4,
        "_format": "json",
        "ctx": "web6dot0",
        "_marker": 0
    }

    # Sending request
    response = reqs.get("https://www.jiosaavn.com/api.php", params)

    # Getting response raw content
    results = response.content.decode('utf-8')

    # Stripping extras
    results = results.strip()

    # Converting content to dict
    jsonResults = json.loads(results)

    # Returning auth_url
    return jsonResults["auth_url"]
    
# Method to get direct media url
def getMediaUrl(authUrl):
    response = reqs.get(authUrl)

    # Returning media url
    return response.url

songUrl = sys.argv[1]                                       # To store song original url
songName = getSongNameFromUrl(songUrl)                      # Getting song name

# Fetch encrypted url by searching for song then reqtrieving it from results
encryptedUrl = getEncryptedUrl(songUrl)
encryptedUrl = encryptedUrl.replace('+', "%2B").replace('/', "%2F")

# Get authorization url by passing encrypted url
authUrl = getAuthUrl(encryptedUrl)

# Get song cdn url by authorizing authUrl
mediaUrl = getMediaUrl(authUrl)

# Increasing quality to 320 kbps
mediaUrl = mediaUrl.replace("160.mp4", "320.mp4")

# Downloading song as raw from cdn url
open(songName + '.mp4', 'wb').write(reqs.get(mediaUrl).content)

# Converting raw song to mp3
audioFile = AudioFileClip(songName + '.mp4')
audioFile.write_audiofile((songName + '.mp3'), bitrate='3000k')

# Deleting raw song
os.remove(songName + '.mp4')