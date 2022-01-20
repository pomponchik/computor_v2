from srcs.computor_v1.tokens.sign import Sign
from srcs.computor_v1.tokens.group import Group
from srcs.computor_v1.tokens.letter import Letter
from srcs.computor_v1.tokens.number import Number
from srcs.computor_v1.tokens.unknown_variable import UnknownVariable

from srcs.computor_v1.utils.error import error


class Expression:
    def __init__(self, items):
        self.items = items
        self.redused_items = self.reduce()
        self.degree = self.get_degree()
        self.full_form, self.full_form_dict = self.get_full_form()

    def __repr__(self):
        return ' + '.join([str(x) for x in self.redused_items]) + ' = 0'

    def __getitem__(self, key):
        if type(key) is int:
            if key in self.full_form_dict:
                return self.full_form_dict[key][0]
            elif key >= 0:
                return Group(Sign('+'), [Letter(f'{UnknownVariable().letter}^{key}'), Number('0')])
            raise KeyError(f'Expression "{self}" has no element with the degree "{key}"')
        elif type(key) is str:
            keys = {
                'a': 2,
                'b': 1,
                'c': 0,
            }
            if key not in keys:
                raise KeyError(f'The key "{key}" most be an int of a str of kind: "a", "b", "c" (from full form of the expression "ax^2 + bx + c")')
            index = keys[key]
            item = self[index]
            number = item.number.content
            return number

    def solve(self):
        if self.degree > 2:
            error("The polynomial degree is strictly greater than 2, I can't solve.")
        if self.degree == 0:
            if self[0].number.content != 0:
                error(f'The equation is made incorrectly, it follows that "{self[0].number.content} = 0". I can' + "'" + 't solve.')
            return ('[-∞:+∞]', )
        elif self.degree == 1:
            return self.solve_power_one()
        discriminant = self.discriminant()
        if self['a'] == 0:
            error('Calculating the discriminant requires division by zero, and the equation has no solution.')
        if discriminant < 0:
            discriminant *= -1
            first_part = self.round((-1 * self['b']) / (2 * self['a']))
            second_part = self.round(self.root(discriminant) / (2 * self['a']))
            return (f'{first_part} + {second_part}i', f'{first_part} - {second_part}i')
        elif discriminant == 0:
            result = self.round(-1 * (self['b'] / (2 * self['a'])))
            return (str(result),)
        result_1 = self.round((-1 * self['b'] + self.root(discriminant)) / (2 * self['a']))
        result_2 = self.round((-1 * self['b'] - self.root(discriminant)) / (2 * self['a']))
        return (str(result_1), str(result_2))

    def solve_power_one(self):
        number = self[0].number.content
        if not number:
            return ('0',)
        number *= -1
        mult = self[1].number.content
        if mult > 0:
            result = self.round(number / mult)
            return (str(result), )
        elif mult < 0:
            result = self.round((1 / mult) * number)
            return (str(result),)
        error('There is an error in the equation (the result of multiplication by 0 is not equal to 0), it is impossible to calculate.')

    def discriminant(self):
        result = self['b'] * self['b'] - 4 * self['a'] * self['c']
        return result

    @staticmethod
    def round(number):
        if int(number) == number:
            return int(number)
        return number

    @staticmethod
    def root(number, precision_factor=0.0001):
        def square(n):
            return n * n
        def good_enough(guess, number):
            return abs(square(guess) - number) < precision_factor
        def improve(guess, number):
            return ((number/guess) + guess) / 2
        def sqrt_iter(guess, number):
            return guess if good_enough(guess, number) else sqrt_iter(improve(guess, number), number)
        return sqrt_iter(1.0, number)

    def get_full_form(self):
        if self.degree == 0:
            return self.redused_items, self.grouping_by_power(self.redused_items)
        groups = self.grouping_by_power(self.redused_items)
        sign = Sign('+')
        for number in range(self.degree):
            if number not in groups:
                number_item = Number('0')
                new_group = Group(sign, [Letter(f'{UnknownVariable().letter}^{number}'), number_item])
                groups[number] = [new_group]
        return self.groups_merger(groups), groups

    def get_degree(self):
        result = 0
        for item in self.redused_items:
            content = item.letter.content
            mult = item.number.content
            if content > result and mult:
                result = content
        return result

    def reduce(self):
        groups_of_groups = self.grouping_by_power(self.items)
        result = self.groups_merger(groups_of_groups)
        return result

    def groups_merger(self, groups_dict):
        result = []
        sign = Sign('+')
        for key, value in groups_dict.items():
            number = Number('0')
            for item in value:
                number += item.number
            new_group = Group(sign, [Letter(f'{UnknownVariable().letter}^{key}'), number])
            result.append(new_group)
        result.sort(key=lambda x: x.letter.content)
        return result

    def grouping_by_power(self, items):
        result = {}
        for item in items:
            content = item.letter.content
            if content in result:
                result[content].append(item)
            else:
                result[content] = [item]
        return result
