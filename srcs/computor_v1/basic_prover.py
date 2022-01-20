from srcs.computor_v1.utils.cut_tokens import cut_tokens
from srcs.computor_v1.utils.error import error


class BasicProver:
    def __init__(self, source_string):
        self.string = source_string.replace(' ', '')
        self.full_string = source_string

    def go(self):
        base = True
        proves = {
            'the equal sign in the expression is not exist': self.equal_sign_exist,
            'the equal sign in the expression is not only one': self.equal_sign_is_only_one,
            'the expression is not complete': self.before_and_after_equal_exist,
            'not all symbols in the expression is allowed': self.all_symbols_is_allowed,
            'the variable letter in the expression is not only one': self.letter_is_only_one,
            'extra space(s)': self.extra_space,
            'extra sign': self.extra_sugn,
        }
        for error_message, prove in proves.items():
            if not prove():
                error(error_message)
        return True

    def equal_sign_exist(self):
        return '=' in self.string

    def extra_sugn(self):
        signs = ('+', '-', '*', '.', '^',)
        halfs = self.full_string.split('=')
        for index, half in enumerate(halfs):
            half = half.strip()
            index = 'first' if not index else 'second'
            for sign in signs:
                if half[0] == sign:
                    if sign == '-':
                        if len(half) == 1:
                            error(f'missing half of the expression: "{half}"')
                        if not half[1].isdigit():
                            error(f'extra sign "{sign}" in the begin of the {index} half of the expression')
                elif half[-1] == sign:
                    error(f'extra sign "{sign}" in the end of the {index} half of the expression')
        return True

    def equal_sign_is_only_one(self):
        count = 0
        for letter in self.string:
            if letter == '=':
                count += 1
        return True if count == 1 else False

    def before_and_after_equal_exist(self):
        splitted = self.string.split('=')
        return bool(len(splitted[0])) and bool(len(splitted[1]))

    def all_symbols_is_allowed(self):
        prove = lambda letter: letter.isalpha() or letter.isdigit() or letter in ('+', '-', '*', '^', '.', '=')
        for letter in self.string:
            if not prove(letter):
                return False
        return True

    def letter_is_only_one(self):
        letters_bag = set()
        for letter in self.string:
            if letter.isalpha():
                letters_bag.add(letter)
        return len(letters_bag) == 1

    def extra_space(self):
        splited_string = self.full_string.split(' ')
        if '' in splited_string:
            return False
        return True
