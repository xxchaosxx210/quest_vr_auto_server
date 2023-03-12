import fastapi
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

import config

router = APIRouter(prefix="/help")


@router.get(
    "/development-mode-setup",
    response_class=HTMLResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_help(request: Request):
    return config.templates.TemplateResponse("help.html", {"request": request})
