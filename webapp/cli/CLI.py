from flask import Blueprint
import click
from sqlmodel import SQLModel
from webapp.db import engine

from webapp.gamedata_parser.parser import delete_generated_models, parse_csv

bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('parse')
def initialize_database():
    """Parse gamedata."""
    click.echo('Parsing gamedata!')
    (numGeneratedModels, numAddedToParsingwayJson, rowsInserted) = parse_csv()
    click.echo("Models generated.")
    click.echo(f"\t{numGeneratedModels} models generated.")
    click.echo(f"\t{numAddedToParsingwayJson} models added to gamedata_parser.json.")
    click.echo(f"\t{rowsInserted} rows inserted into the database.")


@bp.cli.command('clear_db')
def clear_database():
    """Clear database."""
    # First delete all generated models
    delete_generated_models()

    # Then delete all tables, and remove any references to them.
    # This is enough to re-create and re-import the tables/data, but the program still needs to be restarted.
    click.echo("Deleting all tables, and removing all references, mappers and registries.")
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.clear()

    click.echo('Database cleared; Generated code removed!')
