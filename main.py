from src.conf import redis
from src.feature.gpt import GptRequest
from src.feature.request.RequestHandler import RequestDataBase
from src.logger import logger

def str_to_bool(s):
    return s.lower() in ("true", "yes")

def process_message(message):
    try:
        logger.info("Начало обработки сообщения", extra={'tags': {'message_id': message.get('id_post')}})
        logger.debug(f"Получаем новость", extra={'tags': {'content': message["content"][:50] + '...'}})
        
        request_db = RequestDataBase()
        gpt_request = GptRequest()

        recent_news = request_db.get_last_news()
        logger.info(f"Получено {len(recent_news)} последних новостей", extra={'tags': {'news_count': len(recent_news)}})
        
        post_exists = recent_news and gpt_request.was_there_post(news_list=recent_news, news=message["content"])
        logger.debug(f"Результат проверки уникальности: {post_exists}", extra={'tags': {'post_exists': post_exists}})
        
        if not recent_news or str_to_bool(post_exists):
            logger.info("Создание новой очереди новостей", extra={'tags': {
                'channel': message["channel"],
                'post_id': message["id_post"]
            }})
            request_db.create_news_queue(
                channel=message["channel"],
                post_id=message["id_post"]
            )
    except Exception as error:
        logger.critical("Критическая ошибка обработки", extra={'tags': {
            'error_type': type(error).__name__,
            'message_id': message.get('id_post')
        }})
        raise

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