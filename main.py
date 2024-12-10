import json

from src.conf import redis, evaluate_news_post
from src.feature.gpt import GptRequest
from src.feature.request.RequestHandler import RequestDataBase
from src.logger import logger


def process_message(message):
    try:
        logger.debug(f"Получаем новость")
        request_db = RequestDataBase()
        gpt_request = GptRequest()

        recent_news = request_db.get_last_news()
        post_exists = recent_news and gpt_request.was_there_post(news_list=recent_news, news=message["content"])

        if not recent_news or post_exists:
            rating = json.loads(gpt_request.rate_post(news=message["content"]))

            score = evaluate_news_post(
                rating["influence"],
                rating["interest"],
                rating["emotional_impact"],
                rating["social_significance"]
            )
            request_db.create_news_rate_and_queue(
                channel=message["channel"],
                post_id=message["id_post"],
                score_rate=score
            )
    except Exception as error:
        logger.exception("Произошла ошибка: %s", error)

def main():
    try:
        message = redis.receive_from_queue(queue_name="filter")
        if message and "content" in message and isinstance(message["content"], str):
            process_message(message)
    except Exception as error:
        logger.exception("Произошла ошибка: %s", error)


if __name__ == '__main__':
    logger.info("Start work")
    while True:
        main()