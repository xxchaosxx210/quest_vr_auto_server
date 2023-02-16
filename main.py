# endpoint https://6vppvi.deta.dev/

import fastapi

from routers import games
from routers import logs


app = fastapi.FastAPI()

app.include_router(games.router)
app.include_router(logs.router)
