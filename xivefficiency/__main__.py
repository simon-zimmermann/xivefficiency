import json
import sys
from sqlalchemy import create_engine
from sqlmodel import SQLModel

SQLModel.model_config['protected_namespaces'] = ()

match sys.argv[1]:
    case "cleanup":
        from xivefficiency.gamedata_parser.gamedata_parser import delete_generated_code
        delete_generated_code()
    case "parser":
        from xivefficiency.gamedata_parser.gamedata_parser import handle_csv
        f = open("resources/gamedata_csv.json", "r")
        gamedata_csv_config = json.load(f)
        f.close()
        engine = create_engine("sqlite:///resources/RESTingway.db")  # TODO use config file
        handle_csv(gamedata_csv_config, engine)
