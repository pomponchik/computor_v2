class AbstractGraphNode:
    def __init__(self, ast_node, node_creator):
        self.ast_node = ast_node
        self.creator = node_creator
        self.fill_data(self.ast_node, self.creator)

    def __repr__(self):
        return f'{type(self).__name__}({self.ast_node})'

    def calculate(self, context):
        raise NotImplementedError('operation not defined')

    def fill_data(self, ast_node, creator):
        pass
