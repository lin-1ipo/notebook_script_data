from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myproject.items import Restaurant
import re


# 実行例 scrapy crawl tabelog -o restaurants.json -t json
class TabelogSpider(CrawlSpider):
    name = "tabelog_old"
    allowed_domains = ["tabelog.com"]
    start_urls = (
        'http://tabelog.com/tokyo/rstLst/lunch/?LstCosT=2&RdoCosTp=1',)

    rules = [
        # ページャーをたどる（最大9ページまで）
        # LinkExtractorの引数で特定のルール(例えばURLにnewを含むページのみScrapingするなど)を指定可能
        # 正規表現の \d を \d+ に変えると10ページ目以降もたどれる
        # Ruleにマッチしたページをダウンロードすると、callbackに指定した関数が呼ばれる
        # followをTrueにすると、再帰的に探査を行う。callbackがNoneならfollowのデフォルトはTrueとなる
        Rule(LinkExtractor(allow=r'/\w+/rstLst/lunch/\d/')),
        # レストランの詳細ページをパースする
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), callback='parse_restaurant'), ]

    # レストランの詳細ページのパース
    def parse_restaurant(self, response):
        # 緯度経度取得
        latitude, longitude = response.css('img.js-map-lazyload::attr("data-original")').re(
            r'markers=.*?%7C([\d.]+),([\d.]+)')

        # address材料取得
        prefectures = response.css('p.rstinfo-table__address span a::text').extract()
        street_number = response.css('p.rstinfo-table__address span::text').extract()

        item = Restaurant(
            name=response.css('.display-name').xpath('string()').extract_first().strip(),
            address=''.join(prefectures + street_number),
            latitude=latitude,
            longitude=longitude,
            station=response.css('dt:contains("最寄り駅")+dd span::text').extract_first(),
            score=response.css('span.rdheader-rating__score-val-dtl::text').extract_first(),
        )

        yield item
