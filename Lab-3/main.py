from Lexer import Lexer
from Parser import Parser
from Parser import get_tree
from prettytable import PrettyTable


def print_tokens(tokens):
    tokens_table = PrettyTable(['Keyword', 'Type'])
    for token in tokens:
        tokens_table.add_row([token.word, token.token_type])
    print('Tokens:\n', tokens_table)


def print_tree(node, level=0):
    if isinstance(node, list):
        for child in node:
            print_tree(child, level + 1)
    else:
        print("\t" * level + str(node))


if __name__ == '__main__':
    with open('main.cpp', 'r') as file:
        code = file.read()
    lexer = Lexer()
    tokens = lexer.get_tokens(code)
    print_tokens(tokens)
    parser = Parser(lexer)
    tree = get_tree(parser.parse_code())
    print_tree(tree)
