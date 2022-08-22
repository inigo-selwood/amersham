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
            help_callback: callable = None,
            raise_exceptions = False,
            **overrides) -> callable:
        
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
        if self.get_command(command.name):
            self.fail(f"'{command.name}' already registered")
        command.raise_exceptions = self.raise_exceptions
        self.commands.append(command)
    
    def get_command(self, name: str) -> Command:
        for command in self.commands:
            if command.name == name:
                return command
        return None

    def fail(self, message: str):
        if self.raise_exceptions:
            raise ParseException(message)
        else:
            print(self.usage_text())
            print(message)
            exit(1)
    
    def help(self) -> str:
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
        if command_name == "--help" or command_name == "-h":
            if command_count > 1:
                self.fail(f"'{command_name}' followed by other arguments")
            else:
                return self.help()
        
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