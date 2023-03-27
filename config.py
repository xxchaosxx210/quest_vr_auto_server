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
        "url": "https://www.mediafire.com/file/87l2bnmrs0aeqhw/questcave_setup_1.0.3.exe/file",
        "mirror_url": "https://drive.google.com/file/d/1CfhG5Ae0D1rkG7dNm8wi9Hr0tFy_pgOh/view?usp=sharing",
        "description": {
            "new_features": [
                "Screen now stays on during the install process",
                "Version check. QuestCave will now notify when there is a new release",
            ],
            "bug_fixes": [
                "adb.exe could not be removed during install and uninstall. Now fixed",
            ],
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
