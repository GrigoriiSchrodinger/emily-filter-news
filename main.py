from src.conf import redis
from src.feature.gpt import GptRequest
from src.feature.request.RequestHandler import RequestDataBase
from src.logger import logger

def str_to_bool(s):
    return s.lower() in ("true", "yes")

def process_message(message):
    try:
        logger.debug(f"Получаем новость")
        request_db = RequestDataBase()
        gpt_request = GptRequest()

        recent_news = request_db.get_last_news()
        post_exists = recent_news and gpt_request.was_there_post(news_list=recent_news, news=message["content"])
        if not recent_news or str_to_bool(post_exists):
            print(recent_news)
            request_db.create_news_queue(
                channel=message["channel"],
                post_id=message["id_post"]
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