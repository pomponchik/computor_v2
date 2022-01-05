class AbstractToken:
    def __init__(self, lexemes, form):
        self.lexemes = lexemes
        self.form = form
        self.source = self.get_source(lexemes)
        self.string = lexemes[0].string
        self.string_index = lexemes[0].string_index
        self.string_begin_index = lexemes[0].source_index
        self.string_end_index = lexemes[-1].source_index + len(lexemes[-1])
        self.check_lexemes()

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

    def check_lexemes(self):
        pass
