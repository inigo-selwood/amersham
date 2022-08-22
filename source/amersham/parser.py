from .command import Command
from .table import serialize as table_serialize
from .parse_exception import ParseException


class Parser:

    def __init__(self, 
            name: str, 
            description: str = "", 
            raise_exceptions: bool = False):
        
        self.name = name

        self.description = description
        self.raise_exceptions = raise_exceptions

        self.commands = []
    
    def command(self, 
            name = "", 
            description = "", 
            raise_exceptions = False,
            **overrides) -> callable:
        ''' Decorator for registering a command with the parser
        
        Reads the signature of a function to generate a command object, with
        some optional overrides
        
        Arguments
        ---------
        name: str
            an override for the function's name
        description: str
            a short overview of the command's purpose
        raise_exceptions: bool
            set this value if you want the parser to fail silently, passing
            user input exceptions back for you to handle yourself
        overrides: dict
            optional overrides for the command's arguments
        
        Returns
        -------
        command: callable
            the generated command
        
        Raises
        ------
        exception: Exception
            if there was some configuration error
        '''
        
        def wrapper(functor: callable) -> callable:
            command = Command.construct(functor, 
                    self.name,
                    overrides,
                    name=name, 
                    description=description, 
                    raise_exceptions=raise_exceptions)
            self.add_command(command)

            return functor
        return wrapper
    
    def add_command(self, command: Command):
        ''' Adds a command
        
        Arguments
        ---------
        command: Command
            the command to add
        
        Raises
        ------
        exception: Exception
            if you messed up somehow with the command
        '''

        if self.get_command(command.name):
            raise Exception(f"'{command.name}' already registered")
        command.raise_exceptions = self.raise_exceptions
        self.commands.append(command)
    
    def get_command(self, name: str) -> Command:
        ''' Gets a command of a given name
        
        Arguments
        ---------
        name: str
            the name of the command to fetch
            
        Returns
        -------
        command: Command
            the fetched command, or None if there was no match
        '''

        for command in self.commands:
            if command.name == name:
                return command
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
    
    def help(self) -> str:
        ''' Serializes an informative help message
        
        Returns
        -------
        help: str
            the help message
        '''

        if len(self.commands) == 1:
            return self.commands[0].help(root=True)

        result = self.usage()

        if self.description:
            result += f"\n\ndescription\n  {self.description}"

        result += f"\n\nflags\n  --help  -h  displays this message"

        # Enumerate commands
        if self.commands:
            command_table = []
            for command in self.commands:
                command_table.append([command.name, command.description])
            commands = table_serialize(command_table, "  ", "\n  ")
            result += f"\n\ncommands\n  {commands}"
        
        return result

    def usage(self) -> str:
        ''' Prints parser usage information
    
        Returns
        -------
        usage: str
            the usage message
        '''

        if len(self.commands) == 1:
            return self.commands[0].usage(root=True)

        result = f"usage\n  {self.name} [--help]"

        # Enumerate commands
        if self.commands:
            command_names = []
            for command in self.commands:
                command_names.append(command.name)
            commands = ", ".join(command_names)
            result += f" {{{commands}}} ..."
        
        return result

    def run(self, arguments: list) -> any:
        ''' Runs the parser

        Takes user CLI input and formats its flags and parameters into
        something usable by the command callback; finds the relevant command
        (or delegates directly if only one exists)
        
        Arguments
        ---------
        arguments: list
            the arguments (stripped of path directory)
        
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

        # Check arguments non-empty
        for argument in arguments:
            if not argument:
                self.fail("empty argument")

        # Check command(s) registered
        command_count = len(self.commands)
        if not self.commands:
            raise Exception("no registered commands")

        # Given just 1 command, run it right away
        command = None
        if command_count == 1:
            return self.commands[0].run(arguments, root=True)

        # Given options, at least one argument (command name) needed
        if not arguments:
            self.fail("expected a command")
        
        # Handle help; check no trailing garbage
        command_name = arguments[0]
        argument_count = len(arguments)
        if command_name == "--help" or command_name == "-h":
            if argument_count > 1:
                self.fail(f"'{command_name}' followed by other arguments")
            else:
                print(self.help())
                return None
        
        # Check command name (not flag) given
        if command_name[0] == "-":
            self.fail(f"expected command, not '{command_name}'")
        
        # Find command
        command = self.get_command(command_name)
        if not command:
            self.fail(f"unrecognized command '{command_name}'")
            
        # Trim command name, run command
        arguments = arguments[1:]
        return command.run(arguments)