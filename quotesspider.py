import scrapy


class QuotesspiderSpider(scrapy.Spider):
    name = "quotesspider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={"playwright": True}
        )
    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')

        for quote in quotes:
            text = quote.xpath('.//span[@class="text"]/text()').get()
            author = quote.xpath('.//small[@class="author"]/text()').get()
            tags = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()


            yield {
                'text': text.strip() if text else "Brak tekstu",
                'author': author.strip() if author else "Brak autora",
                'tags': [tag.strip() for tag in tags] if tags else "Brak tagów",
            }
