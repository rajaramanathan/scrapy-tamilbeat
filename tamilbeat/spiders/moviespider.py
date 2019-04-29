import scrapy
from tamilbeat.itemloaders import SongItemLoader, AlbumItemLoader

#
# For just development use. Can use to quickly test scraping a movie page on tamilbeat.com
#
class MovieSpider(scrapy.Spider):
    name = 'moviespider'

    # start_urls = [
    #     'http://www.tamilzbeat.com/tamilsongs/newreleases/Kathavarayan/index.html',
    # ]

    def parse(self, response):
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
