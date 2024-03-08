import time
import traceback
import requests
from datetime import datetime
from sqlmodel import Session, select
from flask import Flask, current_app as app

from webapp.db import db_util, engine
from webapp.db.models.LogEntry import LogLevel
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
    db_util.log("Starting universalis data refresh")
    db_util.log(f"Requesting data for {count} items from universalis")
    for i in range(count):
        try:
            item_id = all_itemids[i]
            if i % 10 == 0:
                db_util.log(f"Requested data for {i} out of {count} items from universalis")
            refresh_single_item(item_id)
        except Exception as e:
            db_util.log(f"error while requesting data from universalis: {e}", LogLevel.ERROR)
            db_util.log(traceback.format_exc(), LogLevel.ERROR)
            pass


def scraper_thread(local_app: Flask):
    with local_app.app_context():
        db_util.log("Starting universalis scraper thread")
        while True:
            if (local_app.config["ADMIN_STATUS"]["ENABLE_SCRAPER"]):
                refresh_universalis_data()
            time.sleep(10)
