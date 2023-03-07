from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional

from uuid import UUID


def validate_uuid(value: str) -> str:
    """
    checks if value is valid UUID and converts back into string if ok

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


class Game(BaseModel):
    name: str
    display_name: str
    magnet: str
    version: float
    filesize: int
    date_added: float
    id: str
    key: str


class GameUpdateRequest(BaseModel):
    name: Optional[str]
    display_name: Optional[str]
    magnet: Optional[str]
    version: Optional[float]
    filesize: Optional[int]
    date_added: Optional[float]
    id: Optional[str]
    key: Optional[str]


class GamesList(BaseModel):
    games: List[Game]


class SearchGameRequest(BaseModel):
    key: Optional[str]
    name: Optional[str]
    display_name: Optional[str]
    date_added: Optional[float]
    id: Optional[str]


class ErrorRequest(BaseModel):
    type: str
    uuid: str
    exception: str
    traceback: str

    _validate_uuid = validator("uuid", allow_reuse=True)(validate_uuid)


class ErrorLog(BaseModel):
    type: str
    traceback: str
    exception: str
    uuid: str
    date_added: float


class ErrorLogResponse(ErrorLog):
    key: str


class User(BaseModel):
    email: EmailStr
    date_created: Optional[float]
    is_admin: bool = False
    is_user: bool = True
    disabled: Optional[bool]


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    username: Optional[EmailStr]
