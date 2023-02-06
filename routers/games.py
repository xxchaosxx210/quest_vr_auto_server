from typing import List
import fastapi
from sqlalchemy.orm import Session

import database
import models
import schemas

router = fastapi.APIRouter(prefix="/games", tags=["Games"])

@router.get("", status_code=fastapi.status.HTTP_200_OK)
def get_games(db: Session = fastapi.Depends(database.get_db)) -> dict:
    game_models = db.query(models.Games).all()
    def get_game_schema(game: models.Games):
        return schemas.Game.from_orm(game)
    games = list(map(get_game_schema, game_models))
    return {
        "games": games
    }
    