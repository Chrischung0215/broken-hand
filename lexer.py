import re
from error import BrokenHandError

TOKEN_SPEC = [
    ('PRINT',    r'p'),
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('BOOLEAN',  r'T|F'),
    ('STRING',   r'"[^"\n]*"'),
    ('IF',       r'\?'),
    ('ELSE',     r'~'),
    ('WHILE',    r'@'),
    ('FOR',      r'\$'),
    ('SWITCH',   r'\^'),
    ('NE', r'!='),
    ('BREAK',    r'<<'),
    ('CONTINUE', r'>>'),
    ('NOT',      r'!'),
    ('CASE',     r'\|'),
    ('DEFAULT',  r'_'),
    ('MOD',      r'%'),
    ('FUNCTION', r'f'),
    ('RETURN',   r'r'),
    ('EQ',       r'=='),
    ('LE',       r'<='),
    ('GE',       r'>='),
    ('ASSIGN',   r'='),
    ('COLON',    r':'),
    ('SEMICOLON',r';'),
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
    ('AND',      r'&&'),
    ('OR',       r'\|\|'),
    ('LT',       r'<'),
    ('GT',       r'>'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

KEYWORDS = {
    'T': 'BOOLEAN',
    'F': 'BOOLEAN',
}

class Token:
    def __init__(self, type_, value, line=1, column=1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value}, line={self.line}, column={self.column})'

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        pos = 0
        line = 1
        col = 1
        while pos < len(self.code):
            if self.code[pos] == '#':
                while pos < len(self.code) and self.code[pos] != '\n':
                    pos += 1
                if pos < len(self.code) and self.code[pos] == '\n':
                    pos += 1
                    line += 1
                    col = 1
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
                    value = text[1:-1]
                elif kind == 'SKIP':
                    pos += len(text)
                    col += len(text)
                    continue
                elif kind == 'NEWLINE':
                    value = '\n'
                    line += 1
                    col = 1

                self.tokens.append(Token(kind, value, line, col))
                pos += len(text)
                if kind == 'NEWLINE':
                    col = 1
                else:
                    col += len(text)
            else:
                raise BrokenHandError(f"Illegal character: '{self.code[pos]}' at line {line}, column {col}")
        self.tokens.append(Token('EOF', None, line, col))
        return self.tokens
