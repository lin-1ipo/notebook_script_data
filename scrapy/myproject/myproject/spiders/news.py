# coding: utf-8
import scrapy
# ItemのHeadlineクラスをインポート。
from myproject.items import Headline


class NewsSpider(scrapy.Spider):
    # Spiderの名前。
    name = "news"
    # クロール対象とするドメインのリスト。
    allowed_domains = ["news.yahoo.co.jp"]
    # クロールを開始するURLのリスト。
    start_urls = (
        'http://news.yahoo.co.jp/',
    )

    def parse(self, response):
        """
        トップページのトピックス一覧から個々のトピックスへのリンクを抜き出してたどる。
        """
        for url in response.css('ul.topics a::attr("href")').re(r'/pickup/\d+$'):
            yield scrapy.Request(response.urljoin(url), self.parse_topics)


    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す。
        """
        # Headlineオブジェクトを作成。
        item = Headline()
        # タイトル
        item['title'] = response.css('.newsTitle ::text').extract_first()
        # 本文
        item['body'] = response.css('.hbody').xpath('string()').extract_first()
        # Itemをyieldして、データを抽出する。
        yield item
