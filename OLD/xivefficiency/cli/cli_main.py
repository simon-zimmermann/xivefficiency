# from flask import Blueprint
# import click
# import sqlalchemy
# from flask import current_app as app
#
# from webapp.gamedata_parser.parser import delete_generated_models, parse_csv
#
# bp = Blueprint('cli', __name__, cli_group=None)
#
#
# @bp.cli.command('parse')
# def initialize_database():
#    """Parse gamedata."""
#    click.echo('Parsing gamedata!')
#    (numGeneratedModels, numAddedToParsingwayJson, rowsInserted) = parse_csv()
#    click.echo("Models generated.")
#    click.echo(f"\t{numGeneratedModels} models generated.")
#    click.echo(f"\t{numAddedToParsingwayJson} models added to gamedata_parser.json.")
#    click.echo(f"\t{rowsInserted} rows inserted into the database.")
#
#
# @bp.cli.command('clear_db')
# def clear_database():
#    """Clear database."""
#    # First delete all generated models
#    delete_generated_models()
#
#    # Then delete all tables, and remove any references to them.
#    # This is enough to re-create and re-import the tables/data, but the program still needs to be restarted.
#    click.echo("Deleting all tables, and removing all references, mappers and registries.")
#    local_engine = sqlalchemy.create_engine(app.config["DATABASE_URI"], echo=True)
#    m = sqlalchemy.MetaData()
#    m.reflect(local_engine)
#    m.drop_all(local_engine)
#
#    click.echo('Database cleared; Generated code removed!')
#


# Import order is important, DO NOT import this before create_app() is called
# from webapp.universalis_scraper.scraper import scraper_thread
# threading.Thread(target=scraper_thread, args=(app,)).start()

from sqlmodel import SQLModel
from common.db import engine


def cli_main():

    print("main")
    # try:
    # data_enum.init_enums()
    SQLModel.metadata.create_all(engine)
    # except Exception as e:
    # print("Failed to initialize data enums!")
    # print(f"\t{e}")
