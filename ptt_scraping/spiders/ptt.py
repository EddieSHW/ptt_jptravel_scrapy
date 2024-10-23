import scrapy
from ptt_scraping.items import PostItem
from scrapy.loader import ItemLoader
import logging


class PttSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Japan_Travel/index.html']

    def parse(self, response):
        articles = response.xpath('//div[@class="r-ent"]')

        for article in articles:
            yield response.follow(url=response.urljoin(article.xpath('.//div[@class="title"]/a/@href').get()),
                                  callback=self.parse_article)

        next_page = response.xpath('//a[contains(text(), "上頁")]/@href').get()
        logging.debug({
            'response.status': response.status,
            'response.url': response.url,
            'next_page': next_page
        })
        # if next_page is not None:
        #     yield response.follow(url=next_page, callback=self.parse)

    def parse_article(self, response):
        logging.info(response.url)
        loader = ItemLoader(item=PostItem(), response=response)

        loader.add_value('id', response.url.split('/')[-1])

        loader.add_xpath('author', '//div[@class="article-metaline"][position()=1]/span['
                                   '@class="article-meta-value"]/text()')
        loader.add_xpath('title', '//div[@class="article-metaline"][position()=2]/span['
                                  '@class="article-meta-value"]/text()')
        loader.add_xpath('date', '//div[@class="article-metaline"][position()=3]/span['
                                 '@class="article-meta-value"]/text()')
        loader.add_xpath('content', '//div[@id="main-content"]/text()')

        yield loader.load_item()
