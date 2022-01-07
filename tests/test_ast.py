import pytest

from srcs.ast.ast import AbstractSyntaxTree
from srcs.lexer.lexer import Lexer
from srcs.parser.parser import Parser

from srcs.errors import InternalSyntaxError


def test_raise_if_extra_bracket():
    string = '())'

    lexemes = Lexer(string, 1).get_lexemes()
    tokens = Parser(lexemes).tokenize()
    with pytest.raises(InternalSyntaxError):
        ast = AbstractSyntaxTree(tokens)

def test_raise_if_wrong_bracket():
    string = '[(])'

    lexemes = Lexer(string, 1).get_lexemes()
    tokens = Parser(lexemes).tokenize()
    with pytest.raises(InternalSyntaxError):
        ast = AbstractSyntaxTree(tokens)

def test_operators_tree():
    string = 'a + a + a + a + a'

    lexemes = Lexer(string, 1).get_lexemes()
    tokens = Parser(lexemes).tokenize()
    ast = AbstractSyntaxTree(tokens)

    assert len(ast.nodes) == 1
