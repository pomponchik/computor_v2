class InternalError(ValueError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Error: {self.message}.'

class InternalLexicalError(InternalError):
    def __init__(self, message, lexeme):
        self.message = message
        self.lexeme = lexeme

    def __str__(self):
        return f'Lexical Error: {self.message} ("{self.lexeme_representation()}").'

    def lexeme_representation(self):
        begin = self.lexeme.string[0:self.lexeme.source_index]
        inner_part = self.lexeme.string[self.lexeme.source_index:self.lexeme.source_index + len(self.lexeme)]
        end = self.lexeme.string[self.lexeme.source_index + len(self.lexeme):]

        return f'{begin}\033[4m{inner_part}\033[0m\033[31m{end}'

class InternalSyntaxError(InternalError):
    def __init__(self, message, token):
        self.message = message
        self.token = token

    def __str__(self):
        return f'Syntax Error: {self.message} ("{self.token_representation()}").'

    def token_representation(self):
        begin = self.token.string[0:self.token.string_begin_index]
        inner_part = self.token.string[self.token.string_begin_index:self.token.string_end_index]
        end = self.token.string[self.token.string_end_index:]

        return f'{begin}\033[4m{inner_part}\033[0m\033[31m{end}'
