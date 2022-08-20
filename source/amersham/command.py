from __future__ import annotations

from .flag import Flag
from .parameter import Parameter


class Command:

    def __init__(self, 
            name: str, 
            detail: str = None, 
            help_callback: callable = None):
        
        self.name: name

        self.detail: detail
        self.help_callback = help_callback if help_callback else self.help

        self.callback: callable = None
        self.flags = []
        self.parameters = []
    
    @staticmethod
    def construct(functor: callable, arguments: dict) -> Command:
        pass
    
    def get_flag(self, name: str, alias: bool) -> Flag:
        pass

    def get_parameter(self, name: str) -> Parameter:
        pass
    
    def help(self) -> str:
        pass

    def usage(self) -> str:
        pass

    def parse(self, arguments: list) -> any:
        pass