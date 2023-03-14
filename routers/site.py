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
async def get_help_contents(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("help-contents.html", context)


@router.get(
    "/help/quest-setup",
    response_class=HTMLResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_help_quest_setup(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("help-part1.html", context)


@router.get(
    "/help/quest-cave-guide",
    response_class=HTMLResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_help_questcave_guide(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("help-part2.html", context)


@router.get(
    "/download", status_code=fastapi.status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_download(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("download.html", context)


@router.get(
    "/contact", status_code=fastapi.status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_contact(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("contact.html", context)
