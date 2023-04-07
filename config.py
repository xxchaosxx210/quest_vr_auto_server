from typing import Dict, Union, Any

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


NAME = "QuestCave"
VERSION = "1.0.5"
AUTHOR = "Paul Millar"
EMAIL = "chaosad@hotmail.co.uk"


DOWNLOAD_LINKS: Dict[str, Dict[str, Any]] = {
    "1.0.5": {
        "url": "https://www.mediafire.com/file/3ov5iugnek7fnkl/questcave_setup_1.0.4.exe/file",
        "mirror_url": "https://drive.google.com/file/d/19BgNOSWlrlS3Y-zPTLDaNpKBGPVQv2fe/view?usp=sharing",
        "description": {
            "new_features": [],
            "bug_fixes": [],
        },
    },
    "1.0.4": {
        "url": "https://www.mediafire.com/file/3ov5iugnek7fnkl/questcave_setup_1.0.4.exe/file",
        "mirror_url": "https://drive.google.com/file/d/19BgNOSWlrlS3Y-zPTLDaNpKBGPVQv2fe/view?usp=sharing",
        "description": {
            "new_features": [
                "User now gets notified when new games have been added",
                "Load new Games only when new Games avalible",
                "Improvements to the Admin functionality (Admin only)",
            ],
            "bug_fixes": [
                "Fixed an issue with Client not dealing with empty response from api"
            ],
        },
    },
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
