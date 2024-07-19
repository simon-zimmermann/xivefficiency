import os

from sqlmodel import SQLModel

from xivefficiency.gamedata_parser.csv_file_parser import CSVFileParser
from xivefficiency.db import models_generated
from xivefficiency.gamedata_parser.csv_model_generator import CSVModelGenerator


def delete_generated_code():
    path = models_generated.__path__[0]
    print(f"Deleting all model files in {path}.")
    files: list[str] = os.listdir(models_generated.__path__[0])
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            os.remove(os.path.join(path, filename))


def handle_csv(config: dict, engine):
    print("Parsing gamedata csv files, generating models and adding them into the database.")
    numGeneratedModels = 0
    numAddedToJsonConfig = 0
    rowsInserted = 0
    parser_list: list[CSVFileParser] = []

    for file_to_parse in config["files_to_parse"]:
        filepath_to_parse = os.path.join(*config["gamedata_csv_path"], file_to_parse)
        model_name = file_to_parse.split(".")[0]
        parser = CSVFileParser(model_name, filepath_to_parse, config, engine)
        parser_list.append(parser)

        model_exists = parser.parse_header()
        if not model_exists:
            print(f"Model class {parser.model_name} does not exist. Generating it.")
            generator = CSVModelGenerator(model_name, parser.csv_colnames, parser.csv_datatypes, config)
            generator.generate()
            numGeneratedModels += 1
            numAddedToJsonConfig += generator.numAddedToJsonConfig
            parser.import_python_module()

    if (numAddedToJsonConfig > 0):
        print(f"Added {numAddedToJsonConfig} models to the config file.")
        print("Please re-run the program to generate the new models.")
        return

    SQLModel.metadata.create_all(engine)
    # Actually read the contents of the csv files and add them to the database.
    for parser in parser_list:
        parser.parse_body()
        rowsInserted += parser.rowsInserted
        if (parser.rowsInserted > 0):
            print(f"File complete. Inserted {parser.rowsInserted} rows into the database")

    print("Successfully parsed all csv files present in config file.")
    print(f"Generated {numGeneratedModels} model classes.")
    print(f"Inserted {rowsInserted} rows into the database")
