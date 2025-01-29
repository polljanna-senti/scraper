

import scrapy
from scrapy_playwright.page import PageMethod


class SteamspiderSpider(scrapy.Spider):
    name = "steamspider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com"]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_page_methods = [
                    PageMethod("wait_for_selector", "div.tab_content_items > a")
                ]
            )
        )

    def parse(self, response):
        games = response.xpath('//div[@class="tab_content_items"]/a')
        for game in games:
            title = game.xpath('.//div[@class="tab_item_name"]//text()').get(),
            thumbnail = game.xpath('.//div[@class="tab_item_cap"]/img/@src').get(),
            release_date = game.xpath('.//div[@class="release_date"]//text()').get(),
            final_price = game.xpath('.//div[@class="discount_final_price"]//text()').get()

            yield {
                'title': title,
                'thumbnail' : thumbnail,
                'release_date': release_date,
                'final_price' : final_price
            }
