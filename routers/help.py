import fastapi
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/help")


templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse, status_code=fastapi.status.HTTP_200_OK)
async def get_help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})
