import re
from error import BrokenHandError

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN',   r'='),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MUL',      r'\*'),
    ('DIV',      r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('COMMA',    r','),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('IF',       r'\?'),
    ('WHILE',    r'@'),
    ('BOOLEAN',  r'T|F'),
    ('LT', r'<'),
    ('GT', r'>'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

KEYWORDS = {
    'print': 'PRINT',
    'f': 'FUNCTION',
    'r': 'RETURN',
    # 你可以繼續擴充關鍵字
}

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        pos = 0
        while pos < len(self.code):
            match = re.match(TOKEN_REGEX, self.code[pos:])
            if match:
                kind = match.lastgroup
                text = match.group()  # 原始字串，用來計算長度
                value = text

                if kind == 'ID' and value in KEYWORDS:
                    kind = KEYWORDS[value]
                if kind == 'NUMBER':
                    value = float(text) if '.' in text else int(text)
                elif kind == 'SKIP':
                    pos += len(text)
                    continue
                elif kind == 'NEWLINE':
                    value = '\n'

                self.tokens.append(Token(kind, value))
                pos += len(text)
            else:
                raise BrokenHandError(f"Illegal character: '{self.code[pos]}' at position {pos}")
        self.tokens.append(Token('EOF', None))
        return self.tokens

