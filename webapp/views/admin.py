from flask import Blueprint, render_template, url_for
from flask import current_app as app
import json
import os
from sqlmodel import Session, select

from webapp.calc import market_prices
from webapp.db import engine
from webapp.db.models_generated.GatheringType import GatheringType

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/sitemap")
def sitemap():
    links = []
    for rule in app.url_map.iter_rules():
        if len(rule.defaults or []) >= len(rule.arguments):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("sitemap.jinja", links=links)


@bp.route("/debug_overview")
def debug_overview():
    env_list = [f"{k}: {v}" for k, v in os.environ.items()]
    env_str = json.dumps(env_list, default=str, indent=4, sort_keys=True)
    config_str = json.dumps(app.config, default=str, indent=4, sort_keys=True)
    universalis_test_str = json.dumps(market_prices.test_average_calc(), indent=4, sort_keys=True)
    db_test_str = ""
    with Session(engine) as session:
        data = session.exec(select(GatheringType)).all()
        gathering_types_dict = {str(i.id): i.name for i in data}
        db_test_str = json.dumps(gathering_types_dict, default=str, indent=4, sort_keys=True)
    return render_template("debug_overview.jinja",
                           env_vars=env_str,
                           flask_config=config_str,
                           universalis_test=universalis_test_str,
                           db_test=db_test_str)
