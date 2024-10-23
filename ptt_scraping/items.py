# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join


def get_id(element):
    if element:
        return element.replace('.html', '')
    return element


def get_main_content(element):
    if element:
        pretext = element.split('--')[0]
        texts = pretext.split('\n')
        contents = texts[1:]
        content = ''.join(contents)
        return content
    return element


def convert_hundreds(element):
    if element == '爆':
        return 100
    return element


def convert_integer(element):
    if element:
        return int(element)
    return 0


class PostItem(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(get_id, str.strip),
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join('')
    )
    author = scrapy.Field(
        output_processor=TakeFirst()
    )
    date = scrapy.Field(
        output_processor=TakeFirst()
    )
    push = scrapy.Field(
        input_processor=MapCompose(convert_hundreds, convert_integer),
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        input_processor=MapCompose(get_main_content),
        output_processor=Join('')
    )
