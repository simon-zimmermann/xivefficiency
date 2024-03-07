from flask import Blueprint, jsonify
from sqlmodel import Session, select

from webapp.calc import market_prices
from webapp.db import engine
from webapp.db.models_generated.GatheringType import GatheringType

bp = Blueprint("db_tests", __name__, url_prefix="/api/db_tests")


@bp.route("/universalis_calc")
def hello_world():
    return jsonify(market_prices.test_average_calc())


@bp.route("/db_access")
def db_access():
    with Session(engine) as session:
        data = session.exec(select(GatheringType)).all()
        gathering_types_dict = {str(i.id): i.name for i in data}
        gathering_types_dict.pop("4")  # Remove currently unused types
        gathering_types_dict.pop("5")
        return jsonify(gathering_types_dict)
