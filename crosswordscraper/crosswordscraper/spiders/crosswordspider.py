from crosswordscraper.items import AnswerItem, QuestionItem, AnswerQuestion
from scrapy_redis.spiders import RedisSpider


class CrosswordspiderSpider(RedisSpider):
    name = "crosswordspider"

    redis_key = "quotes_queue:start_urls"
    redis_batch_size = 0
    max_idle_time = 7

    def parse(self, response):
        questions_data = response.css("tr")

        for question_data in questions_data:
            question = question_data.css(".Question a::text").get()

            if question is not None:
                answer = question_data.css(".AnswerShort a::text").get()

                question_item = QuestionItem()
                question_item["word"] = question
                yield question_item

                answer_item = AnswerItem()
                answer_item["word"] = answer
                answer_item["length"] = len(answer)
                yield answer_item

                answer_question_item = AnswerQuestion()
                answer_question_item["answer"] = answer
                answer_question_item["question"] = question
                yield answer_question_item
