from __future__ import annotations

import inspect

from .flag import Flag
from .parameter import Parameter
from .parse_exception import ParseException
from .type import cast as type_cast, serialize as type_serialize
from .table import serialize as table_serialize


class Command:

    def __init__(self, 
            callback: callable,
            parser_name: str,
            name: str,
            description: str = "", 
            raise_exceptions = False):
        
        name = name.replace(" ", "-")
        name = name.replace("_", "-")
        name = name.lower()
        
        self.callback = callback
        self.parser_name = parser_name
        self.name = name
        self.canonical_name = callback.__name__

        self.description = description
        self.raise_exceptions = raise_exceptions

        self.flags = []
        self.parameters = []
    
    @staticmethod
    def construct(functor: callable, 
            parser_name: str,
            overrides = {},
            name = "", 
            description = "",
            raise_exceptions = False) -> Command:
        
        ''' Creates a command from a functor

        Reads signature information to construct a command, with optional
        overrides

        Arguments
        ---------
        functor: callable
            the command function to construct from
        parser_name: str
            the name of the command's parser's name
        overrides: dict
            optional overrides for the parser's arguments
        name: str
            override for the command's name
        description: str
            a short description of the command
        raise_exceptions: bool
            a flag for testing; prevents the command from printing errors and 
            quitting
        
        Returns
        -------
        command: Command
            the command generated
        
        Raises
        ------
        exception: Exception
            if you've messed up somehow
        '''
        
        command_name = name if name else functor.__name__

        command = Command(functor,
                parser_name, 
                command_name,
                description=description,
                raise_exceptions=raise_exceptions)

        parameters = inspect.signature(functor).parameters
        for name, parameter in parameters.items():

            parameter_overrides = {}
            if name in overrides:
                parameter_overrides = overrides[name]
            
            if parameter.default != inspect.Parameter.empty:
                flag = Flag.construct(parameter, parameter_overrides)
                command.add_flag(flag)
            else:
                parameter = Parameter.construct(parameter, parameter_overrides)
                command.add_parameter(parameter)

        return command
    
    def add_flag(self, new_flag: Flag):
        ''' Adds a flag to the command
        
        Arguments
        ---------
        new_flag: Flag
            the flag to add
        
        Raises
        ------
        exception: Exception
            if the flag's name or alias are already present in the command
        '''

        for flag in self.flags:

            identifier = ""
            if flag.alias and flag.alias == new_flag.alias:
                identifier = f"-{flag.alias}"
            elif flag.name == new_flag.name:
                identifier = f"--{flag.name}"
            
            message = f"'{identifier}' already registered in '{self.name}'"
            raise Exception(message)
        self.flags.append(new_flag)

    def add_parameter(self, new_parameter: Parameter):
        ''' Adds a parameter
        
        Arguments
        ---------
        new_parameter: Parameter
            the parameter to add
        
        Raises
        ------
        exception: Exception
            if the command's name is already registered
        '''

        for parameter in self.parameters:
            if parameter.name != new_parameter.name:
                continue
            message = f"'{parameter.name}' already registered in '{self.name}'"
            raise Exception(message)
        
        self.parameters.append(new_parameter)
    
    def get_flag(self, name: str, alias: bool) -> Flag:
        ''' Fetches a flag of a given name, alias or long-form
        
        Arguments
        ---------
        name: str
            the name of the flag to fetch
        alias: bool
            if the name is an alias, not long-form
        
        Returns
        -------
        flag: Flag
            the fetched flag, or None if one with a matching name/alias 
            couldn't be found
        '''

        for flag in self.flags:
            if ((alias and name == flag.alias) or 
                    (not alias and name == flag.name)):
                return flag
        return None

    def fail(self, message: str):
        ''' Fails when an input exception occurs
        
        Arguments
        ---------
        message: str
            the message to print
        
        Raises
        ------
        exception: ParseException
            if the raise exception flag is set; helps in testing, or cases
            where the user wants to handle exceptions themselves
        '''

        if self.raise_exceptions:
            raise ParseException(message)
        else:
            print(self.usage())
            print(message)
            exit(1)

    def help(self, root: bool = False) -> str:
        ''' Serializes an informative help message
        
        Arguments
        ---------
        root: bool
            if this command is the only one registered with the parser
        
        Returns
        -------
        help: str
            the help message
        '''

        result = self.usage(root=root)

        if self.description:
            result += f"\n\ndescription\n  {self.description}"

        # Enumerate flags
        flag_table = [["--help", "-h", "", "displays this message"]]
        for flag in self.flags:
            row = [
                f"--{flag.name}", 
                f"-{flag.alias}" if flag.alias else "", 
                type_serialize(flag.type),
                flag.description,
            ]
            flag_table.append(row)
        table = table_serialize(flag_table, "  ", "\n  ")
        result += f"\n\nflags\n  {table}"

        # Enumerate parameters
        if self.parameters:
            parameter_table = []

            for parameter in self.parameters:
                row = [
                    parameter.name.upper(),
                    type_serialize(parameter.type),
                    parameter.description,
                ]
                parameter_table.append(row)
            table = table_serialize(parameter_table, "  ", "\n  ")
            result += f"\n\nparameters\n  {table}"
        
        return result

    def usage(self, root: bool = False) -> str:
        ''' Prints command usage information
        
        Arguments
        ---------
        root: bool
            if the command is the only one registered with the parser
        
        Returns
        -------
        usage: str
            the usage message
        '''

        path = "" if root else f" {self.name}"
        result = f"usage\n  {self.parser_name}{path} [--help]"

        # Append flags
        for flag in self.flags:
            hint = "=" if flag.type != type(None) else ""
            result += f" [--{flag.name}{hint}]"
        
        # Append parameters
        for parameter in self.parameters:
            result += f" {parameter.name.upper()}"
        
        return result

    def run(self, arguments: list, root: bool = False) -> any:
        ''' Runs the command

        Takes user CLI input and formats its flags and parameters into
        something usable by the command callback
        
        Arguments
        ---------
        arguments: list
            the arguments (stripped of path directory and command name if 
            present
        root: bool
            if this is the only command registed with the parser
        
        Returns
        -------
        result: any
            whatever the command's callback returns
        
        Raises
        ------
        parse_error: ParseException
            if the user's input was wrong, somehow
        error: Exception
            if the parser was set-up incorrectly
        '''

        # Check for help
        if arguments and (arguments[0] == "--help" or arguments[0] == "-h"):
            if len(arguments) != 1:
                self.fail(f"'{arguments[0]}' followed by other arguments")
            print(self.help(root=root))
            return

        parameter_index = 0
        parameter_count = len(self.parameters)
        defined_flags = []

        pack = {}
        for argument in arguments:

            length = len(argument)
            if ((length >= 2 and argument[:2] == "--") or
                    (length >= 1 and argument[0] == "-")):
                
                # Unpack flag
                name = ""
                is_alias = False
                value = None
                try:
                    name, is_alias, value = Flag.parse(argument)
                except ParseException as error:
                    self.fail(f"{error}")
                
                # Try to find match
                flag = self.get_flag(name, is_alias)
                identifier = f"-{name}" if is_alias else f"--{name}"
                if not flag:
                    self.fail(f"'{identifier}' flag unexpected")
                
                # Check a value was asked for
                if value is not None and flag.type == type(None):
                    self.fail(f"'--{flag.name}' expects no value")
                
                # Check flag not already defined
                if flag.canonical_name in defined_flags:
                    self.fail(f"'--{flag.name}' defined more than once")
                defined_flags.append(flag.canonical_name)
                
                # Check flag not defined after parameters
                if parameter_index != 0:
                    self.fail(f"'--{flag.name}' follows a parameter")
                
                # Cast value to flag type
                cast_value = None
                try:
                    cast_value = type_cast(flag.type, value)
                except ParseException as error:
                    self.fail(f"'--{name}' {error}")
                
                pack[flag.canonical_name] = cast_value
            
            else:

                # Find parameter
                if parameter_index == parameter_count:
                    self.fail(f"unexpected parameter '{argument}'")
                parameter = self.parameters[parameter_index]
                
                # Cast value to flag type
                cast_value = None
                try:
                    cast_value = type_cast(parameter.type, argument)
                except ParseException as error:
                    self.fail(f"'{parameter.name}' {error}")

                pack[parameter.canonical_name] = cast_value
                parameter_index += 1
        
        # Provide default values for "boolean" flags
        for flag in self.flags:
            if flag.canonical_name not in pack and flag.type == type(None):
                pack[flag.canonical_name] = False

        # Check all the parameters we expected are present
        if parameter_index != parameter_count:
            missing_parameters = []
            for index in range(parameter_index, parameter_count):
                hint = f"'{self.parameters[index].name}'"
                missing_parameters.append(hint)
            
            parameter_names = ", ".join(missing_parameters)
            self.fail(f"expected {parameter_names}")
            
        return self.callback(**pack)