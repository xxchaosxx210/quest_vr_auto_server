# endpoint https://6vppvi.deta.dev/
# https://6vppvi.deta.dev/games

import fastapi

import config

from routers import games
from routers import logs
from routers import users
from routers import site


app = fastapi.FastAPI()

config.mount_static_path(app)

app.include_router(site.router)
app.include_router(games.router)
app.include_router(logs.router)
app.include_router(users.router)
