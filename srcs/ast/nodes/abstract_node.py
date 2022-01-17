class AbstractNode:
    def __init__(self, tokens):
        self.tokens = tokens

    def __repr__(self):
        tokens = ', '.join([f'"{token.source}"' if not isinstance(token, AbstractNode) else repr(token) for token in self.tokens])
        return f'{type(self).__name__}({tokens})'

    def clean_repr(self, level=0):
        tokens = []

        for token in self.tokens:
            if isinstance(token, AbstractNode):
                if len(token.tokens) == 1:
                    tokens.append(token.clean_repr(level=level + 1).strip())
                elif len(token.tokens) == 3 and not isinstance(token.tokens[1], AbstractNode) and token.tokens[1].source in ('*', '/', '^', '%', '**'):
                    tokens.append(f'{token.clean_repr(level=level + 1)}')
                else:
                    if level == 0:
                        tokens.append(f'{token.clean_repr(level=level + 1)}')
                    else:
                        tokens.append(f'({token.clean_repr(level=level + 1)})')
            else:
                tokens.append(f' {token.source} ')

        result = ''.join(tokens)
        
        return result


    def __len__(self):
        return len(self.tokens)
