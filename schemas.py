from pydantic import BaseModel
from typing import List


class Game(BaseModel):

    name: str
    magnet: str
    version: float
    filesize: int

    class Config:
        orm_mode = True


class GamesList(BaseModel):

    games: List[Game]

    class Config:
        orm_mode = True
