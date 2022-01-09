import pytest

from srcs.lexer.lexer import Lexer
from srcs.parser.parser import Parser
from srcs.ast.ast import AbstractSyntaxTree
from srcs.sg.sg import SemanticGraph
from srcs.executor.executor import Executor


def test_base():
    string = '(kek)'
    string_number = 5
    context = {}

    lexemes = Lexer(string, string_number).get_lexemes()

    tokens = Parser(lexemes).tokenize()

    ast = AbstractSyntaxTree(tokens)

    semantic_graph = SemanticGraph(ast)
    output = Executor(semantic_graph, context).execute()
