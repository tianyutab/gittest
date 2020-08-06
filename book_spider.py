import scrapy
from baidutuijian.items import BaidutuijianItem


class bookspider(scrapy.Spider):
    name = 'baidutuijian'
    allowed_domain = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_page)

        for page in response.xpath('//div[@class="paginator"]/a'):
            link = 'https://movie.douban.com/top250' + page.xpath('@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse_page)

    def parse_page(self, response):
        for item in response.xpath('//div[@class="info"]'):
            try:
                book = BaidutuijianItem()
                book['name'] = item.xpath('div[1]/a/span[1]/text()').extract()[0]
                book['english_name'] = item.xpath('div[1]/a/span[2]/text()').extract()[0][3:]
                book['other_name'] = item.xpath('div[1]/a/span[3]/text()').extract()[0][3:]
                yield book
            except:
                continue
