from sqlmodel import Session, select

from webapp.db.models_generated.GatheringType import GatheringType
from .api import admin
from .cli import CLI
from flask import Flask
import json
from flask import g

from .calc import market_prices
from .db import engine


app = Flask(__name__)
app.config.from_file("../resources/config.json", load=json.load)


app.register_blueprint(CLI.bp)
app.register_blueprint(admin.bp)


@app.route("/")
def hello_world():
    # return market_prices.test_average_calc()
    with Session(engine) as session:
        data = session.exec(select(GatheringType)).all()
        gathering_types_dict = {str(i.id): i.name for i in data}
        gathering_types_dict.pop("4")  # Remove currently unused types
        gathering_types_dict.pop("5")
        return gathering_types_dict


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    # if db is not None:
    #    db.close()
