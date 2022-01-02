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

        return all_lexemes

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
