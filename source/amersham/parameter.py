from __future__ import annotations

import inspect


class Parameter:

    def __init__(self, 
            name: str, 
            canonical_name: str, 
            type: type, 
            description: str = ""):

        name = name.replace(" ", "-")
        name = name.replace("_", "-")
        name = name.lower()

        self.name = name
        self.canonical_name = canonical_name
        self.type = type
        
        self.description = description
    
    @staticmethod
    def construct(signature: inspect.Parameter, overrides: dict) -> Parameter:
        ''' Constructs a parameter from a function's argument signature
        
        Arguments
        ---------
        signature: inspect.Parameter
            the argument's signature information
        overrides: dict
            optional overrides for the parameter
        
        Returns
        -------
        parameter: Parameter
            the constructed parameter
        
        Raises
        ------
        exception: Exception
            if there was some configuration problem
        '''

        name = overrides["name"] if "name" in overrides else signature.name

        # Evaluate type
        permitted_types = [
            str,
            int,
            bool,
            list,
        ]
        parameter_type = signature.annotation
        if parameter_type == inspect.Parameter.empty:
            parameter_type = str
        elif parameter_type not in permitted_types:
            raise Exception(f"'{name}' type ({parameter_type}) not supported")
        
        description = ""
        if "description" in overrides:
            description = overrides["description"]
        
        return Parameter(name, signature.name, parameter_type, description)