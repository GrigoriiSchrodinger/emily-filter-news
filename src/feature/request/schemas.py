from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    pass


class PostSendNews(PostBase):
    seed: str
    text: str
    created_at: datetime

class PostSendNewsList(PostBase):
    send: list[PostSendNews]

class PostQueue(PostBase):
    seed: str
    text: str
    created_at: datetime

class PostQueueList(PostBase):
    queue: list[PostQueue]


class CreateNewsQueue(PostBase):
    channel: str
    post_id: int

