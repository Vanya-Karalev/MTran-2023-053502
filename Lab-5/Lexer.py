import re
from Token import Token


class Lexer:
    def __init__(self):
        self.tokens = []
        self.new_tokens = []
        self.var_types_tokens = []
        self.key_word_tokens = []
        self.constants_tokens = {}
        self.var_tokens = {}
        self.func_tokens = {}

    def lex_analyze(self, code):
        find_variable = r"^[a-zA-Z0-9]+(\[[a-zA-Z0-9]*\])?$"
        current_token = ''
        quote_open = False
        for char in code:
            variable_matches = re.findall(find_variable, current_token)
            char_matches = re.findall(find_variable, char)
            if quote_open:
                current_token += char
                if char == "\"":
                    quote_open = False
            elif char == "\"":
                quote_open = True
                current_token += char
            elif char in [" ", "\n", "\t"]:
                if current_token:
                    self.tokens.append(current_token)
                    current_token = ""
            elif char in [";", ",", "{", "}", "(", ")", "/", "*", "[", "]", "+", "-", "<"]:
                if char in ["+", "-", "<"]:
                    if current_token and variable_matches:
                        self.tokens.append(current_token)
                        current_token = ""
                        current_token += char
                    else:
                        current_token += char
                else:
                    if current_token:
                        self.tokens.append(current_token)
                        self.tokens.append(char)
                        current_token = ""
                    else:
                        self.tokens.append(char)
            elif current_token in [";", ",", "{", "}", "(", ")", "/", "*", "[", "]", "+", "-", "<"] and char_matches:
                self.tokens.append(current_token)
                current_token = ""
                current_token += char
            else:
                current_token += char

        return self.tokens

    def get_tokens(self, tokens):
        for i in range(len(tokens)):
            if tokens[i] in ['bool', 'char', 'int', 'float', 'double', 'string', 'void']:
                self.var_types_tokens.append(tokens[i])
                self.new_tokens.append(Token(tokens[i], 'VARIABLE TYPE', ''))
            elif tokens[i] in ['for', 'while', 'continue', 'break', 'if', 'else', 'switch', 'case', 'return', 'cin',
                               'cout', 'endl', 'default', 'new']:
                self.key_word_tokens.append(tokens[i])
                self.new_tokens.append(Token(tokens[i], 'KEY WORD', ''))
            elif tokens[i] in ['true', 'false']:
                self.constants_tokens[tokens[i]] = 'BOOLEAN CONSTANT'
                self.new_tokens.append(Token(tokens[i], 'BOOLEAN CONSTANT', ''))
            elif len(tokens[i]) > 0 and tokens[i][0] == '"' and tokens[i][-1] == '"':
                self.constants_tokens[tokens[i]] = 'STRING CONSTANT'
                self.new_tokens.append(Token(tokens[i], 'STRING CONSTANT', ''))
            elif len(tokens[i]) > 0 and tokens[i][0] == "'" and tokens[i][-1] == "'":
                self.constants_tokens[tokens[i]] = 'CHAR CONSTANT'
                self.new_tokens.append(Token(tokens[i], 'CHAR CONSTANT', ''))
            elif is_int(tokens[i]):
                self.constants_tokens[tokens[i]] = 'INT CONSTANT'
                self.new_tokens.append(Token(tokens[i], 'INT CONSTANT', ''))
            elif is_float(tokens[i]):
                self.constants_tokens[tokens[i]] = 'FLOAT CONSTANT'
                self.new_tokens.append(Token(tokens[i], 'FLOAT CONSTANT', ''))
            elif tokens[i] in [';', '{', '}', '(', ')', '[', ']', ',', ':']:
                self.new_tokens.append(Token(tokens[i], 'SEPARATOR', ''))
            elif tokens[i] in ['+', '-', '*', '/', '%','=', '<', '>', '&', '|','!', '?', '==', '!=', '+=', '-=', '*=',
                               '/=', '<<', '>>', '&&', '||', '++', '--', '<=']:
                self.new_tokens.append(Token(tokens[i], 'OPERATOR', ''))
            elif is_valid_variable_name(tokens[i]) and tokens[i-1] in ['bool', 'char', 'int', 'float', 'double',
                                                                       'string', 'void'] and tokens[i+1] == "(":
                self.func_tokens[tokens[i]] = 'FUNCTION'
                self.new_tokens.append(Token(tokens[i], 'FUNCTION', ''))
            elif is_valid_variable_name(tokens[i]) and tokens[i-1] in ['bool', 'char', 'int', 'float', 'double',
                                                                       'string', 'void'] and tokens[i+1] == "=" or \
                    tokens[i-1] == "," or tokens[i+1] in ["[", "<", '++']:
                self.var_tokens[tokens[i]] = 'VARIABLE'
                self.new_tokens.append(Token(tokens[i], 'VARIABLE', ''))
            else:
                self.new_tokens.append(Token(tokens[i], 'UNKNOWN', ''))
        return self.new_tokens


def is_valid_variable_name(name):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))


def is_int(number_str):
    if not number_str:
        return False
    if not (number_str.isdigit() or (number_str[0] == '-' and number_str[1:].isdigit())):
        return False
    number = int(number_str)
    return number_str == str(number)


def is_float(number_str):
    if not number_str:
        return False
    try:
        float(number_str)
    except ValueError:
        return False
    return not (is_int(number_str) or (number_str[0] == '-' and is_int(number_str[1:])))
