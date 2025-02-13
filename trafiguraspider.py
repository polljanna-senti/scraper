import scrapy
from scrapy_playwright.page import PageMethod


class TrafiguraspiderSpider(scrapy.Spider):
    name = "trafiguraspider"
    allowed_domains = ["myworkdayjobs.com"]
    start_urls = ["https://trafigura.wd3.myworkdayjobs.com/TrafiguraCareerSite"]


    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_page_methods = [
                    PageMethod("wait_for_selector", "ul[role='list'] > li"),
                ],
            ),
            callback=self.parse,
        )

    async def parse(self, response):
        for job in response.css("ul[role='list'] > li"):
            yield {
                'title': job.css('h3 a::text').get(),
                'location': job.css('div[data-automation-id="locations"] dd::text').get(),
            }
