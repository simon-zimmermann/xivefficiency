import json
import sys
from sqlmodel import SQLModel

SQLModel.model_config['protected_namespaces'] = ()

match sys.argv[1]:
    case "generator":
        from xivefficiency.code_generator.code_generator import parse_csv_files, delete_generated_models
        delete_generated_models()
        f = open("resources/code_generator_config.json", "r")
        generator_config = json.load(f)
        f.close()
        parse_csv_files(generator_config)
