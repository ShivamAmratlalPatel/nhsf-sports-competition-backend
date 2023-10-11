"""Stats schemas"""
from pydantic import BaseModel


class Stat(BaseModel):
    """Stat schmema"""

    text: str
    count: float
    icon: str
    color: str
