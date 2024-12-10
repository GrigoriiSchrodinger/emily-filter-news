from openai import OpenAI
from src.conf import API_KEY, return_promt_was_there_post, return_promt_rate_post
from src.logger import logger


class GptAPI:
    def __init__(self, api_key: str = API_KEY, model: str = "gpt-4o"):
        self.client = None
        self.api_key = api_key
        self.model = model
        self.initialize_client()

    def initialize_client(self):
        try:
            self.client = OpenAI(api_key=self.api_key)
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
        logger.debug(f"Делаем запрос gpt - на проверку поста")
        return self.create(
            prompt=return_promt_was_there_post().format(news_list=news_list),
            user_message=news
        )

    def rate_post(self, news: str) -> str:
        logger.debug(f"Делаем запрос gpt- на оценку")
        return self.create(
            prompt=return_promt_rate_post(),
            user_message=news
        )