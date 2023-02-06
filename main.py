import fastapi

from routers import games

import database

database.Base.metadata.create_all(bind=database.engine)

app = fastapi.FastAPI()

app.include_router(games.router)
