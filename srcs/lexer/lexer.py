from srcs.lexer.lexemes.characters_lexeme import CharactersLexeme
from srcs.lexer.lexemes.number_lexeme import NumberLexeme
from srcs.lexer.lexemes.other_lexeme import OtherLexeme


class Lexer:
    def __init__(self, string, string_number):
        self.string = string
        self.string_number = string_number

    def get_lexemes(self):
        substrings = self.get_splitted_substrings()

        all_lexemes = []

        for index, substring in substrings:
            lexemes = self.get_lexemes_from_substring(substring, index)
            for lexeme in lexemes:
                all_lexemes.append(lexeme)

        all_lexemes = self.post_processing(all_lexemes)

        return all_lexemes

    def post_processing(self, all_lexemes):
        result = []
        index = 0

        while index < len(all_lexemes):
            current_lexeme = all_lexemes[index]
            if current_lexeme.source == '-':
                if index != (len(all_lexemes) - 1):
                    next_lexeme = all_lexemes[index + 1]
                    if isinstance(next_lexeme, NumberLexeme) and not next_lexeme.previous_is_space:
                        new_lexeme = NumberLexeme(current_lexeme.source + next_lexeme.source, current_lexeme.source_index, current_lexeme.string, current_lexeme.string_index)
                        result.append(new_lexeme)
                        index += 2
                    else:
                        result.append(current_lexeme)
                        index += 1
                else:
                    result.append(current_lexeme)
                    index += 1
            else:
                result.append(current_lexeme)
                index += 1

        return result

    def get_lexemes_from_substring(self, substring, index):
        result = []

        characters = []
        numbers = []
        others = []

        previous_letter = ''
        last_index = 0

        for increment, letter in enumerate(substring):
            letter_index = index + increment

            if letter.isalpha():
                if not previous_letter.isalpha():
                    if numbers:
                        result.append(NumberLexeme(''.join(numbers), last_index, self.string, self.string_number))
                        numbers = []
                    elif others:
                        for other_index, other in enumerate(others):
                            result.append(OtherLexeme(other, last_index + other_index, self.string, self.string_number))
                        others = []
                    last_index = letter_index
                characters.append(letter)
            elif letter.isdigit():
                if not previous_letter.isdigit():
                    if characters:
                        result.append(CharactersLexeme(''.join(characters), last_index, self.string, self.string_number))
                        characters = []
                    elif others:
                        for other_index, other in enumerate(others):
                            result.append(OtherLexeme(other, last_index + other_index, self.string, self.string_number))
                        others = []
                    last_index = letter_index
                numbers.append(letter)
            else:
                if not ((not previous_letter.isdigit()) and (not previous_letter.isalpha())):
                    if numbers:
                        result.append(NumberLexeme(''.join(numbers), last_index, self.string, self.string_number))
                        numbers = []
                    elif characters:
                        result.append(CharactersLexeme(''.join(characters), last_index, self.string, self.string_number))
                        characters = []
                    last_index = letter_index
                others.append(letter)

            previous_letter = letter

        if characters:
            result.append(CharactersLexeme(''.join(characters), last_index, self.string, self.string_number))
        elif numbers:
            result.append(NumberLexeme(''.join(numbers), last_index, self.string, self.string_number))
        else:
            for other_index, other in enumerate(others):
                result.append(OtherLexeme(other, last_index + other_index, self.string, self.string_number))

        return result


    def get_splitted_substrings(self):
        result = []
        buffer = []
        last_index = 0
        previous_letter = ''

        for index, letter in enumerate(self.string):
            if not letter.isspace():
                if previous_letter.isspace():
                    last_index = index
                buffer.append(letter)
            else:
                if buffer:
                    substring = ''.join(buffer)
                    item = (last_index, substring)
                    result.append(item)
                    buffer = []
            previous_letter = letter

        if buffer:
            substring = ''.join(buffer)
            item = (last_index, substring)
            result.append(item)

        return result
