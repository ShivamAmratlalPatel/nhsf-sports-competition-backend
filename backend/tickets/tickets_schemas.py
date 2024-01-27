from pydantic import BaseModel


class CustomQuestion(BaseModel):
    question: str | None = None
    answer: str | None = None


class Payload(BaseModel):
    object: str
    id: str
    add_on_id: str | None
    barcode: str
    barcode_url: str
    checked_in: str
    created_at: int
    custom_questions: list[CustomQuestion]
    description: str
    email: str
    event_id: str
    first_name: str
    full_name: str
    group_ticket_barcode: str | None
    last_name: str
    order_id: str
    qr_code_url: str
    reference: str | None
    reservation: str | None
    source: str
    status: str
    ticket_type_id: str
    updated_at: int
    voided_at: int | None


class IssuedTicketCreatedEvent(BaseModel):
    id: str
    created_at: str
    event: str
    resource_url: str
    payload: Payload


# Example usage:
json_data = {
    "id": "wh_786777",
    "created_at": "2024-01-25 02:56:51",
    "event": "ISSUED_TICKET.CREATED",
    "resource_url": "https:\\/\\/api.tickettailor.com\\/v1\\/issued_tickets\\/it_58491154",
    "payload": {
        "object": "issued_ticket",
        "id": "it_58491154",
        "add_on_id": None,
        "barcode": "ef4hEvs",
        "barcode_url": "https:\\/\\/cdn.tickettailor.com\\/userfiles\\/cache\\/barcode\\/st\\/attendee\\/58491154\\/c49b689ea123f83732be.jpg",
        "checked_in": "false",
        "created_at": 1706151411,
        "custom_questions": [
            {
                "answer": "Football, Kho, Kabaddi-Female",
                "question": "What sports are you signing up for?",
            },
        ],
        "description": "Player",
        "email": "shivam.patel.nhsf@gmail.com",
        "event_id": "ev_3535201",
        "first_name": "Test",
        "full_name": "Test Webhook",
        "group_ticket_barcode": None,
        "last_name": "Webhook",
        "order_id": "or_38526828",
        "qr_code_url": "https:\\/\\/cdn.tickettailor.com\\/userfiles\\/cache\\/barcode\\/qr\\/attendee\\/58491154\\/c49b689ea123f83732be.png",
        "reference": None,
        "reservation": None,
        "source": "checkout",
        "status": "valid",
        "ticket_type_id": "tt_3815953",
        "updated_at": 1706151411,
        "voided_at": None,
    },
}
