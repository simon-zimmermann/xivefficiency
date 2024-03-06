
from flask import current_app as app
from sqlmodel import create_engine, SQLModel
# from app.common import config

# The __init__.py files in those two modules will automatically import all python files in their directory
import webapp.db.models
import webapp.db.models_generated

from flask import g

from werkzeug.local import LocalProxy


def get_engine():
    if 'db' not in g:
        g.db = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    return g.db


engine = LocalProxy(get_engine)

# engine = create_engine("sqlite:///resources/RESTingway.db")


# engine = create_engine("sqlite:///resources/RESTingway.db")

# class Base(DeclarativeBase):
#     pass
#
#
# engine = SQLAlchemy(model_class=Base)
#
