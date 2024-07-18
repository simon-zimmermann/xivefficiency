import os

from xivefficiency.code_generator.csv_parser import CSVParser
from xivefficiency.db import models_generated


def delete_generated_models():
    path = models_generated.__path__[0]
    print(f"Deleting all model files in {path}.")
    files: list[str] = os.listdir(models_generated.__path__[0])
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            os.remove(os.path.join(path, filename))


def parse_csv_files(generator_config: dict):
    print("Parsing gamedata csv files and generating model classes...")
    numGeneratedModels = 0
    numAddedToJsonConfig = 0

    for file_to_parse in generator_config["files_to_parse"]:
        filepath_to_parse = os.path.join(*generator_config["gamedata_csv_path"], file_to_parse)
        model_name = file_to_parse.split(".")[0]
        parser = CSVParser(model_name, filepath_to_parse, generator_config)

        model_exists = parser.parse_header()
        if not model_exists:
            print(f"Model class {parser.model_name} does not exist. Generating it.")
            parser.generate_model()
            numGeneratedModels += parser.numGeneratedModels
            numAddedToJsonConfig += parser.numAddedToJsonConfig

    print("Successfully parsed all csv files present in config file.")
    print(f"Generated {numGeneratedModels} model classes.")
    if (numAddedToJsonConfig > 0):
        print(f"Added {numAddedToJsonConfig} models to the config file.")
        print("Please re-run the program to generate the new models.")
