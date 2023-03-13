from typing import Dict, List, Union

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.routing import Mount
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


NAME = "QuestCave"
VERSION = "1.0.0"
AUTHOR = "Paul Millar"
EMAIL = "chaosad@hotmail.co.uk"


templates = Jinja2Templates(directory="templates")
# routes = [Mount("/static", app=StaticFiles(directory="static"), name="static")]


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
