from pydantic import BaseModel
from typing import List


class Game(BaseModel):
    name: str
    display_name: str
    magnet: str
    version: float
    filesize: int
    date_added: float
    id: str

    class Config:
        orm_mode = True


class GamesList(BaseModel):
    games: List[Game]

    class Config:
        orm_mode = True
