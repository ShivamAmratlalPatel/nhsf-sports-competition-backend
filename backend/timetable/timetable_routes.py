"""Ednpoints for timetable"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.timetable.timetable_models import Timetable
from backend.timetable.timetable_schemas import TimetableRead
from backend.utils import object_to_dict



timetable_router = APIRouter()

db_session = Depends(get_db)


@timetable_router.get("/timetable", tags=["timetable"])
def get_timetable(db: Session = db_session):
    timetables = db.query(Timetable).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(TimetableRead.model_validate(timetable))
            for timetable in timetables
        ],
    )
