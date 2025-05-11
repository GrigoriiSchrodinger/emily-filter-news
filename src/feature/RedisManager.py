import json
import redis

from src.logger import logger
from src.service_url import get_url_redis


class RedisQueue:
    def __init__(self, queue_name, host=get_url_redis(), port=6379, db=0):
        """
        Инициализирует подключение к Redis и имя очереди.
        """
        self.queue_name = queue_name
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

    def send_to_queue(self, queue_name, data):
        """
        Отправляет данные в очередь
        """
        try:
            logger.info("Отправка в очередь", extra={'tags': {
                'queue': queue_name,
                'data_length': len(data)
            }})
            self.redis_conn.rpush(queue_name, data)
        except Exception as error:
            logger.exception("Произошла ошибка: %s", error)

    def receive_from_queue(self, queue_name, block=True, timeout=None):
        """
        Получает данные из очереди
        """
        try:
            logger.info("Ожидание сообщения из очереди", extra={'tags': {
                'queue': queue_name,
                'blocking': block
            }})
            if block:
                logger.debug(f"Ждем ответа очереди - {queue_name}")
                item = self.redis_conn.blpop(queue_name, timeout=timeout)
            else:
                item = self.redis_conn.lpop(queue_name)

            if item:
                logger.info("Успешно получено сообщение", extra={'tags': {
                    'queue': queue_name,
                    'message_size': len(item[1]) if item else 0
                }})
                logger.debug(f"Получили из очереди - {json.loads(item[1].decode('utf-8'))}")
                return json.loads(item[1].decode('utf-8'))
            return None
        except Exception as error:
            logger.exception("Произошла ошибка: %s", error)
