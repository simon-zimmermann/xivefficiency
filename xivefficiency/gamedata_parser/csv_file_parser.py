import csv
import os
from types import ModuleType

from sqlmodel import Session

from xivefficiency.db import models, models_generated
import xivefficiency.util as util


class CSVFileParser:
    def __init__(self, model_name: str, csv_filepath: str, config: dict, engine):
        self.config = config
        self.manual_fixes = config["manual_fixes"]
        self.model_name: str = model_name
        self.csv_filepath: str = csv_filepath
        self.csv_colnames: list[str] = []
        self.csv_datatypes: list[str] = []
        self.imported_module: bool | ModuleType = False
        self.engine = engine
        self.numGeneratedModels = 0
        self.numAddedToJsonConfig = 0
        self.rowsInserted = 0

        self.csvfile = open(self.csv_filepath, newline="", encoding="utf-8")
        self.csvreader = csv.reader(self.csvfile, delimiter=",", quotechar="\"")

    def __del__(self):
        self.csvfile.close()

    def import_python_module(self):
        # Check whether the model has been overridden manually.
        model_manual_path = os.path.join(models.__path__[0], self.model_name + ".py")
        if os.path.exists(model_manual_path):
            print(f"Model class {self.model_name} has been overridden manually.")
            self.imported_module = util.import_if_exists(self.model_name, models.__package__)
        else:
            self.imported_module = util.import_if_exists(self.model_name, models_generated.__package__)

    def parse_header(self) -> bool:
        """Parses the header of the CSV file. If a matching model class exists, it is imported.
        Returns True if a matching model class exists, False otherwise."""
        print(f"Parsing header of CSV file {self.csv_filepath}")

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

        self.import_python_module()

        return self.imported_module is not False

    def parse_body(self):
        """Parses the body of the CSV file, and add the data to the database."""
        print(f"Parsing body of CSV file {self.csv_filepath}")

        if self.imported_module == False:
            raise RuntimeError(f"Model class {self.model_name} does not exist. Cannot parse body!")

        with Session(self.engine) as session:
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

    def __read_file_byline(self):
        for row in self.csvreader:
            # Debug option: make it faster
            if (self.config["debug_limit"] > 0 and self.csvreader.line_num > self.config["debug_limit"]):
                break
            keydict = {}
            for i in range(len(self.csv_colnames)):
                # ignore empty columns
                if (self.csv_colnames[i] == ""):
                    continue
                # Convert the string into a proper datatype.
                py_datatype = util.csv_convert_datatype(self.csv_datatypes[i])
                py_colname = util.csv_convert_colname(self.csv_colnames[i])
                # insert into the id columns, not the object fields. This way the forein key relationship is established.
                if (py_datatype == "FOREIGN_KEY"):
                    py_colname += "_id"
                converted_value = util.csv_convert_value(py_datatype, row[i])
                keydict[py_colname] = converted_value
            yield keydict
