import scrapy


class RedisSpider(scrapy.Spider):
    name = "redis"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
        #'http://www.baidu.com',
    ]

    def __init__(self, *args, **kwargs):
        super(RedisSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        print('!!!parse {0}'.format(response))
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)