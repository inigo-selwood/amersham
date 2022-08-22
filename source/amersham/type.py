from .parse_exception import ParseException


def serialize(type_name: type) -> str:
    values = {
        str: "string",
        int: "integer",
        bool: "boolean",
        type(None): "",
    }

    if type_name not in values:
        raise Exception("!")
    return values[type_name]


def cast(value_type: type, value: str) -> any:

    # NoneType expects a boolean "is-present" value
    if value_type == type(None):
        return True

    # Handle strings
    elif value_type == str:
        return value
    
    # Booleans
    elif value_type == bool:
        true_symbols = [
            "1",
            "yes",
            "y",
            "true",
        ]

        false_symbols = [
            "0",
            "no",
            "n",
            "false",
        ]

        if value.lower() in true_symbols:
            return True
        elif value.lower() in false_symbols:
            return False
        else:
            raise ParseException(f"expects boolean, got '{value}'")
    
    # Integers
    elif value_type == int:
        
        try:
            return int(value)
        except ValueError as error:
            raise ParseException(f"expects integer, got '{value}'")

    # Lists
    elif value_type == list:
        if value == "[]":
            return []
        
        tokens = value.split(",")
        for token in tokens:
            if not token:
                raise ParseException(f"empty token in list '{value}'")
        return tokens
    
    # Other
    else:
        raise Exception(f"unsupported type '{value_type}'")