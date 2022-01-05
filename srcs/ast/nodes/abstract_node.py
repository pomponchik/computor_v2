class AbstractNode:
    def __init__(self, tokens):
        self.tokens = tokens

    def __repr__(self):
        tokens = ', '.join([f'"{token.source}"' if not isinstance(token, type(self)) else repr(token) for token in self.tokens])
        return f'({tokens})'

    def __len__(self):
        return len(self.tokens)
