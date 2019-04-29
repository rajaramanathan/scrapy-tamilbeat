from scrapy.loader import ItemLoader
from w3lib.html import replace_escape_chars
from tamilbeat.items import Song,Album
from scrapy.loader.processors import MapCompose, TakeFirst

#
# Strip the html space encoding and spaces.
#
def clean_text(value):
    if value:
        return " ".join(replace_escape_chars(value).strip().split())
    return ""

class SongItemLoader(ItemLoader):
    default_item_class = Song
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

class AlbumItemLoader(ItemLoader):
    default_item_class = Album
    name_in = MapCompose(clean_text)
    name_out = TakeFirst()
    music_director_in = MapCompose(clean_text)
    music_director_out = TakeFirst()
