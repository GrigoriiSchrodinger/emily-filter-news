from pydantic import BaseModel


class PostBase(BaseModel):
    pass


class PostSendNews(PostBase):
    texts: list[str]


class PostSendQueue(PostBase):
    texts: list[str]


class CreateNewsQueue(PostBase):
    channel: str
    post_id: int


class CreateNewsRate(PostBase):
    channel: str
    post_id: int
    value: float
