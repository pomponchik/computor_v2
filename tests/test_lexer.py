import pytest

from srcs.lexer.lexer import Lexer

from srcs.lexer.lexemes.characters_lexeme import CharactersLexeme
from srcs.lexer.lexemes.number_lexeme import NumberLexeme
from srcs.lexer.lexemes.other_lexeme import OtherLexeme


def test_create_lexemes_1():
    string = '(abc + ghn)- 7'

    lexemes = Lexer(string, 1).get_lexemes()
    lexemes_labels = [x.name for x in lexemes]
    lexemes_numbers = [x.source_index for x in lexemes]

    assert lexemes_labels == list('ococoon')
    assert lexemes_numbers == [0, 1, 5, 7, 10, 11, 13]


def test_create_lexemes_2():
    string = '+ (lel)'

    lexemes = Lexer(string, 1).get_lexemes()
    lexemes_labels = [x.name for x in lexemes]
    lexemes_numbers = [x.source_index for x in lexemes]

    assert lexemes_labels == list('ooco')
    assert lexemes_numbers == [0, 2, 3, 6]
