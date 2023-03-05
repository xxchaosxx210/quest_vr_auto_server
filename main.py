# endpoint https://6vppvi.deta.dev/
# https://6vppvi.deta.dev/games

import fastapi

from routers import games
from routers import logs
from routers import users


app = fastapi.FastAPI()


app.include_router(games.router)
app.include_router(logs.router)
app.include_router(users.router)
