import requests
from datetime import datetime
from sqlmodel import Session, select
from flask import current_app as app

from webapp.db import engine
from webapp.db.models.UniversalisEntry import UniversalisEntry


def get_by_item(item_id: int) -> list[UniversalisEntry]:
    with Session(engine) as session:
        statement = select(UniversalisEntry).filter(UniversalisEntry.item_id == item_id)
        return session.exec(statement).all()


def remove_by_item(item_id: int):
    with Session(engine) as session:
        items = get_by_item(item_id)
        for item in items:
            session.delete(item)
        session.commit()


def add_batch(data: list[UniversalisEntry]):
    with Session(engine) as session:
        for d in data:
            session.add(d)
        session.commit()


def refresh_single_item(item_id: int):
    # remove old entries for this item
    remove_by_item(item_id)
    # get new entries for this item
    url = f"https://universalis.app/api/v2/light/{item_id}?fields=itemID%2Clistings"
    r = requests.get(url).json()
    # add all current listings on the marketboard
    db_obj_batch: list[UniversalisEntry] = []
    for listing in r["listings"]:
        keydict = {
            "item_id": int(r["itemID"]),
            "quantity": int(listing["quantity"]),
            "hq": bool(listing["hq"]),
            "last_review_time": datetime.fromtimestamp(int(listing["lastReviewTime"])),
            "last_import_time": datetime.now(),
            "single_price": int(listing["pricePerUnit"]),
            "world_id": int(listing["worldID"]),
        }
        db_obj = UniversalisEntry(**keydict)
        db_obj_batch.append(db_obj)
    add_batch(db_obj_batch)


def refresh_universalis_data():
    # get currently available items on universalis
    url = "https://universalis.app/api/v2/marketable"
    all_itemids = requests.get(url).json()
    limit = app.config["DEBUG_LIMITS"]["UNIVERSALIS_SCRAPER"]
    count = len(all_itemids) if limit == 0 else limit
    print(f"requesting data for {count} items from universalis")
    try:
        for i in range(count):
            item_id = all_itemids[i]
            if i % 10 == 0:
                print(f"requested data for {i} out of {count} items from universalis")
            refresh_single_item(item_id)
    except Exception as e:
        print(f"error while requesting data from universalis: {e}")
        pass
