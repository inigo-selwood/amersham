class Flag:

    def __init__(self, 
            name: str, 
            alias: str, 
            type: type, 
            default: any, 
            detail: str = None):

        self.name = name
        self.alias = alias
        self.type = type
        self.default = default

        self.detail = detail
    
    @staticmethod
    def parse(value: str) -> tuple:
        pass

    def validate(self, name: str, alias: bool, value: any):
        pass