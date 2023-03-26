from typing import Dict, Union, Any

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


NAME = "QuestCave"
VERSION = "1.0.3"
AUTHOR = "Paul Millar"
EMAIL = "chaosad@hotmail.co.uk"


DOWNLOAD_LINKS: Dict[str, Dict[str, Any]] = {
    VERSION: {
        "url": "https://drive.google.com/file/d/1ptBAVlo6BTY6GgRrwpWlCZNMAet4X00X/view?usp=sharing",
        "mirror_url": "https://www.mediafire.com/file/r0zg89jkb4ryr31/questcave_setup_v1.0.2.exe/file",
        "description": {
            "new_features": [
                "Screen now stays on during the install process",
                "Version check. QuestCave will now notify when there is a new release",
            ],
            "bug_fixes": [],
        },
    }
}


templates = Jinja2Templates(directory="templates")


def mount_static_path(app: fastapi.FastAPI) -> None:
    """mount the static directory into the app

    Args:
        app (fastapi.FastAPI): the app to mount the static path to
    """
    app.mount("/static", app=StaticFiles(directory="static"), name="static")


def get_context(request: Request) -> Dict[str, Union[str, Request]]:
    """gets the context for the template

    Args:
        request (Request): the request object

    Returns:
        Dict[str, Union[str, Request]]: the NAME, VERSION, AUTHOR, EMAIL including the Request object
    """
    return {
        "name": NAME,
        "version": VERSION,
        "author": AUTHOR,
        "email": EMAIL,
        "request": request,
    }
