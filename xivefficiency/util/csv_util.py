import re
from camel_converter import to_snake


def csv_convert_colname(csvname: str) -> str:
    """Converts the name of a column in a csv file to a valid python variable name."""
    # The id column is called "#"
    if csvname == "#":
        return "id"
    # Only the id column is allowed to be called "id"
    elif csvname.lower() == "id":
        return "param_id"
    else:
        # Remove invalid characters
        fixed_name = re.sub('[^0-9a-zA-Z_]', '', csvname)
        # If there is a leading number, add 'param_' to the beginning
        if fixed_name[0].isdigit():
            fixed_name = f"param_{fixed_name}"
        return to_snake(fixed_name)


def csv_convert_value(python_datatype: str, value: str) -> int | bool | str | None:
    """Converts a string to the proper datatype. Accepts names converted by convert_datatype()."""
    if python_datatype == "int":
        # For some reason some IDs are decimal numbers. Remove the dot, should still be unique.
        value = value.replace(".", "")
        return int(value)
    elif python_datatype == "FOREIGN_KEY":
        # For some reason some IDs are decimal numbers. Remove the dot, should still be unique.
        value = value.replace(".", "")
        return int(value)
    elif python_datatype == "bool":
        return value.lower() == "true" or value == "1"
    elif python_datatype == "str":
        return value
    elif python_datatype == "float":
        return float(value)
    else:
        return None


def csv_convert_datatype(csv_datatype: str) -> str:
    """Converts a datatype from the csv file to a valid python datatype.
    If the datatype is not recognized, it is assumed to be a foreign key, and return \"FOREIGN_KEY\"."""
    int_like = ["byte", "uint16", "uint32", "uint64", "int16", "int32", "int", "sbyte", "ubyte", "Row"]
    bool_like = ["bool"]
    # TODO int64 is supposed to be a integer, but the formatting in the csv file is strange.
    str_like = ["str", "Image", "Color", "int64"]  # TODO: fix Image, Row, Color
    float_like = ["single"]

    # special cases
    if csv_datatype.startswith("bit&"):
        return "bool"
    # list-based
    elif csv_datatype in int_like:
        return "int"
    elif csv_datatype in bool_like:
        return "bool"
    elif csv_datatype in str_like:
        return "str"
    elif csv_datatype in float_like:
        return "float"
    # Not in list -> probybly a reference to another table -> int
    else:
        return "FOREIGN_KEY"
