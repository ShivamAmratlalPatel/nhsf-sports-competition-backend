"""Players Database Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Player(Base):
    """Player database model."""

    __tablename__ = "players"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime_now(),
        server_default=func.timezone("Europe/London", func.current_timestamp()),
    )
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone("Europe/London", func.current_timestamp()),
    )
    morning_team_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
    )
    afternoon_team_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
    )
    cards = Column(pg.JSONB, nullable=False, default=[], server_default="[]")
    tickets = relationship("Ticket")

    @property
    def has_ticket(self):
        """Check if player has a ticket."""
        output = False
        for ticket in self.tickets:
            if ticket.is_deleted is False:
                output = True
                break
        return output
