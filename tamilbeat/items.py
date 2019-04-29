import scrapy

class Song(scrapy.Item):
    name = scrapy.Field()
    download_link = scrapy.Field()

class Album(scrapy.Item):
    name = scrapy.Field()
    music_director = scrapy.Field()
    songs = scrapy.Field()