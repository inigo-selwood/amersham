class ParseException(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        pass