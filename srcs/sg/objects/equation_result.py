from srcs.sg.objects.abstract_object import AbstractObject

from srcs.sg.nodes.function_definition_node import FunctionDefinitionGraphNode

from srcs.errors import RuntimeASTError

from srcs.computor_v1.basic_prover import BasicProver
from srcs.computor_v1.tokenizator import Tokenizator
from srcs.computor_v1.normalizator import Normalizator
from srcs.computor_v1.groups_maker import GroupsMaker


class EquationResultObject(AbstractObject):
    type_mark = 'e'

    def __init__(self, node, left_part, right_part):
        self.node = node
        self.left_part = left_part
        self.right_part = right_part
        self.full_equation = f'{left_part} = {right_part}'

    @classmethod
    def create_from_node(cls, node, context, creator):
        left = cls.get_left_part(node, node.ast_node.tokens[0], node.ast_node, context, creator)
        right = cls.get_left_part(node, node.ast_node.tokens[2], node.ast_node, context, creator)
        return EquationResultObject(node, left, right)

    @staticmethod
    def get_left_part(node, ast_node, parent, context, creator):
        graph_node = creator(ast_node, parent)
        if isinstance(graph_node, FunctionDefinitionGraphNode):
            name = ast_node.tokens[0].tokens[0].source
            object = context.get(name, None)
            if object is None:
                raise RuntimeASTError('the function does not exist', node)
            try:
                argument_node = creator(ast_node.tokens[1], ast_node).calculate(context)
                return argument_node.representation(context)
            except RuntimeASTError as e:
                return object.representation(context)
            except Exception as e:
                return object.representation(context)
            object = graph_node.calculate(context, ast_node)
            representation = object.representation(context)
            return representation

        else:
            try:
                object = graph_node.calculate(context)
            except:
                return ast_node.cut_substring()
            representation = object.representation(context)
            return representation

    def representation(self, context):
        source_string = Normalizator(self.full_equation).get_norm_version()
        BasicProver(source_string).go()
        tokens_list = Tokenizator(source_string).get_list()
        expression = GroupsMaker(tokens_list).get_pieces()
        redused = str(expression)
        solves = expression.solve()
        if len(solves) == 1:
            return f'{redused}\nUne solution sur R:\n{solves[0]}'
        return f'{redused}\nDeux solutions sur R:\n{solves[0]}\n{solves[1]}'


    def type_representation(self):
        return 'equation result'

    def real_operation(self, other, operation, operation_node):
        raise RuntimeASTError(f'the "{operation}" operation between {self.type_representation()} and {other.type_representation()} is not defined', operation_node)
