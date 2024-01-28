from uuid import UUID

from pydantic import BaseModel


class SpectatorRead(BaseModel):
    id: UUID
    name: str | None = None
    email: str | None = None
    chapter_id: UUID | None = None
    order_id: str | None = None
    ticket_id: str | None = None
    barcode: str | None = None
    checked_in: bool
    ticket_voided: bool
    emergency_contact_name: str | None = None
    emergency_contact_number: str | None = None
    emergency_contact_relation: str | None = None
    allergies_medical_conditions: str | None = None
    original_chapter: str | None = None
