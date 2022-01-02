class AbstractToken:
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.source = self.get_source(lexemes)
        self.string = lexemes[0].string
        self.string_index = lexemes[0].string_index

    def __repr__(self):
        return f'{type(self).__name__}("{self.source}")'

    def get_source(self, lexemes):
        buffer = []

        for index, lexeme in enumerate(lexemes):
            if lexeme.previous_is_space and index:
                item = f" {lexeme.source}"
            else:
                item = lexeme.source
            buffer.append(item)

        result = ''.join(buffer)
        return result
