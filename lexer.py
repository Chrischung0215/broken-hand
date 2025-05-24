import re
from error import BrokenHandError

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('BOOLEAN',  r'T|F'),
    ('STRING',   r'"[^"\n]*"'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('EQ',       r'=='),
    ('NE',       r'!='),
    ('LE',       r'<='),
    ('GE',       r'>='),
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
    ('AND',      r'&&'),
    ('OR',       r'\|\|'),
    ('LT',       r'<'),
    ('GT',       r'>'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

KEYWORDS = {
    'print': 'PRINT',
    'f': 'FUNCTION',
    'r': 'RETURN',
    'T': 'BOOLEAN',
    'F': 'BOOLEAN',
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
        line = 1
        while pos < len(self.code):
            if self.code[pos] == '#':
                while pos < len(self.code) and self.code[pos] != '\n':
                    pos += 1
                if pos < len(self.code) and self.code[pos] == '\n':
                    pos += 1
                    line += 1
                continue

            match = re.match(TOKEN_REGEX, self.code[pos:])
            if match:
                kind = match.lastgroup
                text = match.group()
                value = text

                if kind == 'ID' and value in KEYWORDS:
                    kind = KEYWORDS[value]
                if kind == 'BOOLEAN':
                    value = True if text == 'T' else False
                if kind == 'NUMBER':
                    value = float(text) if '.' in text else int(text)
                if kind == 'STRING':
                    # 去除前後雙引號
                    value = text[1:-1]
                elif kind == 'SKIP':
                    pos += len(text)
                    continue
                elif kind == 'NEWLINE':
                    value = '\n'
                    line += 1

                self.tokens.append(Token(kind, value))
                pos += len(text)
            else:
                raise BrokenHandError(f"Illegal character: '{self.code[pos]}' at line {line}")
        self.tokens.append(Token('EOF', None))
        return self.tokens
