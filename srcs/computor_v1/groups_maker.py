from srcs.computor_v1.tokens.sign import Sign
from srcs.computor_v1.tokens.group import Group
from srcs.computor_v1.expression import Expression
from srcs.computor_v1.utils.error import error


class GroupsMaker:
    def __init__(self, tokens_list):
        self.tokens = tokens_list

    def cut_by_token(self, dilimiters_list, tokens):
        result = []
        item = []
        sign = Sign('+')
        for index, token in enumerate(tokens):
            if token in dilimiters_list:
                if not item:
                    error(f'double of the sign "{token.content}"')
                result.append({'sign': sign, 'tokens': item})
                item = []
                sign = token
            else:
                item.append(token)
        if item:
            result.append({'sign': sign, 'tokens': item})

        return result

    def get_pieces(self):
        halfs = self.cut_by_token([Sign('=')], self.tokens)
        first_half = self.cut_by_token([Sign('-'), Sign('+')], halfs[0]['tokens'])
        second_half = self.cut_by_token([Sign('-'), Sign('+')], halfs[1]['tokens'])
        first_half = [Group(**x) for x in first_half]
        second_half = [Group(**x) for x in second_half]
        expression = first_half
        for group in second_half:
            expression.append(group.replase_sign())
        expression = Expression(expression)
        return expression
