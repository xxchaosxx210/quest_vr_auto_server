import fastapi
from pydantic.error_wrappers import ValidationError

import schemas

from database import base_logs

from utils import create_timestamp


router = fastapi.APIRouter(prefix="/logs")


@router.post("", status_code=fastapi.status.HTTP_200_OK)
def add_error_to_logs(error: schemas.ErrorRequest):
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
    base_logs.put(data=error_validator.dict())
