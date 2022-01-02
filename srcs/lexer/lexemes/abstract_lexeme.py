class AbstractLexeme:
    def __init__(self, source, source_index, string, string_index):
        self.source = source
        self.source_index = source_index
        self.string = string
        self.string_index = string_index
        self.previous_is_space = False if source_index == 0 else True if string[source_index - 1].isspace() else False

    def __repr__(self):
        return f'{type(self).__name__}("{self.source}", {self.source_index})'

    def __len__(self):
        return len(self.source)

    def __eq__(self, other):
        if type(other) is type(self):
            if other.source == self.source:
                return True
        return False
