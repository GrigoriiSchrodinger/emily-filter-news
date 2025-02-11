from openai import OpenAI
from src.conf import API_KEY, return_promt_was_there_post, BASE_URL, MODEL
from src.logger import logger


class GptAPI:
    def __init__(self, api_key: str = API_KEY, base_url: str = BASE_URL, model: str = MODEL):
        self.client = None
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.initialize_client()

    def initialize_client(self):
        try:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except Exception as error:
            logger.exception("Произошла ошибка: %s", error)

    def create(self, prompt: str, user_message: str) -> str:
        try:
            logger.debug(f"Запрос GPT - model = {self.model} | prompt = {prompt} | user_message = {user_message}")
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            logger.debug(f"Ответ GPT - {completion}")
            return completion.choices[0].message.content
        except Exception as error:
            logger.exception("Произошла ошибка: %s", error)
            return ""


class GptRequest(GptAPI):
    def was_there_post(self, news_list: list, news: str) -> str:
        logger.info("Запрос к GPT на проверку уникальности", extra={'tags': {
            'news_length': len(news),
            'news_list_count': len(news_list)
        }})
        result = self.create(
            prompt=return_promt_was_there_post().format(news_list=news_list),
            user_message=news
        )
        logger.info("Ответ GPT получен", extra={'tags': {'gpt_response': result[:100] + '...'}})
        return result