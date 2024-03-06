import json
import os
import io
import sys
from sqlmodel import SQLModel
import click

from .csv_parser import CSVParser

from webapp.db import models_generated, engine
from webapp.common import config


def delete_generated_models():
    # First unload all modules
    click.echo("Unloading all model modules.")
    for module in list(sys.modules.keys()):
        if module.startswith("app.storingway.models"):
            del sys.modules[module]
    # Then delete all model files
    path = models_generated.__path__[0]
    click.echo(f"Deleting all model files in {path}.")
    files: list[str] = os.listdir(models_generated.__path__[0])
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            os.remove(os.path.join(path, filename))


def parse_csv() -> (int, int, int):
    click.echo("Parsing CSV files.")
    # Parse headers, create model classes. Save Parsers for later.
    parser_list: list[CSVParser] = []
    numGeneratedModels = 0
    numAddedToJsonConfig = 0
    rowsInserted = 0
    with open(config.filepath_gamedata_parser_json) as f:
        d = json.load(f)
        manual_fixes: list[dict] = d["csv"]["manual_fixes"]
        for entry in d["csv"]["files_to_parse"]:
            parser = CSVParser(entry, manual_fixes)
            parser_list.append(parser)

            model_exists = parser.parse_header()
            if not model_exists:
                click.echo(f"Model class {parser.model_name} does not exist. Generating it.")
                parser.generate_model()
                numGeneratedModels += parser.numGeneratedModels
                numAddedToJsonConfig += parser.numAddedToJsonConfig

    click.echo("Successfully parsed headers of CSV files.")

    if numAddedToJsonConfig > 0:
        click.echo("Cannot parse csv bodies, since new models have been added to gamedata_parser.json.")
    else:
        # Re-create all tables to match with model definitions.
        SQLModel.metadata.create_all(engine)
        # Actually read the contents of the csv files and add them to the database.
        for parser in parser_list:
            parser.parse_body()
            rowsInserted += parser.rowsInserted

        click.echo("Successfully parsed bodies of CSV files.")
    return numGeneratedModels, numAddedToJsonConfig, rowsInserted
