class UnknownVariable:
    def __init__(self, letter=None):
        if not (letter is None):
            self.letter = letter

    def __new__(cls, letter=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UnknownVariable, cls).__new__(cls)
        return cls.instance
