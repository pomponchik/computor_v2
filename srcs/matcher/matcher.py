from srcs.matcher.pattern import Pattern


class PatternMatcher:
    def __init__(self, patterns, type_extractor, value_extractor):
        self.type_extractor = type_extractor
        self.value_extractor = value_extractor
        self.patterns = self.create_patterns(patterns)

    def match(self, iterable, index):
        for pattern in self.patterns:
            if (len(iterable) - index) >= len(pattern):
                increment = 0
                flag = True

                while increment < len(pattern):
                    pattern_unit = pattern[increment]
                    iterable_unit = iterable[index + increment]

                    if not pattern_unit.its_me(iterable_unit):
                        flag = False

                    increment += 1

                if flag:
                    return pattern

    def create_patterns(self, patterns):
        result = []

        for pattern, result_value in patterns.items():
            result.append(Pattern(pattern, result_value, self.type_extractor, self.value_extractor))

        result.sort(key=lambda x: len(x), reverse=True)
        return result
