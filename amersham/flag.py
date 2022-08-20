from __future__ import annotations


class Flag:

    def __init__(self, 
            description: str, 
            name: str = None, 
            alias: str = None, 
            value_count: int = None):
        
        if name:
            name = name.replace(" ", "-")
            name = name.replace("_", "-")
            name = name.lower()

        self.description = description

        self.name = name
        self.alias = alias
        self.value_count = value_count
    
    def parse(flag: str) -> tuple:
        """ Parses a flag's fields

        - Checks if the flag is an alias ('-' prefix) or not ('--' prefix)
        - Makes sure the values (if any) are not empty

        Arguments
        ---------
        flag: the flag to parse

        Returns
        -------
        name, is_alias, value: the flag's fields

        Usage
        -----

        ```
        >>> flag = "--tokens=lorem,ipsum,dolor"
        >>> Flag.parse(flag)
        ("tokens", False, ["lorem", "ipsum", "dolor"])
        ```
        """

        # Split tokens, check count valid
        tokens = flag.split('=')
        token_count = len(tokens)
        if token_count > 2:
            raise Exception(f"multiple '=' instances in '{flag}'")
        
        # Evaluate flag, verbose or aliased
        identifier = tokens[0]
        is_alias = None
        name = None
        if len(identifier) > 2 and identifier[:2] == "--":
            is_alias = False
            if len(identifier) == 2:
                raise Exception("invalid flag '--'")
            name = identifier[2:]
        elif identifier[0] == "-":
            is_alias = True
            if len(identifier) == 1:
                raise Exception("invalid flag '-'")
            name = identifier[1:]
        
        # Check value, if present
        value = tokens[1] if len(tokens) == 2 else None
        if value is not None and not value:
            raise Exception(f"empty value in '{flag}'")

        # Split value tokens, if present
        if value and "," in value:

            value = value.split(",")
            for token in value:
                if len(token) == 0:
                    raise Exception(f"empty value token in '{flag}'")
        
        return (name, is_alias, value)