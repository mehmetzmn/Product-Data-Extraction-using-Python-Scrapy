# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy


class EplanProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name: str | None = None
    part_number = scrapy.Field()
    manufacturer = scrapy.Field()
    designation = scrapy.Field()
    description = scrapy.Field()
    product_group = scrapy.Field()
