import inspect

from .table import serialize as table_serialize

from .flag import Flag


class Parameter:

    def __init__(self, description: str, name: str = None):
        self.description = description

        self.name = name


class Command:

    def __init__(self, 
            description: str, 
            parser_name: str,
            functor: callable, 
            definitions: dict,
            command_name: str = None):
        
        """ Constructs a command from a functor

        Tries to infer as much as possible from the function signature, ie:
        - Command name
        - Flag, parameter names
        - Default values

        The rest should be provided in the definitions dict
        
        Arguments
        ---------
        description: some information about the command
        parser_name: the name of the program
        functor: the function bound to this command
        definitions: information about each argument
        command_name: optional override for the command's name

        Usage
        -----

        ```
        >>> def callback(parameter: str, flag: str):
        ...     pass
        >>> definitions = {
        ...     "flag" = Flag("a flag"),
        ...     "parameter" = Parameter("a flag"),
        ... }
        >>> command = Command("a command", "my-program", callback, definitions)
        ```
        """
        
        self.description = description
        self.name = command_name if command_name else functor.__name__
        self.parser_name = parser_name

        self._functor = functor
        self._flags = []
        self._parameters = []

        reserved_aliases = []
        parameter_names = []

        signature = inspect.signature(functor)
        for argument_name, argument in signature._parameters.items():

            # Check argument defined
            if argument_name not in definitions:
                raise Exception(f"'{argument_name}' undefined")

            # Handle flags
            definition = definitions[argument_name]
            if isinstance(definition, Flag):

                # Evaluate name
                flag_name = definition.name
                if not flag_name:
                    flag_name = argument_name
                
                # Check flag has default value
                if (argument.default == inspect.Parameter.empty and 
                        not argument.annotation == bool):
                    message = f"'--{argument_name}' has no default value"
                    raise Exception(message)
                
                # Evaluate alias; if none given, take slices of name until 
                # something unique resolved
                alias = definition.alias
                end = 1
                while not alias or alias in reserved_aliases:
                    alias = flag_name[:end]
                    end += 1

                    if end == len(flag_name):
                        message = f"no unique alias for '--{definition.name}'"
                        raise Exception(message)
                reserved_aliases.append(alias)
                
                # Work out expected value count
                value_count = definition.value_count
                if value_count is None:
                    default = argument.default
                    if default == inspect.Parameter.empty:
                        value_count = 0
                    elif isinstance(default, list):
                        value_count = -1
                    else:
                        value_count = 1

                flag = Flag(definition.description, 
                        name=flag_name, 
                        alias=alias, 
                        value_count=value_count)
                self.add_flag(flag)

            # Handle parameters
            elif isinstance(definition, Parameter):

                # Evaluate name
                parameter_name = definition.name
                if not parameter_name:
                    parameter_name = argument_name
                            
                parameter = Parameter(definition.description, 
                        name=parameter_name)
                self.add_parameter(parameter)

            else:
                message = f"'{argument_name}' definition not Flag or Parameter"
                raise Exception(message)
    
    def _usage(self) -> str:
        """ Creates a usage message for the command

        Returns
        -------
        usage: the usage message
        """
        
        result = f"usage\n  {self.parser_name} {self.name} [--help]"

        for flag in self._flags:
            hint = "=_" if flag.value_count else ""
            result += f" [--{flag.name}{hint}]"

        for parameter in self._parameters:
            result += f" {parameter.name.upper()}"
        
        return result
    
    def _help(self) -> str:
        """ Creates a help message for the command

        Returns
        -------
        help: the help message
        """

        result = self._usage()

        result += f"\n\ndescription\n  {self.description}"

        if self._flags:
            flag_table = [
                ["--help", "-h", "displays this message"]
            ]
            for flag in self._flags:
                row = [
                    f"--{flag.name}", 
                    f"-{flag.alias}", 
                    flag.description
                ]
                flag_table.append(row)
            flags = table_serialize(flag_table, "  ", "\n  ")
            result += f"\n\nflags\n  {flags}"

        if self._parameters:
            parameter_table = []
            for parameter in self._parameters:
                parameter_table.append([parameter.name, parameter.description])
            parameters = table_serialize(parameter_table, "  ", "\n  ")
            result += f"\n\nparameters\n  {parameters}"
        
        return result
    
    def _get_flag(self, name: str, is_alias: str) -> Flag:
        """ Fetches a flag
        
        Arguments
        ---------
        name: the flag's name
        is_alias: whether the name is an alias
        
        Returns
        -------
        flag: the corresponding flag, or None if it couldn't be found
        """

        for flag in self._flags:
            if ((not is_alias and flag.name == name) or
                    (is_alias and flag.alias == name)):
                return flag
        return None
    
    def _get_parameter(self, name: str) -> Parameter:
        """ Fetches a parameter
        
        Arguments
        ---------
        name: the parameter's name
        
        Returns
        -------
        flag: the corresponding parameter, or None if it couldn't be found
        """

        for parameter in self._parameters:
            if parameter.name == name:
                return parameter
        return None
    
    def _fail(self, message: str):
        """ Prints usage and an error message """

        print(f"{self._usage()}\n\n{message}")

    def _parse(self, arguments: list) -> any:
        """ Parses arguments for the command, runs the functor

        - Establishes whether each argument is a flag or parameter
        - Checks the argument is recognized
        - Makes sure it's expected
        - Does some other stuff, too

        In the event a formatting error is encountered, prints an error message
        and exists

        Arguments
        ---------
        arguments: command line arguments, presumed prefixed with the command's
            name
        
        Returns
        -------
        result: whatever the command callback returns
        """
        
        # Check for help
        if arguments and (arguments[0] == "--help" or arguments[0] == "-h"):
            if len(arguments) != 1:
                return self._fail(f"'{arguments[0]}' expects no arguments")
            
            print(self._help())
            return None
        
        pack = {}
        
        parameter_index = 0
        parameter_count = len(self._parameters)
        defined_flags = []
        
        for argument in arguments:

            if argument[0] == "-":

                # Try to parse flag
                name = None
                is_alias = None
                values = None
                try:
                    name, is_alias, values = Flag.parse(argument)
                except Exception as parse_error:
                    return self._fail(parse_error)
                
                # Fetch flag, check not given already
                flag = self._get_flag(name, is_alias)
                if not flag:
                    identifier = f"-{name}" if is_alias else f"--{name}"
                    return self._fail(f"unexpected flag '{identifier}'")
                elif flag.name in defined_flags:
                    message = f"'--{flag.name}' defined multiple times"
                    return self._fail(message)
                defined_flags.append(flag)

                # Verify value count
                value_count = 0
                if isinstance(values, list):
                    value_count = len(values)
                elif values:
                    value_count = 1

                if not flag.value_count and values:
                    return self._fail(f"'--{flag.name}' expects no values")
                elif ((not value_count and flag.value_count == -1) or
                        (value_count != flag.value_count)):
                    return self._fail(f"wrong value count for '--{flag.name}'")

                # Evaluate value; trim if list, or just provide bool
                value = None
                if values and len(values) == 1:
                    value = values[0]
                elif values:
                    value = values
                else:
                    value = True
                
                pack[flag.name] = value
            
            else:
                
                # Check parameter expected
                if parameter_index == parameter_count:
                    return self._fail(f"unexpected parameter '{argument}'")
                
                name = self._parameters[parameter_index].name
                parameter_index += 1

                pack[name] = argument
            
        # Ensure all parameters present
        if parameter_index != parameter_count:
            parameter_names = []
            for parameter in self._parameters:
                parameter_names.append(parameter.name)
            parameters = ", ".join(parameter_names)
        
            return self._fail(f"missing parameters ({parameters})")
        
        # Provide default values for all boolean flags
        for flag in self._flags:
            if flag.name not in pack:
                pack[flag.name] = False
        
        return self._functor(**pack)
    
    def add_flag(self, flag: Flag):
        if self._get_flag(flag.name, False):
            raise Exception(f"'{self.name}' already has flag '{flag.name}'")
        self._flags.append(flag)
    
    def add_parameter(self, parameter: Parameter):
        if self._get_parameter(parameter.name):
            message = f"'{self.name}' already has parameter '{parameter.name}'"
            raise Exception(message)
        self._parameters.append(parameter)