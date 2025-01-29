import scrapy
from ..items import ArticleItem

class PapSpider(scrapy.Spider):
    name = "papspider"
    allowed_domains = ["pap.pl"]
    start_urls = ["https://pap.pl"]

    def parse(self, response):
        # Ekstraktuj artykuły z głównej strony pap.pl:
        articles = response.xpath('//div[@class="textWrapper"]//h3/a/@href').getall()
        for article in articles:
            yield response.follow(article, self.parse_article)

    def parse_article(self, response):
        # Tworzenie items artykułu
        item = ArticleItem()
        item['title'] = " ".join(response.xpath("//h1//text()").getall()).strip()
        item['publishing_date'] = " ".join(response.xpath('//div[@class="moreInfo"]//text()').getall()).strip()
        item['content'] = "\n".join(response.xpath('//article[@role="article"]//p//text()').getall()).strip()
        item['url'] = response.url
        item['markdown'] = f"""# {item['title']}

        **Published on**: {item['publishing_date']}  
        **URL**: ({item['url']})  
        ## Content:  
        {item['content']}
        """

        yield item
