class AbstractToken:
    def __init__(self, piece_of_string):
        self.piece_of_string = piece_of_string
        self.prove_of_piece()
        self.content = self.get_content()

    def __repr__(self):
        name = self.__class__.__name__
        base = f'{name}("{self.piece_of_string}")'
        return base

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            if self.content == other.content:
                return True
        return False

    def prove_of_piece(self):
        raise NotImplementedError()

    def get_content(self):
        raise NotImplementedError()
