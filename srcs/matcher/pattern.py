from srcs.matcher.unit import PatternUnit


class Pattern:
    def __init__(self, pattern_string, result_value, type_extractor, value_extractor):
        self.string = pattern_string
        self.result_value = result_value
        self.type_extractor = type_extractor
        self.value_extractor = value_extractor
        self.units = self.create_pattern_units(pattern_string)

    def __len__(self):
        return len(self.units)

    def __str__(self):
        return f'<pattern "{self.string}">'

    def __iter__(self):
        return iter(self.units)

    def __getitem__(self, key):
        return self.units[key]

    def create_pattern_units(self, pattern_string):
        result = []

        bracket_flag = False
        base_letter = None
        next_letter = None
        into_brackets = None

        for index, letter in enumerate(pattern_string):
            next_letter = pattern_string[index + 1] if index != len(pattern_string) - 1 else ''
            regexp_unit, bracket_flag, into_brackets, base_letter = self.create_pattern_unit(letter, base_letter, next_letter, bracket_flag, into_brackets)
            if regexp_unit is not None:
                result.append(regexp_unit)
        return result

    def create_pattern_unit(self, letter, base_letter, next_letter, bracket_flag, into_brackets):
        if letter == '[':
            if bracket_flag:
                raise ValueError('Extra token "[" in the regexp.')
            else:
                if base_letter is None:
                    raise ValueError("The value of the regular expression token must be specified in square brackets. You didn't specify a token for this.")
                if base_letter == '*':
                    raise ValueError("""Values can only be specified for "specific" regular expression elements. You cannot specify values in square brackets for element '*'.""")
                bracket_flag = True
                into_brackets = []
                result = None
                return result, bracket_flag, into_brackets, base_letter
        elif letter == ']':
            if not bracket_flag:
                raise ValueError("You close square brackets that you didn't open.")
            value = ''.join(into_brackets)
            result = PatternUnit(base_letter, value, self.type_extractor, self.value_extractor)
            bracket_flag = False
            into_brackets = None
            return result, bracket_flag, into_brackets, base_letter
        else:
            if bracket_flag:
                into_brackets.append(letter)
                result = None
            else:
                base_letter = letter
                if next_letter != '[':
                    result = PatternUnit(letter, None, self.type_extractor, self.value_extractor)
                else:
                    result = None
            return result, bracket_flag, into_brackets, base_letter
