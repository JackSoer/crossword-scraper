# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrosswordscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class QuestionItem(scrapy.Item):
    word = scrapy.Field()


class AnswerItem(scrapy.Item):
    word = scrapy.Field()
    length = scrapy.Field()


class AnswerQuestion(scrapy.Item):
    answer = scrapy.Field()
    question = scrapy.Field()
