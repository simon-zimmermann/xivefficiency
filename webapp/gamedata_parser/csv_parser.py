import os
import csv
from types import ModuleType
from sqlmodel import Session
import click
from flask import current_app as app

from webapp.gamedata_parser import csv_util
from webapp.gamedata_parser.csv_model_generator import CSVModelGenerator
from webapp.common import util
from webapp.db import models_generated, models, engine


class CSVParser:
    def __init__(self, csv_filename: str, manual_fixes: list[dict]):
        self.csv_filename = csv_filename
        self.manual_fixes = manual_fixes
        self.csv_filepath = os.path.join(*app.config["GAMEDATA_CSV_PATH"], csv_filename)
        self.model_name = self.csv_filename.split(".")[0]
        self.csv_colnames: list[str] = []
        self.csv_datatypes: list[str] = []
        self.imported_module: bool | ModuleType = False
        self.numGeneratedModels = 0
        self.numAddedToJsonConfig = 0
        self.rowsInserted = 0

        self.csvfile = open(self.csv_filepath, newline="", encoding="utf-8")
        self.csvreader = csv.reader(self.csvfile, delimiter=",", quotechar="\"")

    def __del__(self):
        self.csvfile.close()

    def parse_header(self) -> bool:
        """Parses the header of the CSV file. If a matching model class exists, it is imported.
        Returns True if a matching model class exists, False otherwise."""
        click.echo(f"Parsing header of CSV file {self.csv_filepath}")

        self.__read_header()

        # If debugging, it is possible to limit the number of columns added to the database, since there can be a lot.
        col_limit = app.config["DEBUG_LIMITS"]["DB_COLUMNS"]
        if (col_limit > 0):
            del self.csv_colnames[col_limit:]
            del self.csv_datatypes[col_limit:]

        # Check whether the model has been overridden manually.
        model_manual_path = os.path.join(models.__path__[0], self.model_name + ".py")
        if os.path.exists(model_manual_path):
            click.echo(f"Model class {self.model_name} has been overridden manually.")
            self.imported_module = util.import_if_exists(self.model_name, models.__package__)
        else:
            self.imported_module = util.import_if_exists(self.model_name, models_generated.__package__)

        return self.imported_module is not False

    def generate_model(self):
        """Generates a model class for this CSV file. The resulting model class is imported."""
        generator = CSVModelGenerator(self.model_name, self.csv_colnames, self.csv_datatypes)
        generator.generate()
        self.numGeneratedModels += 1
        self.numAddedToJsonConfig += generator.numAddedToJsonConfig
        # Import the newly generated model class.
        self.imported_module = util.import_if_exists(self.model_name, models_generated.__package__)

    def parse_body(self):
        """Parses the body of the CSV file, and add the data to the database."""
        click.echo(f"Parsing body of CSV file {self.csv_filepath}, adding to database.")

        if self.imported_module == False:
            raise RuntimeError(f"Model class {self.model_name} does not exist. Cannot parse body!")

        with Session(engine) as session:
            # For each line, build a dictionary.
            # Keys are the column names, values are the values in the csv file.
            for line_keydict in self.__read_file_byline():
                model_class = getattr(self.imported_module, self.model_name)

                # Only insert lines that are not already in the database.
                if session.get(model_class, line_keydict["id"]) is None:
                    # Actually create the ORM object, initializing it with the values from the csv file.
                    db_obj = model_class(**line_keydict)
                    session.add(db_obj)
                    self.rowsInserted += 1
            session.commit()

    def __read_header(self):
        """Reads the first three lines of the CSV file, and returns the column names and datatypes in this file."""
        indices = next(self.csvreader)
        raw_colnames = next(self.csvreader)
        raw_datatypes = next(self.csvreader)

        # check if indices are consistent. Failsafe for broken files.
        for i in range(len(indices)):
            if (i == 0) and ("key" in indices[i]):
                continue
            if int(indices[i]) + 1 == i:
                continue
            raise ValueError(f"CSV file {self.csv_filepath} could not be read."
                             f"Indices not consistent. Expected {i}, got {indices[i]}")

        # Fix the colnames and datatypes
        # Apply manual fixes
        for i in range(len(indices)):
            raw_cn = raw_colnames[i]
            raw_dt = raw_datatypes[i]

            # Skip names with empty names, but add them to the list of fixed names.
            if (raw_cn == ""):
                self.csv_colnames.append(raw_cn)
                self.csv_datatypes.append(raw_dt)
                continue

            # Make sure each colname is unique
            if raw_cn in self.csv_colnames:
                repeat_cntr = 1
                while f"{raw_cn}_{repeat_cntr}" in self.csv_colnames:
                    i += 1
                self.csv_colnames.append(f"{raw_cn}_{repeat_cntr}")
            else:
                self.csv_colnames.append(raw_cn)

            # Apply manual fixes to datatypes
            for fix in self.manual_fixes:
                if fix["model_name"] == self.model_name and fix["old_datatype"] == raw_dt:
                    raw_dt = fix["new_datatype"]
                    break
            self.csv_datatypes.append(raw_dt)

    def __read_file_byline(self):
        for row in self.csvreader:
            # Debug option: make it faster
            if (app.config["DEBUG_LIMITS"]["DB_ROWS"] > 0 and self.csvreader.line_num > app.config["DEBUG_LIMITS"]["DB_ROWS"]):
                break
            keydict = {}
            for i in range(len(self.csv_colnames)):
                # ignore empty columns
                if (self.csv_colnames[i] == ""):
                    continue
                # Convert the string into a proper datatype.
                py_datatype = csv_util.convert_datatype(self.csv_datatypes[i])
                py_colname = csv_util.convert_colname(self.csv_colnames[i])
                # insert into the id columns, not the object fields. This way the forein key relationship is established.
                if (py_datatype == "FOREIGN_KEY"):
                    py_colname += "_id"
                converted_value = csv_util.convert_value(py_datatype, row[i])
                keydict[py_colname] = converted_value
            yield keydict
