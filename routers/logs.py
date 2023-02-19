import fastapi
from fastapi import Depends
from pydantic.error_wrappers import ValidationError

import schemas

import database

from utils import create_timestamp

import routers.users as users


router = fastapi.APIRouter(prefix="/logs")


@router.post("", status_code=fastapi.status.HTTP_200_OK)
def add_log(error: schemas.ErrorRequest):
    timestamp = create_timestamp()
    try:
        error_validator = schemas.Error(
            type=error.type,
            traceback=error.traceback,
            exception=error.exception,
            uuid=error.uuid,
            date_added=timestamp,
        )
    except ValidationError:
        raise fastapi.HTTPException("Error Validating response")
    database.base_logs.put(data=error_validator.dict())


@router.get("", status_code=fastapi.status.HTTP_200_OK)
async def get_logs(
    current_user: schemas.User = Depends(users.get_current_active_admin),
):
    response = database.base_logs.fetch()
    return {"logs": response.items}
