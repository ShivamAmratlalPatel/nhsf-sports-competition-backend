from pydantic import BaseModel, ConfigDict


class TimetableRead(BaseModel):
    id: int
    time_activity: str
    activity_name: str
    location: str

    model_config = ConfigDict(
        from_attributes=True,
    )
