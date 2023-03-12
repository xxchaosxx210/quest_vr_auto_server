# endpoint https://6vppvi.deta.dev/
# https://6vppvi.deta.dev/games

import fastapi

# from fastapi.staticfiles import StaticFiles
# from fastapi.routing import Mount
# from fastapi.templating import Jinja2Templates

from routers import games
from routers import logs
from routers import users
from routers import help


# routes = [Mount("/static", StaticFiles(directory="static"), name="static")]

app = fastapi.FastAPI()


app.include_router(games.router)
app.include_router(logs.router)
app.include_router(users.router)
app.include_router(help.router)
