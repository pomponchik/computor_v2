from srcs.computor_v1.tokens.abstract_token import AbstractToken
from srcs.computor_v1.utils.error import error


class Sign(AbstractToken):
    def prove_of_piece(self):
        if not self.piece_of_string in ('+', '-', '*', '='):
            error(f'unidentified token {self.piece_of_string}')

    def get_content(self):
        return self.piece_of_string

    def invert(self):
        if self.content == '+':
            self.content = '-'
        elif self.content == '-':
            self.content = '+'
