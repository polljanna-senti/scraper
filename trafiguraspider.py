import scrapy
from scrapy_playwright.page import PageMethod


class TrafiguraSpider(scrapy.Spider):
    name = "trafiguraspider"
    allowed_domains = ["myworkdayjobs.com"]
    start_urls = ["https://trafigura.wd3.myworkdayjobs.com/TrafiguraCareerSite"]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", 'ul[role="list"] > li'),
                ],
            },
            callback=self.parse,
        )

    async def parse(self, response):
        # Extract job postings
        for job in response.css('ul[role="list"] > li'):
            yield {
                'title': job.css('h3 a::text').get(),
                'location': job.css('div[data-automation-id="locations"] dd::text').get(),
            }

        # Get Playwright page instance
        page = response.meta["playwright_page"]

        # Check if the "Next" button exists and is not disabled
        has_next = await page.evaluate(
            "() => { const btn = document.querySelector('button[aria-label=\"next\"]'); return btn && !btn.disabled; }"
        )

        if has_next:
            self.logger.info("Next button found! Clicking to the next page.")

            # Click "Next" and wait for new data
            await page.click('button[aria-label="next"]')
            await page.wait_for_selector('ul[role="list"] > li', timeout=5000)

            # Get new page content
            new_html = await page.content()

            # Create a new response object with updated page content
            new_response = scrapy.http.HtmlResponse(
                url=response.url,
                body=new_html,
                encoding="utf-8",
                request=response.request
            )

            # Iterate over new response asynchronously
            async for item in self.parse(new_response):
                yield item  # Correct way to return items in an async function

        else:
            self.logger.info("No Next button found. Scraping complete.")
