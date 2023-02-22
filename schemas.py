from pydantic import BaseModel, constr, validator, EmailStr
from typing import List, Optional

from uuid import UUID, uuid4


class Game(BaseModel):
    name: str
    display_name: str
    magnet: str
    version: float
    filesize: int
    date_added: int
    # torrent_id
    id: str

    class Config:
        orm_mode = True


class GameWithKey(Game):
    key: str


class GamesList(BaseModel):
    games: List[Game]

    class Config:
        orm_mode = True


class SearchGameRequest(BaseModel):
    key: Optional[str]
    name: Optional[str]
    display_name: Optional[str]
    date_added: Optional[float]
    id: Optional[str]


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
    key: str
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


class User(BaseModel):
    email: EmailStr
    date_created: float | None = None
    is_admin: bool = False
    is_user: bool = True
    disabled: bool | None = None


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    username: EmailStr | None = None
