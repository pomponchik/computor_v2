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
        text = f'Syntax Error: {self.message} ("{self.token_representation()}").'
        return text

    def token_representation(self):
        begin = self.token.string[0:self.token.string_begin_index]
        inner_part = self.token.string[self.token.string_begin_index:self.token.string_end_index]
        end = self.token.string[self.token.string_end_index:]

        return f'{begin}\033[4m{inner_part}\033[0m\033[31m{end}'

class ASTError(InternalSyntaxError):
    def __str__(self):
        if self.get_left_token(self.token) is not None:
            text = f'Syntax Error: {self.message} ("{self.token_representation()}").'
            return text
        return f'Syntax Error: empty brackets or other empty expression.'

    def token_representation(self):
        print('AAA1')
        left_token = self.get_left_token(self.token)
        print('AAA2')
        right_token = self.get_right_token(self.token)

        if not hasattr(self.token, 'string'):
            self.token = left_token
        print('AAA3')

        begin = left_token.string[0:left_token.string_begin_index]
        print('AAA4', left_token, right_token)
        inner_part = left_token.string[left_token.string_begin_index:right_token.string_end_index]
        print('AAA5', right_token.string_end_index)
        try:
            end = self.token.string[right_token.string_end_index:]
        except Exception as e:
            print(e)
        print('AAA6')

        return f'{begin}\033[4m{inner_part}\033[0m\033[31m{end}'

    def get_left_token(self, node):
        if hasattr(node, 'tokens'):
            if node.tokens:
                return self.get_left_token(node.tokens[0])
            else:
                return None
        return node

    def get_right_token(self, node):
        if hasattr(node, 'tokens'):
            if node.tokens:
                return self.get_right_token(node.tokens[-1])
            else:
                return None
        return node

class RuntimeASTError(ASTError):
    def __init__(self, message, token):
        self.message = message
        self.token = token.ast_node

    def __str__(self):
        if self.get_left_token(self.token) is not None:
            print(self.token)
            text = f'Runtime Error: {self.message} ("{self.token_representation()}").'
            return text
        return f'Runtime Error: empty brackets or other empty expression.'
