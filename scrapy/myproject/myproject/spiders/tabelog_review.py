from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myproject.items import Restaurant, Review
import re


# 実行例 scrapy crawl tabelog -o restaurants.json -t json -a url=https:/...
# 引数 url 店のURL tabelog.pyで取得しよう
class TabelogSpider(CrawlSpider):
    name = "tabelog_review"

    # 引数取れるように設計
    def __init__(self, url=None, *args, **kwargs):
        super(TabelogSpider, self).__init__(*args, **kwargs)

        # urlが取れること大前提
        if url is not None:
            self.allowed_domains = ["tabelog.com"]
            # start_url = 'https://tabelog.com/tokyo/A1326/A132601/13162681/'
            start_url = url + 'dtlrvwlst/?lc=2&PG=1'
            self.start_urls = (
                start_url,)

    rules = [
        # ページャーをたどる（最大9ページまで）。
        # LinkExtractorの引数で特定のルール(例えばURLにnewを含むページのみScrapingするなど)を指定可能
        # 正規表現の \d を \d+ に変えると10ページ目以降もたどれる。
        # Ruleにマッチしたページをダウンロードすると、callbackに指定した関数が呼ばれる
        # レストランのレビューページをパースする。
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/dtlrvwlst/.*PG=\d+$'), callback='parse_review'),
    ]

    # レストランのレビューページのパース
    def parse_review(self, response):
        # review表取得
        review_list = response.css('div.rvw-item__rvw-comment').xpath('string()').extract()
        score_list = response.css('b.c-rating__val').xpath('string()').extract()

        for i in range(len(review_list)):
            item = Review(
                name=response.css('span.rstdtl-crumb::text').extract()[0],
                score=score_list[i + 1].strip(),
                text=review_list[i].strip(),
            )
            yield item
