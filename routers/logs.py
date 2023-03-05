from typing import Optional
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
        error_validator = schemas.ErrorLog(
            type=error.type,
            traceback=error.traceback,
            exception=error.exception,
            uuid=error.uuid,
            date_added=timestamp,
        )
    except ValidationError as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Error validating the request",
        )
    database.base_logs.put(data=error_validator.dict())


@router.get("", status_code=fastapi.status.HTTP_200_OK)
async def get_logs(
    sort_by: Optional[str] = None,
    order_by: Optional[str] = None,
    limit: int = 1000,
    current_user: schemas.User = Depends(users.get_current_active_admin),
):
    # grab the logs from the database
    response = database.base_logs.fetch(limit=limit)
    error_logs = list(
        map(lambda error_log: schemas.ErrorLogResponse(**error_log), response.items)
    )
    # if no sort required then send
    if not sort_by and not order_by:
        return {"logs": error_logs}
    # check which entry to order by
    if sort_by not in ["date_added"] and order_by not in ["asc", "desc"]:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Query",
        )
    reverse = True if order_by == "desc" else False
    # sort the logs in either ascending or descending order
    error_logs = sorted(
        error_logs, key=lambda error_log: getattr(error_log, sort_by), reverse=reverse
    )
    return {"logs": error_logs}


@router.delete("", status_code=fastapi.status.HTTP_200_OK)
async def delete_log(
    key: str, current_user: schemas.User = Depends(users.get_current_active_admin)
):
    if key == "all":
        # delete all entries
        query_resp = database.base_logs.fetch()
        for index in range(query_resp.count):
            database.base_logs.delete(key=query_resp.items[index].get("key"))
    else:
        log = database.base_logs.fetch({"key": key})
        if log.count == 0:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="No Key matched in Database",
            )
        database.base_logs.delete(log.items[0].get("key"))
    query_resp = database.base_logs.fetch()
    if query_resp.count == 0:
        logs = []
    else:
        logs = list(map(lambda log: schemas.ErrorLogResponse(**log), query_resp.items))
    return {"logs": logs}
