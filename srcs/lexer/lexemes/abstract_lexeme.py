class AbstractLexeme:
    def __init__(self, source, source_index, string, string_index):
        self.source = source
        self.source_index = source_index
        self.string = string
        self.string_index = string_index

    def __repr__(self):
        return f'{type(self).__name__}("{self.source}", {self.source_index})'
