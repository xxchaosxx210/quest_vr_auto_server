from typing import List
import fastapi
import schemas

from database import base_games

from routers.users import get_current_active_admin, get_current_user

router = fastapi.APIRouter(prefix="/games", tags=["Games"])


@router.get("", status_code=fastapi.status.HTTP_200_OK)
async def get_games() -> dict:
    # game_models = db.query(models.Games).all()

    def get_game_schema(game: dict):
        return schemas.Game(**game)

    response = base_games.fetch()
    games = list(map(get_game_schema, response.items))
    return {"games": games}


@router.get(
    "/search",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=List[schemas.GameWithKey],
)
async def find_games(
    search_request: schemas.SearchGameRequest,
    current_user: schemas.User = fastapi.Depends(get_current_user),
):
    query_req = search_request.dict(exclude_unset=True)
    query_resp = base_games.fetch(query_req)
    if query_resp.count == 0:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Could not find a Game with that display name",
        )
    games = list(
        map(
            lambda index: schemas.GameWithKey(**query_resp.items[index]),
            range(query_resp.count),
        )
    )
    return games
