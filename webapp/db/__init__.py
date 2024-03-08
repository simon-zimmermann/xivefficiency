from flask import current_app as app
from flask import g
from sqlmodel import SQLModel, create_engine
from werkzeug.local import LocalProxy

# The __init__.py files in those two modules will automatically import all python files in their directory
import webapp.db.models_generated
import webapp.db.models


def get_engine():
    if 'db' not in g:
        g.db = create_engine(app.config["DATABASE_URI"])

    return g.db


engine = LocalProxy(get_engine)
