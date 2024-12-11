import os

from src.feature.RedisManager import RedisQueue

redis = RedisQueue(queue_name="processing", host="localhost", port=6379, db=0)
API_KEY = os.getenv('API_KEY')


def return_promt_was_there_post():
    return """
        Вот тебе список новостей которые были за 24 часа. 
        Список - {news_list}.
        Твоя задача, проанализировать список и сказать были ли такая новость, которую я тебе отправлю, в списке. 
        Ты должна ответить True или False, True если новости не было. без блока кода, только текст.
        вот как должен выглядеть твой ответ: 
        """
