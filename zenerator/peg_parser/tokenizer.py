import re, collections

class TokenGenerator:
    Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
    keywords = {'if', 'else', 'for', 'in'}
    patterns = [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('OR', r'\|\|'),
        ('NOT', r'!'),
        ('QMARK', r'\?'),
        ('AND', r'&&'),
        ('OPR', r'[/+\-*]'),
        ('DOT', r'\.'),
        ('COLON', r':'),
        ('SEMICOLON', r';'),
        ('UNDERSCORE', r'_'),
        ('ASSIGN', r'='),
        ('SLASH', r'/'),
        ('QUOTE', r'[\'"]'),
        ('ARROW', r'[<>]'),
        ('PAREN', r'[()]'),
        ('CURLY', r'[{}]'),
        ('SQUARE', r'[\[\]]'),
        ('COMMA', r','),
        ('NAME', r'[A-Za-z]+'),
        ('NEWLINE', r'\n'),
        ('WHTSPC', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    regex = '|'.join(f"(?P<{name}>{regex})" for name, regex in patterns)

    @classmethod
    def generate_tokens(cls, data):
        line_num = 1
        line_start = 0
        for mo in re.finditer(cls.regex, data):
            name = mo.lastgroup
            value = mo.group(name)
            column = mo.start() - line_start
            if name == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif name == 'NAME' and value in cls.keywords:
                name = value
            yield cls.Token(name, value, line_num, column)

class Tokenizer:

    def __init__(self, code):
        self.token_gen = TokenGenerator().generate_tokens(code)
        self.tokens = []
        self.tokens_string = []
        self.pos = 0

    def mark(self):
        return self.pos

    def reset(self, pos):
        self.pos = pos

    def get_token(self):
        token = self.peek_token()
        self.pos += 1
        return token

    def get_string(self, pos):
        return ''.join(self.tokens_string[pos:self.pos])

    def peek_token(self):
        if self.pos == len(self.tokens):
            self.tokens.append(next(self.token_gen))
        return self.tokens[self.pos]
        