from sqlmodel import Session, select

from webapp.db.data_enum import GatheringTypes
from webapp.db.models_generated.GatheringPointBase import GatheringPointBase
from webapp.db.models_generated.GatheringItem import GatheringItem
from webapp.db.models_generated.Item import Item
from webapp.db import engine


def get_gatherable_by(gathering_type: GatheringTypes, limit: int = None) -> list[Item]:
    with Session(engine) as session:
        statement = select(GatheringPointBase).limit(limit)
        data = session.exec(statement.where(GatheringPointBase.gathering_type_id == gathering_type.name)).all()
        all_gathering_items: list[GatheringItem] = []
        for item in data:
            if (item.item0 is not None):
                all_gathering_items.append(item.item0)
            if (item.item1 is not None):
                all_gathering_items.append(item.item1)
            if (item.item2 is not None):
                all_gathering_items.append(item.item2)
            if (item.item3 is not None):
                all_gathering_items.append(item.item3)
            if (item.item4 is not None):
                all_gathering_items.append(item.item4)
            if (item.item5 is not None):
                all_gathering_items.append(item.item5)
            if (item.item6 is not None):
                all_gathering_items.append(item.item6)
            if (item.item7 is not None):
                all_gathering_items.append(item.item7)
        unique_gathering_items: list[GatheringItem] = []
        for gathering_item in all_gathering_items:
            if gathering_item not in unique_gathering_items and gathering_item is not None:
                unique_gathering_items.append(gathering_item)
        itemlist: list[Item] = [gi.item for gi in unique_gathering_items if gi.item is not None and gi.item_id != 0]
        return itemlist


def get_gatherable_all(include_untradable: bool = False) -> list[Item]:
    itemlist: list[Item] = []
    for method in GatheringTypes:
        itemlist += get_gatherable_by(method)
    if not include_untradable:
        itemlist = filter(lambda x: not x.is_untradable, itemlist)
    return itemlist
