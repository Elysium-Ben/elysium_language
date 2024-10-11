# src/main.py

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter
import sys
import textwrap

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    try:
        with open(source_file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"File not found: {source_file}")
        sys.exit(1)

    code = textwrap.dedent(code)

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    interpreter = Interpreter(ast)
    interpreter.execute()

if __name__ == "__main__":
    main()
