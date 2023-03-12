# endpoint https://6vppvi.deta.dev/
# https://6vppvi.deta.dev/games

import fastapi

import config

from routers import games
from routers import logs
from routers import users
from routers import site
from routers import help


app = fastapi.FastAPI(routes=config.routes)

app.include_router(site.router)
app.include_router(help.router)
app.include_router(games.router)
app.include_router(logs.router)
app.include_router(users.router)
