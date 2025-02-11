from typing import Optional

import requests
from pydantic import BaseModel, ValidationError

from src.feature.request.schemas import CreateNewsQueue, PostSendNewsList, PostQueueList
from src.logger import logger


class RequestHandler:
    def __init__(self, base_url="http://0.0.0.0:8000/", headers=None, timeout=10):
        """
        Инициализация класса для работы с запросами.

        :param base_url: Базовый URL для запросов
        :param headers: Заголовки для запросов (по умолчанию None)
        :param timeout: Тайм-аут для запросов (по умолчанию 10 секунд)
        """
        self.base_url = base_url
        self.headers = headers if headers is not None else {}
        self.timeout = timeout

    def __get__(
            self, endpoint: str, path_params: Optional[BaseModel] = None, query_params: Optional = None,
            response_model: Optional = None
    ):
        """
        Выполняет GET-запрос к указанному endpoint.

        :param query_params:
        :param path_params:
        :param response_model:
        :param endpoint: Путь к ресурсу относительно base_url
        :return: Ответ сервера в формате JSON (если есть) или текстовый ответ
        """
        # Формируем URL с подстановкой параметров пути

        if path_params:
            endpoint = endpoint.format(**path_params.model_dump())

        url = f"{self.base_url}/{endpoint}"

        try:
            # Преобразуем параметры запроса в словарь
            logger.debug(f"Делаем get запрос - {url}, data - {query_params}")
            query_params_dict = query_params.dict() if query_params else None
            response = requests.get(url, headers=self.headers, params=query_params_dict, timeout=self.timeout)
            response.raise_for_status()

            # Обрабатываем ответ с использованием модели
            data = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            logger.debug(f"Ответ - {data}")
            return response.status_code, (response_model.parse_obj(data) if response_model else data)
        except requests.exceptions.RequestException as error:
            logger.exception("Произошла ошибка: %s", error)
            return None, None
        except ValidationError as error:
            logger.exception("Произошла ошибка: %s", error)
            return None, None

    def __post__(self, endpoint: str, data: Optional = None, response_model: Optional = None):
        """
            Выполняет POST-запрос к указанному endpoint.

            :param self:
            :param response_model:
            :param endpoint: Путь к ресурсу относительно base_url
            :param data: Данные для отправки в формате form-encoded (по умолчанию None)
            :return: Ответ сервера в формате JSON (если есть) или текстовый ответ
            """
        url = f"{self.base_url}/{endpoint}"
        try:
            logger.debug(f"Делаем post запрос - {url}, data - {data}")
            data_dict = data.model_dump() if data else None
            response = requests.post(url, headers=self.headers, json=data_dict, timeout=self.timeout)
            response.raise_for_status()

            data = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            logger.debug(f"Ответ - {data}")
            return response_model.model_validate(data) if response_model else data
        except requests.exceptions.RequestException as error:
            logger.exception("Произошла ошибка: %s", error)
            return None
        except ValidationError as error:
            logger.exception("Произошла ошибка: %s", error)
            return None

    def set_headers(self, headers):
        """
        Устанавливает или обновляет заголовки для запросов.

        :param self:
        :param headers: Словарь с заголовками
        """
        self.headers.update(headers)

    def set_timeout(self, timeout):
        """
        Устанавливает тайм-аут для запросов.

        :param self:
        :param timeout: Тайм-аут в секундах
        """
        self.timeout = timeout


class RequestDataBase(RequestHandler):
    def __get_last_send_news__(self) -> [int, PostSendNewsList]:
        return self.__get__(endpoint='send-news/get-news/by/hours', response_model=PostSendNewsList)

    def __get_last_queue__(self) -> [int, PostQueueList]:
        return self.__get__(endpoint='queue/get-news/by/hours', response_model=PostQueueList)

    def __create_news_queue__(self, data: CreateNewsQueue):
        return self.__post__(endpoint='queue/create', data=data)

    def create_news_queue(self, channel: str, post_id: int):
        queue = CreateNewsQueue(
            channel=channel,
            post_id=post_id
        )
        self.__create_news_queue__(data=queue)
        return

    def get_last_news(self):
        logger.info("Запрос последних отправленных новостей")
        send_news = self.__get_last_send_news__()
        logger.info("Запрос последних новостей в очереди")
        queue = self.__get_last_queue__()
        
        total_news = send_news[1].send + queue[1].queue
        logger.info("Сборка общего списка новостей", extra={'tags': {
            'send_news_count': len(send_news[1].send),
            'queue_news_count': len(queue[1].queue)
        }})
        return total_news
