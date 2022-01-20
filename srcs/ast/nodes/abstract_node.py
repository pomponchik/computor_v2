class AbstractNode:
    def __init__(self, tokens):
        self.tokens = tokens
        self.check_tokens(tokens)

    def __repr__(self):
        tokens = ', '.join([f'"{token.source}"' if not isinstance(token, AbstractNode) else repr(token) for token in self.tokens])
        return f'{type(self).__name__}({tokens})'

    def check_tokens(self, tokens):
        pass

    def clean_repr(self, context, level=0):
        tokens = []

        for token in self.tokens:
            if isinstance(token, AbstractNode):
                if len(token.tokens) == 1:
                    tokens.append(token.clean_repr(context, level=level + 1).strip())
                elif len(token.tokens) == 3 and not isinstance(token.tokens[1], AbstractNode) and token.tokens[1].source in ('*', '/', '^', '%', '**'):
                    tokens.append(f'{token.clean_repr(context, level=level + 1)}')
                else:
                    if level == 0:
                        tokens.append(f'{token.clean_repr(context, level=level + 1)}')
                    else:
                        tokens.append(f'({token.clean_repr(context, level=level + 1)})')
            else:
                representation = self.get_token_representation(context, token.source)
                tokens.append(f' {representation} ')

        result = ''.join(tokens)

        return result

    def get_token_representation(self, context, source):
        context_item = context.get(source, None)
        if context_item is None:
            return source
        return context_item.one_string_representation(context)

    def __len__(self):
        return len(self.tokens)
