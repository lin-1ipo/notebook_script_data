from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myproject.items import Restaurant, Review
import re


# 実行例 scrapy crawl tabelog -o restaurants.json -t json
class TabelogSpider(CrawlSpider):
    name = "tabelog_review_old"
    allowed_domains = ["tabelog.com"]
    start_urls = (
        # 'http://tabelog.com/tokyo/A1302/rstLst/?sw=焼肉トラジ',)
        'https://tabelog.com/tokyo/A1326/A132601/13162681/dtlrvwlst/?lc=2&PG=1',)

    rules = [
        # ページャーをたどる（最大9ページまで）。
        # LinkExtractorの引数で特定のルール(例えばURLにnewを含むページのみScrapingするなど)を指定可能
        # 正規表現の \d を \d+ に変えると10ページ目以降もたどれる。
        # Ruleにマッチしたページをダウンロードすると、callbackに指定した関数が呼ばれる
        # followをTrueにすると、再帰的に探査を行う。callbackがNoneならfollowのデフォルトはTrueとなる。

        # Rule(LinkExtractor(allow=r'/\w+/rstLst/1/')),
        # Rule(LinkExtractor(allow=r'/\w+/rstLst/lunch/\d/')),

        # レストランの詳細ページをパースする。
        # Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), callback='parse_restaurant'),
        # レストランのレビューページをパースする。
        # Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$')),
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/dtlrvwlst/.*PG=\d+$'), callback='parse_review'),
        # Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/dtlrvwlst/$'), callback='parse_review'),
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

    # レストランの詳細ページのパース
#    def parse_restaurant(self, response):
#        # 緯度経度取得
#        latitude, longitude = response.css('img.js-map-lazyload::attr("data-original")').re(
#            r'markers=.*?%7C([\d.]+),([\d.]+)')
#
#        # address材料取得
#        prefectures = response.css('p.rstinfo-table__address span a::text').extract()
#        street_number = response.css('p.rstinfo-table__address span::text').extract()
#
#        item = Restaurant(
#            name=response.css('.display-name').xpath('string()').extract_first().strip(),
#            address=''.join(prefectures + street_number),
#            latitude=latitude,
#            longitude=longitude,
#            station=response.css('dt:contains("最寄り駅")+dd span::text').extract_first(),
#            score=response.css('span.rdheader-rating__score-val-dtl::text').extract_first(),
#        )
#
#        yield item
