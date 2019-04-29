import scrapy
import re
from tamilbeat.itemloaders import SongItemLoader, AlbumItemLoader


#
# Crawl tamilbeat.com and parse album with mp3 links.
#
class TamilBeatSpider(scrapy.Spider):
    name = 'tamilbeat'

    start_urls = [
        'http://www.tamilzbeat.com/tamilsongs/movies%20a%20to%20z/',
    ]

    # Parse start page and crawl to all pagination pages
    def parse(self, response):
        for link in response.css('a::attr("href")').getall():
            pagination_link =  re.match(r"^.*[a-zA-Z0-9]-[a-zA-Z0-9]\.html$",link)
            if pagination_link:
                yield response.follow(link,callback=self.parse_pagination)


    # parse pagination page which has list of movies
    def parse_pagination(self,response):
        for link in response.xpath('//a[contains(@style, "TEXT-DECORATION")]/@href').getall():
            yield response.follow(link, callback=self.parse_movie)

    # parse movie page
    def parse_movie(self, response):
        songs = []
        for songRow in response.xpath('//tr[td[4]/font/a]'):
            songLdr = SongItemLoader(selector=songRow)
            songLdr.add_xpath('name', 'td[1]/font/text()')
            songLdr.add_xpath('download_link', 'td[4]/font/a/@href')
            songs.append(songLdr.load_item())

        albumLdr = AlbumItemLoader(response=response)
        albumLdr.add_xpath('name', '//table[@id="AutoNumber6"]/tr[position()=1]/td[position()=2]/*/font/text()')
        albumLdr.add_xpath('music_director',
                           '//table[@id="AutoNumber6"]/tr[position()=4]/td[position()=2]/*/font/text()')
        albumLdr.add_value('songs', songs)
        yield albumLdr.load_item()