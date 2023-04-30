from pycparser import c_parser, c_ast
import re
from prettytable import PrettyTable

operator_pattern = r'([><=]=|[<>+\-*/()%!=]|<<|>>|\(\)|==|<=|>=|;)'
keyword_pattern = r'\b(int|double|float|char|if|else|for|while|do|switch|case|break|continue|return|bool|endl|const|cin|' \
                  r'cout|for|void|class|string)\b'
# variable_pattern = r'\b((?!^\d)[a-zA-Z_]+[a-zA-Z0-9_]*(\[[^\[\]]*\])*)\s*\=\s*([\w\.\-0-9_]*(\[[\w\.\-0-9_+]*\])?)\s*'
# constant_pattern = r'\b([0-9]+(\.[0-9]+)?)\b'
# output_string_pattern = r'cout\s*<<\s*"(.*)"\s*;'


all_operators = ["+", "-", "*", "/", "%", "=", "+=", "-=", "*=", "/=", "%=", "==", "!=", "<", ">", "<=", ">=",
                 "!", "&&", "||", "~", "&", "|", "^", "<<", ">>", "++", "--", "-", "? :", "&", "*", ".", "->"]
words = ["and", "and_eq", "auto", "bool", "break", "case", "catch", "char", "class", "const", "continue", "goto",
         "default", "delete", "do", "double", "else", "enum", "export", "extern", "false", "float", "for", "friend",
         "if", "inline", "int", "long", "mutable", "namespace", "new", "protected", "public", "requires", "return",
         "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "short", "signed", "sizeof", "static",
         "struct", "switch", "template", "this", "throw", "true", "try", "typedef", "cout"
         "typeid", "typename", "union", "unsigned", "using", "virtual", "void", "while", "xor", "xor_eq", "cin"]
all_types = ["int", "double", "float", "char", "string", "void"]
find_func = r'\b[a-zA-Z]\w*\b'
find_variable = r"^[a-zA-Z0-9]+(\[[a-zA-Z0-9]*\])?$"
find_numbers = r"^[0-9.]+$"
find_string = r'^["\']'


tokens = []
reversed_words = {}
constants = {}
operators = {}
functions = {}
variable = {}

def lex_analyze(code):
    current_token = ""
    open_paren_count = 0
    quote_open = False
    bracket_open = False
    for char in code:
        variable_matches = re.findall(find_variable, current_token)
        char_matches = re.findall(find_variable, char)
        # if char == "[":
        #     bracket_open = True
        #     current_token += char
        # elif char == "]":
        #     bracket_open = False
        #     current_token += char
        # elif bracket_open is True:
        #     current_token += char
        # if char == "(" and current_token not in keyword_pattern:
        #     open_paren_count += 1
        #     current_token += char
        # elif char == ")":
        #     if open_paren_count > 0:
        #         open_paren_count -= 1
        #     if "(" in current_token:
        #         current_token += char
        #     else:
        #         tokens.append(char)
        # elif open_paren_count > 0:
        #     current_token += char
        if quote_open:
            current_token += char
            if char == "\"":
                quote_open = False
        elif char == "\"":
            quote_open = True
            current_token += char
        elif char in [" ", "\n", "\t"]:
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char in [";", ",", "{", "}", "(", ")", "/", "*", "[", "]", "+", "-"]:
            if char in ["+", "-"]:
                if current_token and variable_matches:
                    tokens.append(current_token)
                    current_token = ""
                    current_token += char
                else:
                    current_token += char
            else:
                if current_token:
                    tokens.append(current_token)
                    tokens.append(char)
                    current_token = ""
                else:
                    tokens.append(char)
        elif current_token in [";", ",", "{", "}", "(", ")", "/", "*", "[", "]", "+", "-"] and char_matches:
            tokens.append(current_token)
            current_token = ""
            current_token += char
        else:
            current_token += char

    print("Tokens:")
    for i, token in enumerate(tokens):
        print(f"{i + 1}. {token}")

    for i in range(len(tokens)):
        if tokens[i] in words:
            if tokens[i] in all_types:
                reversed_words[tokens[i]] = 'key word of variable type'
            else:
                reversed_words[tokens[i]] = 'key word'

    words_table = PrettyTable(['Keyword', 'Type'])
    for (token_value, token_type) in reversed_words.items():
        words_table.add_row([token_value, token_type])
    print('Reversed words:\n', words_table)

    for i in range(len(tokens)):
        string_matches = re.findall(find_string, tokens[i])
        numbers_matches = re.findall(find_numbers, tokens[i])
        if string_matches:
            constants[tokens[i]] = 'string const'
        elif numbers_matches:
            constants[tokens[i]] = 'number const'

    constants_table = PrettyTable(['Keyword', 'Type'])
    for (token_value, token_type) in constants.items():
        constants_table.add_row([token_value, token_type])
    print('Constants:\n', constants_table)

    for i in range(len(tokens)):
        if tokens[i] in all_operators:
            operators[tokens[i]] = 'operator'

    operators_table = PrettyTable(['Keyword', 'Type'])
    for (token_value, token_type) in operators.items():
        operators_table.add_row([token_value, token_type])
    print('Operators:\n', operators_table)

    for i in range(len(tokens)):
        func_matches = re.findall(find_func, tokens[i])
        if func_matches and tokens[i-1] in all_types and tokens[i+1] == "(":
            functions[tokens[i]] = f'{tokens[i-1]} function'

    func_table = PrettyTable(['Keyword', 'Type'])
    for (token_value, token_type) in functions.items():
        func_table.add_row([token_value, token_type])
    print('Functions:\n', func_table)

    for i in range(len(tokens)):
        variable_matches = re.findall(find_variable, tokens[i])
        numbers_matches = re.findall(find_numbers, tokens[i])
        if variable_matches and tokens[i-1] in all_types and tokens[i+1] != "(":
            variable[tokens[i]] = f'{tokens[i-1]} variable'
        elif variable_matches and tokens[i-1] == "," and not numbers_matches:
            variable[tokens[i]] = 'variable'

    variable_table = PrettyTable(['Keyword', 'Type'])
    for (token_value, token_type) in variable.items():
        variable_table.add_row([token_value, token_type])
    print('Variables:\n', variable_table)
