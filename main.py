import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from error import BrokenHandError
sys.stdout.reconfigure(encoding='utf-8')
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py source.bh")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r',encoding='utf-8') as f:
        code = f.read()

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        tree = parser.parse()
        interpreter = Interpreter(tree)
        interpreter.interpret()
        # for t in tokens:
        #     print(t)
    except BrokenHandError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()