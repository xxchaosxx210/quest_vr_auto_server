# endpoint https://6vppvi.deta.dev/

import fastapi
import database

from routers import games


app = fastapi.FastAPI()

app.include_router(games.router)
