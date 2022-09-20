from typing import List
from pydantic import BaseModel
from enum import Enum

class Area(BaseModel):
    id: int
    title: str
    slug: str


class Tag(BaseModel):
    id: int
    title: str
    slug: str


class TgUser(BaseModel):
    tg_id: int | None
    tag_settings: List[str] | None
    area_settings: List[str] | None
    viewed_posts: List[int] | None
    status: int | None


class Image(BaseModel):
    id: int | None
    image: str | None
    tg_id: int | None


class Posts(BaseModel):
    id: int | None
    title: str | None
    text: str | None
    lat: float | None
    lon: float | None
    slug: str | None
    status: int | None
    images_set: List[Image] | None
    
    
class Vote(BaseModel):
    count_up: int | None
    count_down: int | None
    status: int | None
    
    
