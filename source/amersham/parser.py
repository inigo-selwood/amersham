from .command import Command

from .table import serialize as table_serialize


class Parser:

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

        self._commands = []
    
    def _help(self) -> str:
        """ Creates a help message for the parser

        Returns
        -------
        help: the help message
        """

        result = self._usage()

        result += f"\n\ndescription\n  {self.description}"

        result += f"\n\nflags\n  --help  -h  displays this message"

        if self._commands:
            command_table = []
            for command in self._commands:
                command_table.append([command.name, command.description])
            commands = table_serialize(command_table, "  ", "\n  ")
            result += f"\n\ncommands\n  {commands}"
        
        return result
    
    def _usage(self) -> str:
        """ Creates a usage message for the parser

        Returns
        -------
        usage: the usage message
        """

        result = f"usage\n  {self.name} [--help]"

        if self._commands:
            command_names = []
            for command in self._commands:
                command_names.append(command.name)
            commands = ", ".join(command_names)
            result += f" {{{commands}}} ..."
        
        return result
    
    def _fail(self, message: str):
        """ Prints usage and an error message """

        print(f"{self._usage()}\n\n{message}")
    
    def _get_command(self, name: str):
        """ Gets a command
        
        Arguments
        ---------
        name: the command's name
        
        Returns
        -------
        command: the command, or None if one couldn't be found
        """
        
        for command in self._commands:
            if command.name == name:
                return command
        return None

    def command(self, description: str, name: str = None, **arguments):
        """ Wrapper for registering commands

        Registers the command with the parser
        
        Arguments
        ---------
        description: some information about the command
        arguments: definitions for each argument
        """
        
        def wrapper(functor: callable):

            # Add the command
            command = Command(description, 
                    self.name,
                    functor, 
                    arguments,
                    command_name=name)
            self._commands.append(command)
            return functor
            
        return wrapper
    
    def run(self, arguments: list) -> any:
        """ Runs the parser
        
        Finds the relevant command, or maybe prints a help message
        
        Arguments
        ---------
        arguments: the command line arguments
        
        Returns
        -------
        result: whatever the command returns 
        
        Usage
        -----
        
        ```
        >>> parser = Parser("parser", "a parser")
        >>> parser.run(sys.argv[1:])
        None
        ```
        """

        if not arguments:
            return self._fail("expected a command")
        
        # Check for help
        command_name = arguments[0]
        if command_name == "--help" or command_name == "-h":
            if len(arguments) != 1:
                return self._fail(f"'{command_name}' expects no arguments")
            
            print(self._help())
            return None
        
        # Make sure command it's a potential command
        elif command_name[0] == '-':
            return self._fail(f"unexpected flag '{command_name}'")
        
        # Fetch command
        command_name = command_name
        command = self._get_command(command_name)
        if not command:
            return self._fail(f"unrecognized command '{command_name}'")
        
        return command._parse(arguments[1:])
        
