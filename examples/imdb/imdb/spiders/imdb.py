import scrapy


class ImdbSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/chart/top',
    ]


    def parse(self, response):

        movie_urls = response.xpath('//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr/td/a/@href').extract()

        for url in movie_urls:
            cur_url = "https://www.imdb.com/{0}".format(url)
            yield scrapy.Request(cur_url, self.parse_movie)



    def parse_movie(self, response):

        pass