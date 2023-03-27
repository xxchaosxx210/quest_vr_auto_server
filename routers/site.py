from typing import Dict, Any
import fastapi
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

import config
import schemas

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
    "/help/faq", response_class=HTMLResponse, status_code=fastapi.status.HTTP_200_OK
)
async def get_help_faq(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("help-part3.html", context)


@router.get(
    "/download", status_code=fastapi.status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_download(request: Request):
    context = config.get_context(request)
    latest = config.DOWNLOAD_LINKS.get(config.VERSION, {})
    context["download_link_one"] = latest.get("url", "")
    context["download_link_two"] = latest.get("mirror_url", "")
    return config.templates.TemplateResponse("download.html", context)


@router.get(
    "/contact", status_code=fastapi.status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_contact(request: Request):
    context = config.get_context(request)
    return config.templates.TemplateResponse("contact.html", context)


@router.get(
    "/app-details",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=schemas.AppLatestVersionResponse,
)
async def get_app_details(request: Request):
    latest = config.DOWNLOAD_LINKS.get(config.VERSION, {})
    description = latest.get("description", {})
    context = config.get_context(request)
    context["new_features"] = description.get("new_features", [])
    context["bug_fixes"] = description.get("bug_fixes")
    description = config.templates.TemplateResponse("update.html", context).body.decode(
        "utf-8"
    )
    return schemas.AppLatestVersionResponse(
        version=config.VERSION,
        url=latest["url"],
        mirror_url=latest["mirror_url"],
        description=description,
    )
