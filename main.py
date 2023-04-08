# endpoint https://6vppvi.deta.dev/
# https://6vppvi.deta.dev/games

import socket

import fastapi

import config
import schemas

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


@app.get(
    "/",
    response_model=schemas.ServerInformationResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_info(request: fastapi.requests.Request):
    hostname = socket.gethostname()
    return schemas.ServerInformationResponse(
        name=config.NAME,
        version=config.VERSION,
        author=config.AUTHOR,
        email=config.EMAIL,
        hostname=hostname,
    )
