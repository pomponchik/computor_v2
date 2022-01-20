from srcs.sg.objects.abstract_object import AbstractObject

from srcs.errors import RuntimeASTError


class UnionContext:
    def __init__(self, global_context, local_context, function_name, function_object):
        self.global_context = global_context
        self.local_context = local_context
        self.function_name = function_name
        self.function_object = function_object

    def __getitem__(self, key):
        key = self.convert_key(key)
        if key == self.convert_key(self.function_name):
            raise RuntimeASTError('recursion detected', self.function_object)
        if key in self.local_context:
            return self.local_context[key]
        return self.global_context[key]

    def __setitem__(self, key, value):
        key = self.convert_key(key)
        if key == self.convert_key(self.function_name):
            raise RuntimeASTError('function name overload', self.function_object)
        if key in self.local_context:
            raise RuntimeASTError('overloading a variable from the local context of a function', self.function_object)
        self.global_context[key] = value

    def get(self, key, default):
        key = self.convert_key(key)
        result = self.local_context.get(key, None)
        return result if result is not None else self.global_context.get(key, None)

    def convert_key(self, key):
        return key.lower()

class FunctionObject(AbstractObject):
    type_mark = 'm'

    def __init__(self, node, name, argument_name, body):
        self.node = node
        self.name = name
        self.argument_name = argument_name
        self.body = self.simplify_expression(body)

    def call(self, parameter, context, creator):
        context = UnionContext(context, {self.argument_name: parameter}, self.name, self)
        body_graph = creator(self.body, self.node)
        return body_graph.calculate(context)

    def simplify_expression(self, body):
        return body

    @classmethod
    def create_from_node(cls, node, body):
        ast_node = node.ast_node
        name_ast_node = ast_node.tokens[0]
        argument_ast_node = ast_node.tokens[1]

        name = name_ast_node.tokens[0].source
        argument_name = argument_ast_node.tokens[0].source
        if name == argument_name:
            raise RuntimeASTError('the names of the function and its argument are the same', node)
        return cls(node, name, argument_name, body)

    def representation(self, context):
        return self.body.clean_repr(context)

    def type_representation(self):
        return 'function'
