from srcs.parser.tokens.abstract_token import AbstractToken


class AbstractNode:
    def __init__(self, tokens):
        self.tokens = tokens
        self.check_tokens(tokens)

    def __repr__(self):
        tokens = ', '.join([f'"{token.source}"' if not isinstance(token, AbstractNode) else repr(token) for token in self.tokens])
        return f'{type(self).__name__}({tokens})'

    def cut_substring(self):
        if not self.tokens:
            return ''

        if isinstance(self.tokens[0], AbstractToken):
            left_token = self.tokens[0]
        else:
            left_token = self.tokens[0]
            while not isinstance(left_token, AbstractNode):
                left_token = left_token.tokens[0]
            while not isinstance(left_token, AbstractToken):
                left_token = left_token.tokens[0]

        if isinstance(self.tokens[-1], AbstractToken):
            right_token = self.tokens[-1]
        else:
            right_token = self.tokens[-1]
            while not isinstance(right_token, AbstractNode):
                right_token = right_token.tokens[-1]
            while not isinstance(right_token, AbstractToken):
                right_token = right_token.tokens[0]

        string = left_token
        while not hasattr(string, 'string'):
            string = string.tokens[0]
        string = string.string

        return string[left_token.string_begin_index:right_token.string_end_index]

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
