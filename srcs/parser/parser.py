from srcs.lexer.lexemes.characters_lexeme import CharactersLexeme
from srcs.lexer.lexemes.number_lexeme import NumberLexeme
from srcs.lexer.lexemes.other_lexeme import OtherLexeme

from srcs.parser.tokens.unary_operator_token import UnaryOperatorToken
from srcs.parser.tokens.binary_operator_token import BinaryOperatorToken
from srcs.parser.tokens.rational_number_token import RationalNumberToken
from srcs.parser.tokens.complex_number_token import ComplexNumberToken
from srcs.parser.tokens.name_token import NameToken
from srcs.parser.tokens.open_bracket_token import OpenBracketToken
from srcs.parser.tokens.close_bracket_token import CloseBracketToken
from srcs.parser.tokens.function_definition_token import FunctionDefinitionToken
from srcs.parser.tokens.question_token import QuestionToken
from srcs.parser.tokens.equal_token import EqualToken
from srcs.parser.tokens.semicolon_token import SemicolonToken
from srcs.parser.tokens.comma_token import CommaToken
from srcs.parser.tokens.square_open_bracket_token import SquareOpenBracketToken
from srcs.parser.tokens.square_close_bracket_token import SquareCloseBracketToken

from srcs.errors import InternalLexicalError

from srcs.matcher.matcher import PatternMatcher


class Parser:
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.matcher = PatternMatcher(
            {
                'o[+]': BinaryOperatorToken,
                'o[-]': BinaryOperatorToken,
                'o[*]': BinaryOperatorToken,
                'o[*]o[*]': BinaryOperatorToken,
                'o[/]': BinaryOperatorToken,
                'o[^]': BinaryOperatorToken,
                'o[%]': BinaryOperatorToken,
                'o[(]': OpenBracketToken,
                'o[)]': CloseBracketToken,
                'o[(]': OpenBracketToken,
                'o[;]': SemicolonToken,
                'o[,]': CommaToken,
                'o[=]': EqualToken,
                'n': RationalNumberToken,
                'no[.]n': RationalNumberToken,
                'no[*]c[i]o[+]n': ComplexNumberToken,
                'no[*]c[i]o[-]n': ComplexNumberToken,
                'nc[i]o[+]n': ComplexNumberToken,
                'nc[i]o[-]n': ComplexNumberToken,
                'no[+]no[*]c[i]': ComplexNumberToken,
                'no[-]no[*]c[i]': ComplexNumberToken,
                'no[+]nc[i]': ComplexNumberToken,
                'no[-]nc[i]': ComplexNumberToken,
                'nc[i]': ComplexNumberToken,
                'no[*]c[i]': ComplexNumberToken,
                'c[i]': ComplexNumberToken,
                'o[=]o[?]': QuestionToken,
                'o[?]': QuestionToken,
                'c': NameToken,
            },
            lambda x: x.name,
            lambda x: x.source,
        )

    def tokenize(self):
        tokens = []
        index = 0

        while index < len(self.lexemes):
            lexeme = self.lexemes[index]
            if lexeme.source == '[' or lexeme.source == ']':
                if lexeme.source == '[':
                    token = SquareOpenBracketToken([lexeme], '')
                    tokens.append(token)
                else:
                    token = SquareCloseBracketToken([lexeme], '')
                    tokens.append(token)
                index += 1
            else:
                pattern = self.matcher.match(self.lexemes, index)

                if pattern is None:
                    raise InternalLexicalError('unrecognized set of lexemes', self.lexemes[index])

                token_class = pattern.result_value
                token = token_class(self.lexemes[index:index + len(pattern)], pattern.string)
                tokens.append(token)

                index += len(pattern)

        return tokens
