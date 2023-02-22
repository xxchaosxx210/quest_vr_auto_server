from typing import List
import fastapi
import schemas

from database import base_games

from routers.users import get_current_active_admin, get_current_user

router = fastapi.APIRouter(prefix="/games", tags=["Games"])


@router.get(
    "", status_code=fastapi.status.HTTP_200_OK, response_model=List[schemas.Game]
)
async def get_games():
    """retrieves all the game magnets found in the database
    no authentication is required for now. May change at a later date

    Response:
        List[schemas.Game]
    """

    # game_models = db.query(models.Games).all()
    def get_game_schema(game: dict):
        return schemas.Game(**game)

    response = base_games.fetch()
    games = list(map(get_game_schema, response.items))
    return games


@router.put("/update/{key}", status_code=fastapi.status.HTTP_200_OK)
async def update_game(
    game: schemas.GameUpdateRequest,
    key: str,
    current_admin: schemas.User = fastapi.Depends(get_current_active_admin),
):
    # Cave Digger 2 - Dig Harder
    try:
        base_games.update(game.dict(exclude_unset=True), key=key)
    except Exception as err:
        raise fastapi.HTTPException(fastapi.status.HTTP_400_BAD_REQUEST, err.__str__())


@router.get(
    "/search",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=List[schemas.GameWithKey],
)
async def find_games(
    search_request: schemas.SearchGameRequest,
    current_user: schemas.User = fastapi.Depends(get_current_user),
):
    """searches the database for games using the search json query

    Args:
        search_request (schemas.SearchGameRequest):
        current_user (schemas.User, optional): _description_. Defaults to fastapi.Depends(get_current_user).

    Raises:
        fastapi.HTTPException: 404 not found error

    Returns:
        List[GameWithKey]:
    """
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
