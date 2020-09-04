class InvalidLanguageCode(Exception):
    
    def __init__(self,message):
        self.message = message

class TranslationError(Exception):
    
    def __init__(self,message):
        self.message = message
