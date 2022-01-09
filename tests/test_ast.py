import pytest

from srcs.ast.ast import AbstractSyntaxTree
from srcs.lexer.lexer import Lexer
from srcs.parser.parser import Parser

from srcs.ast.nodes.branches.bracked_node import BrackedNode
from srcs.ast.nodes.branches.abstract_branche_node import AbstractBrancheNode

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

def test_extra_brackets_1():
    string = 'a+(((b+(((c))))))'

    def check_brackets(nodes):
        for node in nodes:
            if isinstance(node, AbstractBrancheNode):
                if not check_brackets(node.tokens):
                    return False
            if isinstance(node,BrackedNode):
                return False
        return True

    lexemes = Lexer(string, 1).get_lexemes()
    tokens = Parser(lexemes).tokenize()
    ast = AbstractSyntaxTree(tokens)

    assert check_brackets(ast.tokens)

def test_extra_brackets_2():
    string = 'a+(b+(с))'

    def check_brackets(nodes):
        for node in nodes:
            if isinstance(node, AbstractBrancheNode):
                if not check_brackets(node.tokens):
                    return False
            if isinstance(node,BrackedNode):
                return False
        return True

    lexemes = Lexer(string, 1).get_lexemes()
    tokens = Parser(lexemes).tokenize()
    ast = AbstractSyntaxTree(tokens)

    assert check_brackets(ast.tokens)
