class PatternUnit:
    def __init__(self, letter, clarification, type_extractor, value_extractor):
        self.letter = letter
        self.clarification = clarification
        self.type_extractor = type_extractor
        self.value_extractor = value_extractor

    def its_me(self, other):
        other_letter = self.type_extractor(other)
        other_value = self.value_extractor(other)

        if other_letter == self.letter:
            if (self.clarification is None) or (self.clarification == other_value):
                return True
        return False
