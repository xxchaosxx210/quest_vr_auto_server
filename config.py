from fastapi.staticfiles import StaticFiles
from fastapi.routing import Mount
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
routes = [Mount("/static", app=StaticFiles(directory="static"), name="static")]
