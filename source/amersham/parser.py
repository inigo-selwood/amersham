from .command import Command


class Parser:

    def __init__(self, 
            name: str, 
            detail: str = None, 
            help_callback: callable = None):
        
        self.name = name
        self.detail = detail

        self.help_callback = help_callback if help_callback else self.help
        
        self.commands = []
    
    def command(self, 
            name: str = None, 
            detail: str = None, 
            **arguments) -> any:
        
        def wrapper(functor: callable) -> any:

            return functor
        return wrapper
    
    def get_command(self, name: str) -> Command:
        pass
    
    def help(self) -> str:
        pass

    def usage(self) -> str:
        pass

    def run(self, arguments: list) -> any:
        pass