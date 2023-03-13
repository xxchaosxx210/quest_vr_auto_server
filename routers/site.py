import fastapi
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

import config

router = APIRouter(prefix="")


@router.get(
    "/index", response_class=HTMLResponse, status_code=fastapi.status.HTTP_200_OK
)
def get_index(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("index.html", context)


@router.get(
    "/help",
    response_class=HTMLResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_help(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("help.html", context)
