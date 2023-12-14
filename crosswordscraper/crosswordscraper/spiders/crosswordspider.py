import scrapy
from crosswordscraper.items import AnswerItem, QuestionItem, AnswerQuestion


class CrosswordspiderSpider(scrapy.Spider):
    name = "crosswordspider"
    allowed_domains = ["www.kreuzwort-raetsel.net"]
    start_urls = ["https://www.kreuzwort-raetsel.net/uebersicht.html"]

    def parse(self, response):
        letters = response.css(".dnrg li")

        for letter_url in letters:
            url = letter_url.css("a::attr('href')").get()

            yield response.follow(url, callback=self.parse_letter_page)

    def parse_letter_page(self, response):
        questions = response.css(".dnrg li")

        for questions_url in questions:
            url = questions_url.css("a::attr('href')").get()

            yield response.follow(url, callback=self.parse_questions_page)

    def parse_questions_page(self, response):
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
