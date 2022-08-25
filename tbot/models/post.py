from ast import Str
from pydantic import BaseModel


class Posts(BaseModel):
    title: str
    text: str
    lat: float
    lon: float
    slug: str
