class Parameter:

    def __init__(self, name: str, type: type, detail: str = None):
        self.name = name
        self.type = type
        
        self.detail = detail
    
    def validate(self, value: any):
        pass