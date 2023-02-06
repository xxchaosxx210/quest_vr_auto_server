import fastapi
import schemas

from database import db

router = fastapi.APIRouter(prefix="/games", tags=["Games"])


@router.get("", status_code=fastapi.status.HTTP_200_OK)
def get_games() -> dict:
    # game_models = db.query(models.Games).all()

    def get_game_schema(game: dict):
        return schemas.Game(**game)

    response = db.fetch()
    games = list(map(get_game_schema, response.items))
    return {"games": games}
