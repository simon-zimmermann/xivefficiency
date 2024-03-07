import json
from flask import Blueprint, Response
from flask import current_app as app

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.route("/config")
def hello_world():
    return Response(json.dumps(app.config, default=str), mimetype="application/json")
