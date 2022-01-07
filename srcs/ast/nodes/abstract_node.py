class AbstractNode:
    def __init__(self, tokens):
        self.tokens = tokens

    def __repr__(self):
        tokens = ', '.join([f'"{token.source}"' if not isinstance(token, AbstractNode) else repr(token) for token in self.tokens])
        return f'{type(self).__name__}({tokens})'

    def __len__(self):
        return len(self.tokens)