def analyze_cpp_code(cpp_code):
    parser = c_parser.CParser()
    try:
        ast = parser.parse(cpp_code)
        for node in ast:
            # Поиск операторов
            if isinstance(node, c_ast.BinaryOp):
                operator = node.op
                if operator not in operator_pattern:
                    raise Exception(f"Invalid operator {operator}")
            # Поиск идентификаторов
            elif isinstance(node, c_ast.ID):
                identifier = node.name
                if identifier in keyword_pattern:
                    raise Exception(f"Invalid identifier {identifier}")
            # Поиск вызовов функций
            elif isinstance(node, c_ast.FuncCall):
                func_name = node.name.name
                if func_name in keyword_pattern:
                    raise Exception(f"Invalid function name {func_name}")
                for arg in node.args:
                    if isinstance(arg, c_ast.ID):
                        arg_name = arg.name
                        if arg_name in keyword_pattern:
                            raise Exception(f"Invalid identifier {arg_name}")
            # Поиск объявлений переменных
            elif isinstance(node, c_ast.Decl):
                var_name = node.name
                if var_name in keyword_pattern:
                    raise Exception(f"Invalid variable name {var_name}")
                if node.type is not None:
                    var_type = node.type.type.names[-1]
                    if var_type in keyword_pattern:
                        raise Exception(f"Invalid variable type {var_type}")
                # Поиск указателей
                if isinstance(node.type, c_ast.PtrDecl):
                    pointer = node.type.type.names[-1]
                    if pointer in keyword_pattern:
                        raise Exception(f"Invalid pointer type {pointer}")
            # Поиск оператора возврата
            elif isinstance(node, c_ast.Return):
                if isinstance(node.expr, c_ast.ID):
                    ret_name = node.expr.name
                    if ret_name in keyword_pattern:
                        raise Exception(f"Invalid return value {ret_name}")
            # Поиск операторов приведения типа
            elif isinstance(node, c_ast.Cast):
                cast_type = node.to_type.type.names[-1]
                if cast_type in keyword_pattern:
                    raise Exception(f"Invalid cast type {cast_type}")
            # Поиск операторов условных выражений
            elif isinstance(node, c_ast.If):
                if isinstance(node.cond, c_ast.ID):
                    cond_name = node.cond.name
                    if cond_name in keyword_pattern:
                        raise Exception(f"Invalid conditional expression {cond_name}")
        lex_analyze(cpp_code)
    except Exception as e:
        print(f"Error analyzing code: {e}")


if __name__ == '__main__':
    with open('main.cpp', 'r') as file:
        code = file.read()
    analyze_cpp_code(code)
