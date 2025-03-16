import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
MODEL = os.getenv('MODEL', "gpt-4o")
BASE_URL = os.getenv('BASE_URL', "https://api.openai.com/v1")
ENV = os.getenv('ENV', "localhost")

def return_promt_was_there_post():
    return """
        • Действие: Ты будешь анализировать каждую новость из списка - {news_list}.
        • Цель: Твоя задача, проанализировать список и сказать были ли такая новость, которую я тебе отправлю, в списке.
        • Ожидания: Ты должна ответить True или False, True если новости не было.
         Ответ должен быть без блока кода, только текст.
            вот как должен выглядеть твой ответ: True/False
        """
