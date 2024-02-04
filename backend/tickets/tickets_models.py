"""Tickets database models."""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.dialects import postgresql as pg

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    chapter = Column(String)
    original_chapter = Column(String)
    morning_sport = Column(String)
    afternoon_sport = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_number = Column(String)
    emergency_contact_relationship = Column(String)
    allergies_medical_conditions = Column(String)
    order_id = Column(String)
    ticket_id = Column(String)
    barcode = Column(String)
    checked_in = Column(Boolean, nullable=False, default=False, server_default="false")
    ticket_voided = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    data = Column(pg.JSONB)
    update_data = Column(pg.JSONB)
    player_id = Column(pg.UUID(as_uuid=True), ForeignKey("players.id"))
    spectator_id = Column(pg.UUID(as_uuid=True), ForeignKey("spectators.id"))
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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def ticket_type(self):
        if self.player_id is not None:
            return "player"
        if self.spectator_id is not None:
            return "spectator"
        return "unknown"
