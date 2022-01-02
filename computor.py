from srcs.interpretator.interpretator import Interpretator
from srcs.interpretator.console_runner import ConsoleRunner
from srcs.lexer.lexer import Lexer
from srcs.parser.parser import Parser
from srcs.ast.ast import AbstractSyntaxTree
from srcs.asg.asg import AbstractSemanticGraph
from srcs.executor.executor import Executor


def main():
    runner = ConsoleRunner(' > ')
    interpretator = Interpretator(runner)

    @interpretator()
    def responder(string, string_number, context):
        lexemes = Lexer(string, string_number).get_lexemes()
        print(lexemes)
        tokens = Parser(lexemes).tokenize()
        ast = AbstractSyntaxTree(tokens)
        semantic_graph = AbstractSemanticGraph(ast)
        output = Executor(semantic_graph, context).execute()
        return output

    interpretator.run()


if __name__ == '__main__':
    main()
