# This file contains various methods for embedding metadata in songs

import eyed3

class Metadata:
    # The constructor
    def __init__(self, song, meta):
        self.song = song
        self.meta = meta
    
    # Method to get all artist name
    def getArtists(self):
        artists = ""
        for artist in self.meta['more_info']['artistMap']['primary_artists']:
            artists = artists + artist['name'] + ", "
        artists = artists.rstrip(", ")
        return artists

    # Method to embbed meta data into song
    def embbed(self):
        # Opening audio file
        audioFile = eyed3.load((self.song + '.mp3'))

        # Embbeding title
        audioFile.tag.title = self.meta['title']
        audioFile.tag.subtitle = self.meta['subtitle']
        audioFile.tag.original_release_date = self.meta['year']
        audioFile.tag.album = self.meta['more_info']['album']
        audioFile.tag.artist = self.getArtists()
        audioFile.tag.copyright = self.meta['more_info']['copyright_text']
        audioFile.tag.publisher = self.meta['more_info']['label']
        audioFile.tag.images.set(3, open('temp.jpg', 'rb').read(), 'images/jpeg')
        audioFile.tag.save(version=eyed3.id3.ID3_V2_3)