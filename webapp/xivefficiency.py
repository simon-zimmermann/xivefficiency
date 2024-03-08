import threading
import time
from sqlmodel import SQLModel
from flask import Flask
import json
from flask_bootstrap import Bootstrap5
import traceback
from flask_wtf.csrf import CSRFProtect
from webapp.common import util

# set default button sytle and size, will be overwritten by macro parameters
# app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
# app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
#
# # set default icon title of table actions
# app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
# app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
# app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
# app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'


def create_app():
    app = Flask(__name__)
    app.config.from_file("../resources/config.json", load=json.load)
    app.secret_key = 'dev'
    app.extensions["bootstrap"] = Bootstrap5(app)
    # app.extensions["csrf"] = CSRFProtect(app)
    SQLModel.model_config['protected_namespaces'] = ()

    return app


def init_db(app: Flask):
    with app.app_context():
        try:
            # Import order is important, DO NOT import this before create_app() is called
            from webapp.db import data_enum, engine  # noqa
            data_enum.init_enums()
            SQLModel.metadata.create_all(engine)
        except Exception as e:
            print("Failed to initialize data enums!")
            print(f"\t{e}")


def init_views(app: Flask):
    views_to_load = ["CLI", "views.index", "views.bootstrap-demo", "views.admin"]

    for view in views_to_load:
        try:
            # Import order is important, DO NOT import this before create_app() is called
            mod = util.import_if_exists(view, __package__)
            if (mod):
                app.register_blueprint(mod.bp)
            else:
                print(f"Failed to load view module {view} because it does not exist.")
        except Exception as e:
            print(f"Failed to load view module {view} with exception:")
            print(f"\t{e}")
            traceback.print_exc()


def start_tasks(app: Flask):
    # Import order is important, DO NOT import this before create_app() is called
    from webapp.universalis_scraper.scraper import scraper_thread
    threading.Thread(target=scraper_thread, args=(app,)).start()


app = create_app()
init_db(app)
init_views(app)
start_tasks(app)
