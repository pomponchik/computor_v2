from srcs.parser.tokens.abstract_token import AbstractToken

from srcs.errors import InternalSyntaxError


class RationalNumberToken(AbstractToken):
    def check_lexemes(self):
        if self.form == 'no[.]n':
            if self.lexemes[-1].source[0] == '-':
                raise InternalSyntaxError('invalid token, minus after the point', self)
