"""Ednpoints for players"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

players_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_instance = Depends(oauth2_scheme)


@players_router.post("/player", tags=["players"], description="Create player.")
def create_player(token: str = oauth2_scheme_instance) -> dict[str, str]:
    """Create a player."""
    return {"token": token, "player_name": "Random Player"}
