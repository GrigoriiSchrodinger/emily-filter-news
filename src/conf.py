import os

from src.feature.RedisManager import RedisQueue

redis = RedisQueue(queue_name="processing", host="localhost", port=6379, db=0)
API_KEY = os.getenv('API_KEY')


def return_promt_was_there_post():
    return """
        • Действие: Ты будешь анализировать каждую новость из списка - {news_list}.
        • Цель: Твоя задача, проанализировать список и сказать были ли такая новость, которую я тебе отправлю, в списке.
        • Ожидания: Ты должна ответить True или False, True если новости не было.
         Ответ должен быть без блока кода, только текст.
            вот как должен выглядеть твой ответ: True/False
        """
