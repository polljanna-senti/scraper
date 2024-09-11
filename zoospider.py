import scrapy


class ZoospiderSpider(scrapy.Spider):
    name = "zoospider"
    allowed_domains = ["zooplus.pl"]
    start_urls = ["https://www.zooplus.pl/shop/psy/karma_dla_psa_sucha"]

    def parse(self, response):
       products = response.xpath('//div[contains(@class,"ProductListItem_productWrapper")]')
       for product in products:
         yield{
           'name' : product.xpath('//div[contains(@class,"ProductListItem_productWrapper")]//h2/a//text()').get(),
           'description' : product.xpath('//div[contains(@class,"ProductListItem")]//p/object//text()').get(),
           'url' : product.xpath('//h2[contains(@class,"productInfoTitle")]/a/@href').get(),
           'stan_price' : product.xpath('//span[contains(@data-zta,"productStandardPriceAmount")]').get(),
           'num_reviews' : product.xpath('//span[contains(@data-zta,"ratingCount")]').get(),
           }

       next_page = response.xpath('//nav[@class="z-pagination"]//a[@data-zta="paginationNext"]/@href').get()
       if next_page:
           yield response.follow(next_page, callback=self.parse)


































































