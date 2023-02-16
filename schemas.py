from pydantic import BaseModel, constr, validator
from typing import List

from uuid import UUID, uuid4


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


class ErrorRequest(BaseModel):
    type: str
    uuid: constr(
        regex="^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )
    exception: str
    traceback: str

    @validator("uuid")
    def validate_uuid(cls, value: str) -> str:
        """

        Args:
            value (str): the value to validate

        Raises:
            ValueError: raises a ValueError if no pattern in the string found

        Returns:
            str: returns the validated uuid
        """
        try:
            uuid = UUID(value, version=4)
        except ValueError:
            raise ValueError("invalid UUID")
        return str(uuid)


class Error(BaseModel):
    type: str
    traceback: str
    exception: str
    uuid: str
    date_added: float

    class Config:
        orm_mode = True


class ErrorLogs(BaseModel):
    errors: List[Error]

    class Config:
        orm_mode = True
