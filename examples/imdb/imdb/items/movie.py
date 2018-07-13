import scrapy


class MovieItem(scrapy.Item):
    movie = scrapy.Field()

    url = scrapy.Field()

    rating = scrapy.Field()

    spider = scrapy.Field()
