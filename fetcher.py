# This file contains various method to fetch raw song from cdn

import requests
import json

# Method to extract song name from url
def getSongNameFromUrl(songUrl):
    songName = songUrl[songUrl.index('/', songUrl.index('/', songUrl.index('/', songUrl.index("//") + 1) + 1) + 1) + 1:]
    songName = songName[0:songName.index('/')]
    return songName

# Method to get song encrypted url
def getEncryptedUrl(songName, songUrl):
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
    response = requests.get("https://www.jiosaavn.com/api.php", params)

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
def getAuthUrl(encryptedUrl):
    # Setting request params
    params = {
        "__call": "song.generateAuthToken",
        "url": encryptedUrl,
        "bitrate": 128,
        "api_version": 4,
        "_format": "json",
        "ctx": "web6dot0",
        "_marker": 0
    }

    # Sending request
    response = requests.get("https://www.jiosaavn.com/api.php", params)

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
    response = requests.get(authUrl)

    # Returning media url
    return response.url

# Method to start fetching raw song
def getSong(songUrl):
    # Extracting song name from url
    songName = getSongNameFromUrl(songUrl)

    # Getting encrypted song url
    encryptedUrl = getEncryptedUrl(songName, songUrl)

    # Getting authentication url
    authUrl = getAuthUrl(encryptedUrl)

    # Getting song cdn url
    cdnUrl = getMediaUrl(authUrl)

    # Returning cdn url
    return cdnUrl

# Method to download the actual media
def download(songUrl):
    open('test.mp4', 'wb').write(requests.get(getSong(songUrl)).content)