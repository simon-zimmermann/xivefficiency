import os
from camel_converter import to_snake

from xivefficiency.gamedata_parser.csv_column_generator import CSVColumnGenerator
from xivefficiency.db import models, models_generated


class CSVModelGenerator():

    def __init__(self, model_name: str, csv_colnames: list[str], csv_datatypes: list[str], config: dict):
        self.model_name = model_name
        self.config = config
        self.table_name = to_snake(self.model_name)
        self.csv_colnames = csv_colnames
        self.csv_datatypes = csv_datatypes
        self.numAddedToJsonConfig = 0

    def generate(self):
        """Generates a model file based on the csv column names and datatypes.
        Saves the model as a python file"""
        model_fields = ""
        import_list = []

        # Process each column, resulting in one field per column
        for i in range(len(self.csv_colnames)):
            csv_colname = self.csv_colnames[i]
            csv_datatype = self.csv_datatypes[i]

            # Skip empty columns
            if csv_colname == "":
                continue

            # Generate fields for this column
            col_gen = CSVColumnGenerator(self.model_name, csv_colname, csv_datatype, self.config)
            model_fields += col_gen.generate()

            # Check if we need to add an import
            if col_gen.foreign_model != "" \
                    and col_gen.foreign_model not in import_list \
                    and col_gen.foreign_model != self.model_name:
                import_list.append(col_gen.foreign_model)

            # Stats
            if col_gen.addedToJson:
                self.numAddedToJsonConfig += 1

        # Concat import list
        import_string = ""
        for import_entry in import_list:
            # Check if {import_entry} is automatically generated or manually written, import accordingly
            if hasattr(models, import_entry):
                import_string += f"    from db.models.{import_entry} import {import_entry}\n"
            else:
                import_string += f"    from db.models_generated.{import_entry} import {import_entry}\n"

        # Generate & save to file
        self.__generate_save_model(model_fields, import_string)

    def __generate_save_model(self, model_fields: str, import_string: str):
        # If we have imports, generate an import block
        # To fix circular imports, imports are only valid while type checking
        import_block = ""
        if import_string != "":
            import_block = f"from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n{import_string}"

        # Actual code template
        generated_code = f'''from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
{import_block}

class {self.model_name}(SQLModel, table=True):
    __tablename__ = "{self.table_name}"
    __table_args__ = {{'extend_existing': True}}
    __allow_unmapped__ = True
{model_fields}
'''
        # Save to file
        new_filename = os.path.join(models_generated.__path__[0], self.model_name + ".py")
        print(f"Saving model file {new_filename}")
        with open(new_filename, "w") as f:
            f.write(generated_code)
