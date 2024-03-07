from enum import Enum
from sqlmodel import Session, select

from webapp.db import engine
from webapp.db.models_generated.GatheringType import GatheringType


def get_gathering_types_dict() -> dict:
    with Session(engine) as session:
        data = session.exec(select(GatheringType)).all()
        gathering_types_dict = {str(i.id): i.name for i in data}
        gathering_types_dict.pop("4")  # Remove currently unused types
        gathering_types_dict.pop("5")
        return gathering_types_dict


GatheringTypes: Enum


def init_enums():
    global GatheringTypes
    GatheringTypes = Enum("GatheringTypes", get_gathering_types_dict())
