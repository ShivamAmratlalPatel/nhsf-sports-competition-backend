from uuid import UUID

from pydantic import BaseModel


class SpectatorRead(BaseModel):
    id: UUID
    name: str | None = None
    email: str | None = None
