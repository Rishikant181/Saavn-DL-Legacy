# This file contains various method to fetch raw song from cdn

import requests
import json
import meta

class Fetcher:
    # The constructor
    def __init__(self):
        self.found = False                                               # To store whether song was found or not
        self.mData = None                                                # Object to store and manitpulate meta

    # Method to extract song name from url
    def getSongNameFromUrl(self, songUrl):
        songName = songUrl[songUrl.index('/', songUrl.index('/', songUrl.index('/', songUrl.index("//") + 1) + 1) + 1) + 1:]
        songName = songName[0:songName.index('/')]
        return songName

    # Method to get song encrypted url
    def fetchEncryptedUrl(self, songName, songUrl):
        # Searching for song to get encrypted url
        found = False                                                   # To store whether correct song was found or not
        
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

        # Iterating through list to get correct encrypted_media_url
        for song in jsonResults["results"]:
            if(song["perma_url"] == songUrl):
                encryptedUrl = song["more_info"]["encrypted_media_url"]
                found = True
                # Create and store meta data
                mData = meta.Metadata(song)
                break
        
        # If song was found
        if(found == True):
            return encryptedUrl
        # If not found
        else:
            return None

    # Method to get authentication token
    def fetchAuthUrl(self, encryptedUrl):
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
    def fetchMediaUrl(self, authUrl):
        response = requests.get(authUrl)

        # Returning media url
        return response.url

    # Method to start fetching raw song
    def fetchSong(self, songUrl):
        # Extracting song name from url
        songName = self.getSongNameFromUrl(songUrl)

        # Getting encrypted song url
        encryptedUrl = self.fetchEncryptedUrl(songName, songUrl)

        # Getting authentication url
        authUrl = self.fetchAuthUrl(encryptedUrl)

        # Getting song cdn url
        cdnUrl = self.fetchMediaUrl(authUrl)

        # Returning cdn url
        return cdnUrl

    # Method to download the actual media
    def download(self, songUrl):
        open('test.mp4', 'wb').write(requests.get(self.fetchSong(songUrl)).content)