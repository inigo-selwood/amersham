from __future__ import annotations

import inspect

from .parse_exception import ParseException


class Flag:

    def __init__(self, 
            name: str, 
            canonical_name: str,
            alias: str, 
            type: type, 
            description = ""):
        
        if alias and alias[0] == "-":
            raise Exception(f"alias override '{alias}' has hyphen prefix")

        name = name.replace(" ", "-")
        name = name.replace("_", "-")
        name = name.lower()

        self.name = name
        self.canonical_name = canonical_name
        self.alias = alias
        self.type = type

        self.description = description
        self.canonical_name = name
    
    @staticmethod
    def construct(signature: inspect.Parameter, overrides: dict) -> Flag:
        ''' Creates a flag from a function signature's argument
        
        Arguments
        ---------
        signature: inspect.Parameter
            the argument's signature
        overrides: dict
            any optional overrides for the flag
        
        Returns
        -------
        flag: Flag
            the constructed flag
        
        Raises
        ------
        exception: Exception
            if there was some configuration problem
        '''

        name = overrides["name"] if "name" in overrides else signature.name

        # Check type
        permitted_types = [
            type(None),
            str,
            int,
            bool,
            list,
        ]
        flag_type = type(signature.default)
        if flag_type not in permitted_types:
            raise Exception(f"'--{name}' type ({flag_type}) not supported")
        
        # Evaluate alias, default, description
        alias = overrides["alias"] if "alias" in overrides else ""

        description = ""
        if "description" in overrides:
            description = overrides["description"]
        
        return Flag(name, signature.name, alias, flag_type, description)
    
    @staticmethod
    def parse(flag: str) -> tuple:
        ''' Parses a flag, as present in CLI input
        
        Arguments
        ---------
        flag: str
            the flag string representation
        
        Returns
        -------
        name, is_alias, value: tuple[str, bool, str]
            The flag's fields
        
        Raises
        ------
        parse_exception: ParseException
            if the flag was formatted wrong
        '''

        # Split tokens, check count valid
        tokens = flag.split('=')
        
        # Evaluate flag, verbose or aliased
        identifier = tokens[0]
        is_alias = None
        name = None
        if len(identifier) >= 2 and identifier[:2] == "--":
            if len(identifier) == 2:
                raise ParseException("'--' flag invalid")
        
            is_alias = False
            name = identifier[2:]
        
        elif len(identifier) >= 1 and identifier[0] == "-":
            if len(identifier) == 1:
                raise ParseException("'-' flag invalid")
            
            is_alias = True
            name = identifier[1:]

        identifier = f"-{name}" if is_alias else f"--{name}"
        token_count = len(tokens)
        if token_count > 2:
            raise ParseException(f"'{identifier}' has multiple '=' instances")
        
        # Check value, if present
        value = tokens[1] if token_count == 2 else None
        if token_count == 2 and not tokens[1]:
            raise ParseException(f"'{identifier}' value specified but empty")
        
        return (name, is_alias, value)