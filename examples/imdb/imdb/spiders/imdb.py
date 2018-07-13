import scrapy

from examples.imdb.imdb.items.movie import MovieItem


class ImdbSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/chart/top',
    ]

    def parse(self, response):
        movie_urls = response.xpath('//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr/td[1]/a/@href').extract()
        for url in movie_urls:
            cur_url = "https://www.imdb.com/{0}".format(url)
            yield scrapy.Request(cur_url, self.parse_movie)

    def parse_movie(self, response):
        movie_name = response.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/h1/text()').extract_first()
        movie_url = response.url
        movie_rating = response.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()').extract_first()
        item = MovieItem(
            url=movie_url,
            movie=movie_name,
            rating=movie_rating,
            spider="0",
        )
        print("movie",movie_name)
        return item