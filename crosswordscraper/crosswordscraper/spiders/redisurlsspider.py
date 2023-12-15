import scrapy
import redis
from dotenv import load_dotenv
import os

load_dotenv()


class RedisurlsspiderSpider(scrapy.Spider):
    name = "redisurlsspider"
    allowed_domains = ["www.kreuzwort-raetsel.net"]
    start_urls = ["https://www.kreuzwort-raetsel.net/uebersicht.html"]
    
    redis_url = f"redis://{os.getenv("REDIS_USER")}:{os.getenv("REDIS_PASSWORD")}@{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}"
    redis_client = redis.from_url(redis_url)
    size = redis_client.dbsize()
    
    def parse(self, response):
        if self.size == 0:
            yield response.follow(self.start_urls[0], callback=self.add_urls_to_redis) 
            
    def add_urls_to_redis(self, response):
        letters = response.css(".dnrg li")

        for letter_url in letters:
            url = letter_url.css("a::attr('href')").get()

            yield response.follow(url, callback=self.parse_letter_page)   
            
    def parse_letter_page(self, response):
        questions = response.css(".dnrg li")

        for questions_url in questions:
            url = questions_url.css("a::attr('href')").get()
            
            self.redis_client.lpush("quotes_queue:start_urls", f"https://{self.allowed_domains[0]}/{url}")

   
