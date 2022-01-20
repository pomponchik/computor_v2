from srcs.computor_v1.utils.error import error
from srcs.computor_v1.utils.is_number import is_number
from srcs.computor_v1.tokens.number import Number
from srcs.computor_v1.tokens.letter import Letter
from srcs.computor_v1.tokens.sign import Sign


class Tokenizator:
    def __init__(self, source_string):
        self.splitted_string = source_string.split(' ')

    def get_list(self):
        result = []
        for piece in self.splitted_string:
            token_class = self.get_token_class(piece)
            token = token_class(piece)
            result.append(token)
        return result

    @staticmethod
    def get_token_class(piece_of_string):
        if is_number(piece_of_string):
            return Number
        elif '^' in piece_of_string:
            return Letter
        elif len(piece_of_string) == 1 and piece_of_string.isalpha():
            return Letter
        elif piece_of_string in ('+', '-', '*', '^', '.', '='):
            return Sign
        error(f'unidentified token {piece_of_string}')
