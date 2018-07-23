from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myproject.items import Restaurant
import re
import subprocess


# 実行例 scrapy crawl tabelog -o restaurants.json -t json -a pre=tokyo
# 引数 url(default:None) per（都道府県ローマ字）
# その他もろもろ追加しておく
class TabelogSpider(CrawlSpider):
    name = "tabelog"

    # 引数取れるように設計
    def __init__(self, url=None, *args, **kwargs):
        super(TabelogSpider, self).__init__(*args, **kwargs)

        if url is not None:
            self.allowed_domains = [url]
            self.start_urls = ["http://" + url]
        else:
            start_url = 'http://tabelog.com/'
            start_url_tail = 'rstLst/lunch/?LstCosT=2&RdoCosTp=1'

            per = getattr(self, 'per', None)
            if per is not None:
                start_url = start_url + per + '/' + start_url_tail

            self.allowed_domains = ["tabelog.com"]
            self.start_urls = (
                start_url,)

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
        link = response.css('link[rel=canonical]').xpath('@href').extract_first()

        # レビュー取得
        #mynameproject無いよと叱られる
        # try:
        #    print(link)
        #    res = subprocess.check_call('scrapy crawl tabelog_review -o review6.json -t json -a url=' + link)
        #except:
        #    print("Error.")

        item = Restaurant(
            name=response.css('.display-name').xpath('string()').extract_first().strip(),
            address=''.join(prefectures + street_number),
            latitude=latitude,
            longitude=longitude,
            station=response.css('dt:contains("最寄り駅")+dd span::text').extract_first(),
            score=response.css('span.rdheader-rating__score-val-dtl::text').extract_first(),
        )

        yield item
