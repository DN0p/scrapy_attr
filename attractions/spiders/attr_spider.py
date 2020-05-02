import scrapy
import re

from ..google_url import get_url
from scrapy import Request


class AttracionsSpider(scrapy.Spider):
    name = 'attr'
    start_urls = get_url()

    def start_requests(self):
        for url in self.start_urls:
            if 'top10' in url:
                yield Request(url, callback=self.parse)
            elif 'tripzaza' in url:
                yield Request(url, callback=self.parse_tripzaza)
            elif 'sutochno' in url:
                yield Request(url, callback=self.parse_sutochno)

    def parse(self, response):

        url_image = response.xpath('//span[@itemprop="image"]/img[contains(@class, "wp-image")]/@data-src')[
                    1:].extract()
        title = response.xpath('//div[@id="primary"]//h3/text()').extract()
        description = response.xpath('//div[@id="primary"]//p/text()')[7:43].extract()
        row_data = zip(url_image, title, description)

        for item in row_data:
            scrap_info = {
                'url_image': item[0],
                'title': re.sub(r"\d+\.", "", str(item[1])),
                'description': item[2]
            }

            yield scrap_info

    def parse_tripzaza(self, response):
        url_image = response.xpath('//span[@class="ez-toc-section"]/../following-sibling::figure[1]/img/@data-lazy-src').extract()
        title = response.xpath('//span[@class="ez-toc-section"]//text()').extract()
        description = response.xpath('//span[@class="ez-toc-section"]/../following-sibling::p[1]').extract()
        row_data = zip(url_image, title, description)

        for item in row_data:
            scrap_info = {
                'url_image': item[0],
                'title': re.sub(r"\d+\.", "", str(item[1])),
                'description': re.sub(r"<.+?>", "", str(item[2]))
            }

            yield scrap_info

    def parse_sutochno(self, response):
        regular1 = r"<h2>.+?</h2>"
        regular2 = r"<.+?>"
        regular3 = r"[\n\r]"
        regular_all = re.compile("(%s|%s|%s)" % (regular1, regular2, regular3))
        url_image = response.xpath('//img[@class="h-full img-path"]/@src')[1:].extract()
        title = response.xpath('//div[@class="article-col-right"]/h2/text()').extract()
        description = response.xpath('//div[@class="article-col-right"]')[1:].extract()
        row_data = zip(url_image, title, description)

        for item in row_data:
            scrap_info = {
                'url_image': 'https://spb.sutochno.ru' + item[0],
                'title': item[1],
                'description': regular_all.sub('', str(item[2])),
            }

            yield scrap_info
