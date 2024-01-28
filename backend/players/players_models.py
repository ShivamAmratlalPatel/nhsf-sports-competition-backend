"""Players Database Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects import postgresql as pg

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
    order_id = Column(String)
    ticket_id = Column(String)
    barcode = Column(String)
    checked_in = Column(Boolean, nullable=False, default=False, server_default="false")
    ticket_voided = Column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    emergency_contact_name = Column(String)
    emergency_contact_number = Column(String)
    emergency_contact_relation = Column(String)
    allergies_medical_conditions = Column(String)
    original_chapter = Column(String)
