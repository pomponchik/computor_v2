from srcs.lexer.lexemes.characters_lexeme import CharactersLexeme
from srcs.lexer.lexemes.number_lexeme import NumberLexeme
from srcs.lexer.lexemes.other_lexeme import OtherLexeme

from srcs.parser.tokens.unary_operator_token import UnaryOperatorToken
from srcs.parser.tokens.binary_operator_token import BinaryOperatorToken
from srcs.parser.tokens.rational_number_token import RationalNumberToken
from srcs.parser.tokens.complex_number_token import ComplexNumberToken
from srcs.parser.tokens.name_token import NameToken
from srcs.parser.tokens.name_definition_token import NameDefinitionToken
from srcs.parser.tokens.open_bracket_token import OpenBracketToken
from srcs.parser.tokens.close_bracket_token import CloseBracketToken
from srcs.parser.tokens.function_definition_token import FunctionDefinitionToken
from srcs.parser.tokens.function_call_token import FunctionCallToken
from srcs.parser.tokens.question_token import QuestionToken
from srcs.parser.tokens.equal_token import EqualToken

from srcs.errors import InternalError

from srcs.matcher.matcher import PatternMatcher


class Parser:
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.matcher = PatternMatcher(
            {
                'c': NameToken,
                'co[=]': NameDefinitionToken,
                'o[+]': BinaryOperatorToken,
                'o[-]': BinaryOperatorToken,
                'o[*]': BinaryOperatorToken,
                'o[/]': BinaryOperatorToken,
                'o[^]': BinaryOperatorToken,
                'o[%]': BinaryOperatorToken,
                'o[(]': OpenBracketToken,
                'o[)]': CloseBracketToken,
                'n': RationalNumberToken,
                'no[.]n': RationalNumberToken,
                'nc[i]': ComplexNumberToken,
                'no[.]nc[i]': ComplexNumberToken,
                'co[(]co[)]o[=]': FunctionDefinitionToken,
                'co[(]co[)]': FunctionCallToken,
                'o[=]o[?]': QuestionToken,
            },
            lambda x: x.name,
            lambda x: x.source,
        )

    def tokenize(self):
        tokens = []
        index = 0

        while index < len(self.lexemes):
            pattern = self.matcher.match(self.lexemes, index)

            if pattern is None:
                raise InternalError('incorrect syntax')

            token_class = pattern.result_value
            token = token_class(self.lexemes[index:index + len(pattern)])
            tokens.append(token)

            index += len(pattern)

        return tokens
