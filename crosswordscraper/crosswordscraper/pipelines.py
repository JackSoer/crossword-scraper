# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from crosswordscraper.items import AnswerItem, QuestionItem, AnswerQuestion
from dotenv import load_dotenv
import os

load_dotenv()


class CrosswordscraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveToMySQLPipeLine:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=f"{os.getenv('MYSQL_HOST')}",
            user=f"{os.getenv('MYSQL_USER')}",
            password=f"{os.getenv('MYSQL_PASSWORD')}",
            database=f"{os.getenv('MYSQL_DATABASE')}",
        )

        self.cur = self.conn.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS question (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word VARCHAR(255) NOT NULL
            )
        """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS answer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word VARCHAR(255) NOT NULL,
                length INT NOT NULL
            )
        """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_question (
                id INT AUTO_INCREMENT PRIMARY KEY,
                answer_id INT NOT NULL,
                question_id INT NOT NULL,
                FOREIGN KEY (answer_id) REFERENCES answer(id),
                FOREIGN KEY (question_id) REFERENCES question(id)
            )
        """
        )

    def process_item(self, item, spider):
        try:
            if isinstance(item, QuestionItem):
                self.get_or_create_id("question", "word", item["word"])
            elif isinstance(item, AnswerItem):
                self.get_or_create_id(
                    "answer", "word", item["word"], length=item["length"]
                )
            elif isinstance(item, AnswerQuestion):
                answer_id = self.get_or_create_id("answer", "word", item["answer"])
                question_id = self.get_or_create_id(
                    "question", "word", item["question"]
                )

                self.cur.execute(
                    "INSERT INTO answer_question (answer_id, question_id) VALUES (%s, %s)",
                    (answer_id, question_id),
                )
        except Exception as e:
            self.conn.rollback()
            raise e
        else:
            self.conn.commit()

        return item

    def get_or_create_id(self, table, column, value, **kwargs):
        columns = [column]
        values = [value]

        for key, val in kwargs.items():
            columns.append(key)
            values.append(val)

        condition = " AND ".join(f"{col} = %s" for col in columns)
        self.cur.execute(f"SELECT id FROM {table} WHERE {condition}", tuple(values))
        existing_id = self.cur.fetchone()

        if existing_id is not None:
            return existing_id[0]
        else:
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(values))
            query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
            self.cur.execute(query, tuple(values))
            self.conn.commit()

            return self.cur.lastrowid
