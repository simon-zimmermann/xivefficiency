from sqlmodel import SQLModel
from flask import Flask
import json
from flask_bootstrap import Bootstrap5
import traceback
from flask_wtf.csrf import CSRFProtect

from webapp.common import util

app = Flask(__name__)
app.config.from_file("../resources/config.json", load=json.load)
app.secret_key = 'dev'
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'
SQLModel.model_config['protected_namespaces'] = ()

with app.app_context():
    # Import order is important, DO NOT import this before the SQLModel config is applied
    try:
        from webapp.db import data_enum  # noqa
        data_enum.init_enums()
    except Exception as e:
        print("Failed to initialize data enums!")
        print(f"\t{e}")

routes_to_load = ["cli.CLI", "api.admin", "api.db_tests", "routes.index", "routes.bootstrap-demo"]
for route in routes_to_load:
    # Import order is important, DO NOT import this before the SQLModel config is applied
    try:
        mod = util.import_if_exists(route, __package__)
        if (mod):
            app.register_blueprint(mod.bp)
        else:
            print(f"Failed to load routing module {route} because it does not exist.")
    except Exception as e:
        print(f"Failed to load routing module {route} with exception:")
        print(f"\t{e}")
        traceback.print_exc()
