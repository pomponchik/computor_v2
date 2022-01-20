from srcs.computor_v1.tokens.number import Number
from srcs.computor_v1.tokens.letter import Letter
from srcs.computor_v1.tokens.sign import Sign
from srcs.computor_v1.tokens.unknown_variable import UnknownVariable
from srcs.computor_v1.utils.error import error


class Group:
    def __init__(self, sign, tokens):
        self.sign = sign
        self.tokens = tokens
        self.prove_tokens()
        self.number = self.type_items(Number, '1')
        self.apply_sign()
        self.letter = self.type_items(Letter, f'{UnknownVariable().letter}^0')

    def apply_sign(self):
        if self.sign == Sign('-'):
            self.number *= Number('-1')
            self.sign = Sign('+')

    def prove_tokens(self):
        if not len(self.tokens):
            error('empty token')
        signs = ('+', '-', '*',)
        for sign in signs:
            if self.tokens[0] == Sign(sign):
                error(f'extra sign "{sign}"')
            if self.tokens[-1] == Sign(sign):
                error(f'extra sign "{sign}"')
        for index, token in enumerate(self.tokens):
            if index != (len(self.tokens) - 1):
                if token == Sign('*'):
                    if self.tokens[index + 1] == token:
                        error(f'double of a signs "*"')

    def type_items(self, target_class, init):
        items = [x for x in self.tokens if x.__class__ is target_class]
        result = target_class(init)
        for x in items:
            result *= x
        return result

    def replase_sign(self):
        if self.sign == Sign('-'):
            self.sign = Sign('+')
        else:
            self.sign = Sign('-')
        self.number *= Number('-1')
        return self

    def __repr__(self):
        if self.letter.content:
            return f'{self.number.content} * {UnknownVariable().letter}^{self.letter.content}'
        return f'{self.number.content}'
